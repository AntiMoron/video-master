#!/usr/bin/env python3
"""
hf_oauth.py — Higgsfield 视频生成（Gmail/OAuth 订阅用户）

从浏览器 DevTools Network 标签获取两个值（fnf.higgsfield.ai 的任意请求）：
  - Authorization header → HF_JWT
  - x-datadome-clientid header → HF_DATADOME

使用方法:
  export HF_JWT="eyJhbGc..."
  export HF_DATADOME="bl14hxa9..."
  python3 hf_oauth.py "视频描述" [--aspect 9:16] [--duration 5] [--output out.mp4]
"""

import os
import sys
import time
import json
import base64
import argparse
from typing import Optional, Dict, Any

try:
    from curl_cffi import requests
    IMPERSONATE = "chrome131"
except ImportError:
    sys.exit("❌ 缺少依赖，请运行: pip3 install curl_cffi")

API_BASE   = "https://fnf.higgsfield.ai"

ASPECT_DIMS = {
    "9:16":  (720, 1280),
    "16:9":  (1280, 720),
    "1:1":   (720, 720),
    "4:3":   (960, 720),
}


def jwt() -> str:
    token = os.environ.get("HF_JWT", "").strip()
    if not token:
        sys.exit("❌ 未找到 JWT。请先运行:\n   export HF_JWT=\"eyJ...\"")
    # 解码 JWT payload 检查过期时间
    try:
        payload_b64 = token.split(".")[1]
        payload_b64 += "=" * (-len(payload_b64) % 4)  # padding
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        exp = payload.get("exp", 0)
        remaining = exp - time.time()
        if remaining <= 0:
            sys.exit(
                f"❌ JWT 已过期（{int(-remaining)}秒前到期）\n"
                "   请重新从浏览器复制：\n"
                "   DevTools → Network → fnf.higgsfield.ai 任意请求\n"
                "   → Headers → Authorization: Bearer eyJ...\n"
                "   → export HF_JWT=\"eyJ...\""
            )
        if remaining < 60:
            print(f"⚠️  JWT 还剩 {int(remaining)}秒有效期，请尽快完成操作")
        else:
            print(f"  JWT 有效期剩余: {int(remaining)}秒")
    except Exception:
        pass  # 解析失败时继续，让 API 返回 401 再提示
    return token


def make_session() -> requests.Session:
    return requests.Session(impersonate=IMPERSONATE)


def browser_headers() -> dict:
    """完整浏览器指纹 headers，匹配 Chrome 148 on macOS"""
    h = {
        "accept": "*/*",
        "accept-language": "en",
        "content-type": "application/json",
        "origin": "https://higgsfield.ai",
        "referer": "https://higgsfield.ai/",
        "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/148.0.0.0 Safari/537.36"
        ),
        "Authorization": f"Bearer {jwt()}",
    }
    datadome = os.environ.get("HF_DATADOME", "").strip()
    if datadome:
        h["x-datadome-clientid"] = datadome
    return h


def submit_video(session, prompt: str, aspect: str, duration: int,
                 sound: str = "on", enhance: bool = True) -> Optional[str]:
    width, height = ASPECT_DIMS.get(aspect, (720, 1280))
    payload = {
        "params": {
            "prompt": prompt,
            "width": width,
            "height": height,
            "aspect_ratio": aspect,
            "mode": "std",
            "sound": sound,
            "duration": duration,
            "medias": [],
            "multi_shots": False,
            "multi_prompt": [],
            "cfg_scale": 0.5,
            "kling_elements": [],
            "kling_element_ids": [],
            "multi_shot_mode": "auto",
            "reference_elements": [],
            "enhance_prompt": enhance,
        },
        "use_free_gens": False,
        "use_unlim": False,
    }
    resp = session.post(
        f"{API_BASE}/jobs/v2/kling3_0",
        json=payload,
        headers=browser_headers(),
        timeout=30,
    )
    if resp.status_code != 200:
        sys.exit(f"❌ 提交失败 {resp.status_code}:\n{resp.text[:500]}")

    data = resp.json()
    job_sets = data.get("job_sets", [])
    if job_sets:
        return job_sets[0]["id"]
    return data.get("id")


