#!/usr/bin/env python3
"""
Fetch FFmpeg/FFprobe binaries for Windows or Linux and place them into thirdparty/.

This is intended for CI (GitHub Actions) so the repository does not need to version
large binaries.

Windows source:
  - BtbN/FFmpeg-Builds GitHub Releases (latest)

Linux source:
  - johnvansickle.com static builds
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import stat
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path


def _download(url: str, dest: Path, user_agent: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(req) as resp, dest.open("wb") as f:
        shutil.copyfileobj(resp, f)


def _latest_btbn_win64_gpl_zip_url(user_agent: str) -> tuple[str, str]:
    api = "https://api.github.com/repos/BtbN/FFmpeg-Builds/releases/latest"
    req = urllib.request.Request(api, headers={"User-Agent": user_agent})
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)

    best: tuple[str, str] | None = None
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


def _linux_static_url(arch: str) -> str:
    return f"https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-{arch}-static.tar.xz"


def _detect_platform() -> str:
    if sys.platform.startswith("nt"):
        return "windows"
    if sys.platform.startswith("linux"):
        return "linux"
    raise RuntimeError(f"Unsupported platform: {sys.platform}")


def _detect_linux_arch() -> str:
    machine = platform.machine().lower()
    if machine in {"x86_64", "amd64"}:
        return "amd64"
    if machine in {"aarch64", "arm64"}:
        return "arm64"
    raise RuntimeError(f"Unsupported Linux architecture: {platform.machine()}")


def _write_executable(path: Path, data: bytes) -> None:
    path.write_bytes(data)
    mode = path.stat().st_mode
    path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def fetch_windows(repo_root: Path, user_agent: str) -> None:
    if platform.architecture()[0] != "64bit":
        raise RuntimeError("Only 64-bit Windows is supported by this downloader")

    out_dir = repo_root / "thirdparty" / "windows"
    out_dir.mkdir(parents=True, exist_ok=True)

    name, url = _latest_btbn_win64_gpl_zip_url(user_agent)
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        zip_path = td_path / name
        _download(url, zip_path, user_agent=user_agent)

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


def fetch_linux(repo_root: Path, user_agent: str, arch: str | None) -> None:
    out_dir = repo_root / "thirdparty" / "linux"
    out_dir.mkdir(parents=True, exist_ok=True)

    resolved_arch = arch or _detect_linux_arch()
    url = _linux_static_url(resolved_arch)

    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        tar_path = td_path / f"ffmpeg-release-{resolved_arch}-static.tar.xz"
        _download(url, tar_path, user_agent=user_agent)

        with tarfile.open(tar_path, mode="r:xz") as tf:
            ffmpeg_member = None
            ffprobe_member = None
            for member in tf.getmembers():
                name = member.name.lower()
                if name.endswith("/ffmpeg") and member.isfile():
                    ffmpeg_member = member
                elif name.endswith("/ffprobe") and member.isfile():
                    ffprobe_member = member

            if not ffmpeg_member or not ffprobe_member:
                raise RuntimeError("ffmpeg/ffprobe not found inside downloaded tarball")

            ffmpeg_data = tf.extractfile(ffmpeg_member).read()  # type: ignore[union-attr]
            ffprobe_data = tf.extractfile(ffprobe_member).read()  # type: ignore[union-attr]

    _write_executable(out_dir / "ffmpeg", ffmpeg_data)
    _write_executable(out_dir / "ffprobe", ffprobe_data)

    print(f"OK: wrote {out_dir / 'ffmpeg'} and {out_dir / 'ffprobe'}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--platform",
        choices=["auto", "windows", "linux"],
        default="auto",
        help="Which binaries to download (default: auto-detect).",
    )
    parser.add_argument(
        "--linux-arch",
        choices=["amd64", "arm64"],
        default=None,
        help="Linux arch for static build (default: auto-detect).",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Override repository root (default: inferred from script location).",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[1]
    user_agent = "yt-dlp-linux-gui-ci"

    plat = _detect_platform() if args.platform == "auto" else args.platform
    if plat == "windows":
        fetch_windows(repo_root, user_agent=user_agent)
        return 0
    if plat == "linux":
        fetch_linux(repo_root, user_agent=user_agent, arch=args.linux_arch)
        return 0

    raise RuntimeError(f"Unhandled platform: {plat}")


if __name__ == "__main__":
    raise SystemExit(main())
