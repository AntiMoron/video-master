#!/usr/bin/env python3
"""
hf_oauth.py — Higgsfield 视频生成（Gmail/OAuth 订阅用户）

从浏览器 DevTools Network 标签获取 JWT：
  1. 打开 higgsfield.ai，登录
  2. DevTools → Network → 过滤 fnf.higgsfield
  3. 触发任意生成（或刷新 Library 页）
  4. 找到 POST /jobs/... 请求 → Headers → Authorization: Bearer <TOKEN>
  5. 复制 Token 部分（不含 "Bearer "）

使用方法:
  export HF_JWT="eyJhbGc..."
  python3 hf_oauth.py "视频描述" [--aspect 9:16] [--duration 5] [--output out.mp4]
"""

import os
import sys
import time
import json
import argparse
from typing import Optional, Dict, Any

try:
    from curl_cffi import requests
    IMPERSONATE = "chrome131"
except ImportError:
    sys.exit("❌ 缺少依赖，请运行: pip3 install curl_cffi")

API_BASE   = "https://fnf.higgsfield.ai"
WARMUP_URL = "https://higgsfield.ai"

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
    return token


def make_session() -> requests.Session:
    session = requests.Session(impersonate=IMPERSONATE)
    # Warmup to get Cloudflare clearance
    try:
        session.get(WARMUP_URL, timeout=10)
    except Exception:
        pass
    return session


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
    headers = {"Authorization": f"Bearer {jwt()}"}
    resp = session.post(
        f"{API_BASE}/jobs/v2/kling3_0",
        json=payload,
        headers=headers,
        timeout=30,
    )
    if resp.status_code != 200:
        sys.exit(f"❌ 提交失败 {resp.status_code}:\n{resp.text[:500]}")

    data = resp.json()
    # Response: {"id": project_id, "job_sets": [{"id": job_set_id, ...}]}
    job_sets = data.get("job_sets", [])
    if job_sets:
        return job_sets[0]["id"]
    # fallback
    return data.get("id")


def poll_job_set(session, job_set_id: str, timeout: int = 600) -> Optional[Dict]:
    url = f"{API_BASE}/job-sets/{job_set_id}"
    headers = {"Authorization": f"Bearer {jwt()}"}
    deadline = time.time() + timeout
    dots = 0
    while time.time() < deadline:
        try:
            resp = session.get(url, headers=headers, timeout=15)
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
        except Exception as e:
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