def poll_job_set(session, job_set_id: str, timeout: int = 600) -> Optional[Dict]:
    url = f"{API_BASE}/job-sets/{job_set_id}"
    deadline = time.time() + timeout
    dots = 0
    while time.time() < deadline:
        try:
            resp = session.get(url, headers=browser_headers(), timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                jobs = data.get("jobs", [])
                if jobs:
                    status = jobs[0].get("status", "")
                    dots = (dots + 1) % 4
                    print(f"  状态: {status}{'.' * dots}   ", end="\r", flush=True)
                    if status == "completed":
                        print(f"  状态: completed ✓          ")
                        return data
                    if status == "failed":
                        print()
                        sys.exit(f"❌ 生成失败: {json.dumps(data, indent=2)}")
        except Exception:
            pass
        time.sleep(3)
    sys.exit(f"❌ 超时 ({timeout}s)")


def extract_video_url(data: Dict) -> str:
    def _find(obj):
        if isinstance(obj, str) and obj.startswith("http") and (
            ".mp4" in obj or "video" in obj or "media" in obj
        ):
            return obj
        if isinstance(obj, dict):
            for v in obj.values():
                r = _find(v)
                if r:
                    return r
        if isinstance(obj, list):
            for item in obj:
                r = _find(item)
                if r:
                    return r
        return None

    url = _find(data)
    if not url:
        # broader search: any https URL
        def _find_any_url(obj):
            if isinstance(obj, str) and obj.startswith("https://"):
                return obj
            if isinstance(obj, dict):
                for v in obj.values():
                    r = _find_any_url(v)
                    if r:
                        return r
            if isinstance(obj, list):
                for item in obj:
                    r = _find_any_url(item)
                    if r:
                        return r
            return None
        url = _find_any_url(data)

    if not url:
        sys.exit(f"❌ 找不到视频 URL，完整响应:\n{json.dumps(data, indent=2)}")
    return url


def download(url: str, path: str, session):
    resp = session.get(url, timeout=120)
    if resp.status_code != 200:
        sys.exit(f"❌ 下载失败 {resp.status_code}: {url}")
    with open(path, "wb") as f:
        f.write(resp.content)


def main():
    parser = argparse.ArgumentParser(description="Higgsfield Kling 3.0 视频生成（OAuth/订阅用户）")
    parser.add_argument("prompt",         help="视频描述")
    parser.add_argument("--aspect",       default="9:16", choices=list(ASPECT_DIMS.keys()))
    parser.add_argument("--duration",     default=5, type=int, choices=[5, 10])
    parser.add_argument("--sound",        default="on", choices=["on", "off"])
    parser.add_argument("--no-enhance",   action="store_true", help="禁用 prompt 增强")
    parser.add_argument("--output",       default="output.mp4")
    args = parser.parse_args()

    print(f"\n🚀 Higgsfield Kling 3.0 — {args.aspect} · {args.duration}s · sound={args.sound}")
    print(f"  Prompt: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}\n")

    session = make_session()

    print("🎬 提交生成任务...")
    job_set_id = submit_video(
        session, args.prompt, args.aspect, args.duration,
        sound=args.sound, enhance=not args.no_enhance,
    )
    if not job_set_id:
        sys.exit("❌ 未获取到 job_set_id")
    print(f"  Job Set ID: {job_set_id}")

    print("⏳ 等待生成完成（约 2-5 分钟）...")
    result = poll_job_set(session, job_set_id)

    video_url = extract_video_url(result)
    print(f"\n⬇️  下载视频...")
    download(video_url, args.output, session)
    print(f"\n✅ 完成！视频保存至: {args.output}")
    print(f"   URL: {video_url}")


if __name__ == "__main__":
    main()
