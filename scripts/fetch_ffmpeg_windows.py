#!/usr/bin/env python3
"""
Fetch FFmpeg/FFprobe for Windows and place them into thirdparty/windows/.

This script is intended for CI (GitHub Actions) so the repository does not need to
version large binaries.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as resp, dest.open("wb") as f:
        shutil.copyfileobj(resp, f)


def _latest_btbn_win64_gpl_zip_url() -> tuple[str, str]:
    api = "https://api.github.com/repos/BtbN/FFmpeg-Builds/releases/latest"
    req = urllib.request.Request(api, headers={"User-Agent": "yt-dlp-linux-gui-ci"})
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)

    best = None
    best_score = -1
    for asset in data.get("assets", []):
        name = asset.get("name", "")
        url = asset.get("browser_download_url", "")
        if not name.endswith(".zip") or "win64" not in name:
            continue
        score = 0
        if name.startswith("ffmpeg-N-"):
            score += 100
        if "win64-gpl.zip" in name and "shared" not in name:
            score += 50
        if "shared" in name:
            score -= 10
        if score > best_score:
            best = (name, url)
            best_score = score

    if not best:
        raise RuntimeError("Could not find a suitable win64 GPL FFmpeg zip in latest release assets")
    return best


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    out_dir = repo_root / "thirdparty" / "windows"
    out_dir.mkdir(parents=True, exist_ok=True)

    name, url = _latest_btbn_win64_gpl_zip_url()

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        zip_path = td_path / name
        _download(url, zip_path)

        with zipfile.ZipFile(zip_path) as z:
            ffmpeg_member = None
            ffprobe_member = None
            for member in z.namelist():
                lower = member.lower()
                if lower.endswith("/ffmpeg.exe"):
                    ffmpeg_member = member
                elif lower.endswith("/ffprobe.exe"):
                    ffprobe_member = member
            if not ffmpeg_member or not ffprobe_member:
                raise RuntimeError("ffmpeg.exe/ffprobe.exe not found inside downloaded zip")

            (out_dir / "ffmpeg.exe").write_bytes(z.read(ffmpeg_member))
            (out_dir / "ffprobe.exe").write_bytes(z.read(ffprobe_member))

    print(f"OK: wrote {out_dir / 'ffmpeg.exe'} and {out_dir / 'ffprobe.exe'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

