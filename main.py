import yt_dlp
import sys
import re
import os
import json
import argparse
import subprocess
import urllib.request
from tqdm import tqdm
from colorama import Fore, init

init(autoreset=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def strip_ansi(text: str) -> str:
    return re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', text)


def validate_url(url: str) -> bool:
    return url.startswith(("http://", "https://"))


# ── yt-dlp update ──────────────────────────────────────────────────────────────

def get_installed_version() -> str | None:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--version"],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    except Exception:
        return None


def get_latest_version() -> str | None:
    try:
        with urllib.request.urlopen("https://pypi.org/pypi/yt-dlp/json", timeout=5) as r:
            return json.load(r)["info"]["version"]
    except Exception:
        return None


def update_ytdlp():
    print(f"{Fore.YELLOW}🔄 Updating yt-dlp...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], check=True)
    print(f"{Fore.GREEN}✅ yt-dlp updated successfully.")


def check_for_update():
    installed = get_installed_version()
    latest = get_latest_version()
    if installed and latest and installed != latest:
        print(f"{Fore.CYAN}⚠️  New version available ({latest}), updating...")
        update_ytdlp()


# ── Progress hook ──────────────────────────────────────────────────────────────

class ProgressHandler:
    def __init__(self, audio_only: bool, fmt: str):
        self.bar = None
        self.audio_only = audio_only
        self.fmt = fmt

    def hook(self, d: dict):
        if d["status"] == "downloading":
            percent_str = strip_ansi(d.get("_percent_str", "0%")).strip().rstrip("%")
            try:
                percent = float(percent_str)
            except ValueError:
                percent = 0.0

            if self.bar is None:
                self.bar = tqdm(
                    total=100,
                    bar_format=f"{Fore.GREEN}⬇  |{{bar}}| {{percentage:.0f}}%",
                    colour="green",
                )
            self.bar.n = percent
            self.bar.refresh()

        elif d["status"] == "finished":
            if self.bar:
                self.bar.n = 100
                self.bar.refresh()
                self.bar.close()
                self.bar = None
            if self.audio_only:
                print(f"\n{Fore.GREEN}✅ Download complete, extracting audio...")
            else:
                print(f"\n{Fore.GREEN}✅ Download complete, merging to {self.fmt.upper()}...")

        elif d["status"] == "error":
            if self.bar:
                self.bar.close()
                self.bar = None
            print(f"\n{Fore.RED}❌ An error occurred during download.")


# ── Download ───────────────────────────────────────────────────────────────────

def download(url: str, audio_only: bool, fmt: str, output_dir: str, playlist: bool):
    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    handler = ProgressHandler(audio_only=audio_only, fmt=fmt)

    ydl_opts = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "progress_hooks": [handler.hook],
        "noplaylist": not playlist,
        "ignoreerrors": playlist,   # skip unavailable videos in playlists
        "quiet": True,
        "no_warnings": True,
        # Always try to get the best quality available
        "format": "bestaudio/best" if audio_only else "bestvideo+bestaudio/best",
        "merge_output_format": fmt if not audio_only else None,
        # Audio extraction
        "postprocessors": (
            [{"key": "FFmpegExtractAudio", "preferredcodec": fmt if fmt in ("mp3", "aac", "opus", "flac", "wav", "m4a") else "mp3"}]
            if audio_only else []
        ),
        # Broad compatibility: retry on transient errors
        "retries": 5,
        "fragment_retries": 5,
        # Some sites require cookies / age gate bypass
        "age_limit": None,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as e:
        print(f"{Fore.RED}❌ Download error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}❌ Unexpected error: {e}")
        sys.exit(1)


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Download any video from any website using yt-dlp.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python video_dl.py https://youtube.com/watch?v=xxx
  python video_dl.py https://youtube.com/watch?v=xxx --audio --format mp3
  python video_dl.py https://youtube.com/playlist?list=xxx --playlist
  python video_dl.py https://twitter.com/x/status/xxx --output ~/Videos/
  python video_dl.py --update
        """
    )

    parser.add_argument("url", nargs="?", help="URL of the video to download")
    parser.add_argument("--audio",    action="store_true",   help="Extract audio only")
    parser.add_argument("--format",   default="mp4",         help="Output format: mp4, mkv, webm, mp3, m4a… (default: mp4)")
    parser.add_argument("--output",   default="~/Downloads/",help="Output directory (default: ~/Downloads/)")
    parser.add_argument("--playlist", action="store_true",   help="Download full playlist")
    parser.add_argument("--update",   action="store_true",   help="Update yt-dlp to latest version")

    args = parser.parse_args()

    # --update doesn't need a URL
    if args.update:
        update_ytdlp()
        sys.exit(0)

    if not args.url:
        parser.print_help()
        sys.exit(1)

    if not validate_url(args.url):
        print(f"{Fore.RED}❌ Invalid URL: {args.url}")
        sys.exit(1)

    # Auto-check for yt-dlp update before downloading
    check_for_update()

    print(f"{Fore.CYAN}🎬 Starting download: {args.url}")
    download(
        url=args.url,
        audio_only=args.audio,
        fmt=args.format,
        output_dir=args.output,
        playlist=args.playlist,
    )

    print(f"{Fore.CYAN}📁 File saved to: {os.path.expanduser(args.output)}")


if __name__ == "__main__":
    main()
