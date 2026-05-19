#!/usr/bin/env python3
"""
Higgsfield Video Generator — 两步流水线
Step 1: 文字 → 静帧  (Seedream v4)
Step 2: 静帧 → 视频  (Kling 2.1 Pro)

使用方法:
  export HF_CREDENTIALS="KEY_ID:KEY_SECRET"
  python generate.py --prompt "视频动作描述" [选项]

选项:
  --prompt       视频动作/内容描述 (必填)
  --image-prompt 首帧静帧的描述 (可选，默认与 prompt 相同)
  --aspect       画面比例: 9:16 | 16:9 | 1:1  (默认 9:16)
  --duration     时长秒数: 5 | 10               (默认 5)
  --output       输出文件路径                   (默认 output.mp4)
"""

import os
import sys
import time
import json
import argparse
import urllib.request
import urllib.error

BASE_URL = "https://platform.higgsfield.ai"
IMAGE_MODEL = "bytedance/seedream/v4/text-to-image"
VIDEO_MODEL = "kling-video/v2.1/pro/image-to-video"

# Seedream aspect ratios differ slightly from video ratios
ASPECT_MAP = {
    "9:16": "2:3",
    "16:9": "3:2",
    "1:1":  "1:1",
    "4:3":  "4:3",
    "3:4":  "3:4",
}


def credentials() -> tuple[str, str]:
    raw = os.environ.get("HF_CREDENTIALS", "")
    if not raw or ":" not in raw:
        sys.exit("❌ 未找到凭证。请先运行:\n   export HF_CREDENTIALS=\"KEY_ID:KEY_SECRET\"")
    key_id, key_secret = raw.split(":", 1)
    return key_id, key_secret


def auth_header() -> dict:
    key_id, key_secret = credentials()
    return {
        "Authorization": f"Key {key_id}:{key_secret}",
        "Content-Type": "application/json",
    }


def _request(method: str, path: str, body: dict | None = None) -> dict:
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=auth_header(), method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode(errors="replace")
        sys.exit(f"❌ HTTP {e.code} on {method} {path}:\n{err_body}")


def submit(model: str, input_fields: dict) -> str:
    """POST /model → returns request_id"""
    data = _request("POST", f"/{model}", input_fields)
    request_id = data.get("request_id") or data.get("id")
    if not request_id:
        sys.exit(f"❌ 响应中未找到 request_id: {data}")
    return request_id


def poll(request_id: str, label: str, timeout: int = 600) -> dict:
    """轮询直到 completed / failed"""
    deadline = time.time() + timeout
    dots = 0
    while time.time() < deadline:
        data = _request("GET", f"/requests/{request_id}/status")
        status = data.get("status", "")
        dots = (dots + 1) % 4
        print(f"  [{label}] {status}{'.' * dots}   ", end="\r", flush=True)
        if status == "completed":
            print(f"  [{label}] completed ✓          ")
            return data
        if status in ("failed", "nsfw", "canceled"):
            print()
            sys.exit(f"❌ Job {status}: {json.dumps(data, indent=2)}")
        time.sleep(4)
    sys.exit(f"❌ 超时 ({timeout}s) waiting for {label}")


def extract_url(data: dict, kind: str) -> str:
    """从完成响应中提取 image 或 video URL"""
    if kind == "image":
        images = data.get("images") or []
        if images:
            return images[0].get("url", "")
    if kind == "video":
        video = data.get("video") or {}
        if video:
            return video.get("url", "")
    # fallback: search recursively
    def _find(obj):
        if isinstance(obj, dict):
            for k in ("url", "image_url", "video_url"):
                if k in obj and isinstance(obj[k], str) and obj[k].startswith("http"):
                    return obj[k]
            for v in obj.values():
                result = _find(v)
                if result:
                    return result
        elif isinstance(obj, list):
            for item in obj:
                result = _find(item)
                if result:
                    return result
        return None
    url = _find(data)
    if not url:
        sys.exit(f"❌ 找不到 {kind} URL，完整响应:\n{json.dumps(data, indent=2)}")
    return url


def download(url: str, path: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        with open(path, "wb") as f:
            f.write(resp.read())


def main():
    parser = argparse.ArgumentParser(description="Higgsfield 两步视频生成")
    parser.add_argument("--prompt",       required=True, help="视频动作/内容描述")
    parser.add_argument("--image-prompt", help="首帧静帧的描述 (默认同 --prompt)")
    parser.add_argument("--aspect",       default="9:16", choices=["9:16", "16:9", "1:1", "4:3"])
    parser.add_argument("--duration",     default=5, type=int, choices=[5, 10])
    parser.add_argument("--output",       default="output.mp4")
    parser.add_argument("--image-only",   action="store_true", help="只生成首帧，不做视频")
    parser.add_argument("--image-url",    help="跳过 Step 1，直接用此 URL 做 Step 2")
    args = parser.parse_args()

    image_prompt = args.image_prompt or args.prompt

    # ── Step 1: 文字 → 静帧 ──────────────────────────────────────────────
    if args.image_url:
        image_url = args.image_url
        print(f"⏭  跳过 Step 1，使用提供的图片 URL")
    else:
        print(f"\n🖼  Step 1/2 — 生成首帧 ({IMAGE_MODEL})")
        print(f"  提示词: {image_prompt[:80]}{'...' if len(image_prompt) > 80 else ''}")
        req_id = submit(IMAGE_MODEL, {
            "prompt": image_prompt,
            "aspect_ratio": ASPECT_MAP.get(args.aspect, "2:3"),
        })
        img_data = poll(req_id, "Seedream")
        image_url = extract_url(img_data, "image")
        print(f"  图片 URL: {image_url}")

        if args.image_only:
            img_path = args.output.replace(".mp4", ".jpg") if args.output.endswith(".mp4") else args.output + ".jpg"
            print(f"\n⬇️  下载图片...")
            download(image_url, img_path)
            print(f"✅ 完成: {img_path}")
            return

    # ── Step 2: 静帧 → 视频 ──────────────────────────────────────────────
    print(f"\n🎬 Step 2/2 — 生成视频 ({VIDEO_MODEL})")
    print(f"  比例: {args.aspect}  时长: {args.duration}s")
    req_id = submit(VIDEO_MODEL, {
        "prompt": args.prompt,
        "image_url": image_url,
        "aspect_ratio": args.aspect,
        "duration": args.duration,
    })
    vid_data = poll(req_id, "Kling 2.1", timeout=600)
    video_url = extract_url(vid_data, "video")

    print(f"\n⬇️  下载视频...")
    download(video_url, args.output)
    print(f"\n✅ 完成！视频保存至: {args.output}")
    print(f"   原始 URL: {video_url}")


if __name__ == "__main__":
    main()
