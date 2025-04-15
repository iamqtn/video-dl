import yt_dlp
import sys
import validators
import subprocess
import re
import os
import argparse
from requests.exceptions import RequestException
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)  # Active la coloration automatique

progress_bar = None  # Global pour suivre une seule barre

def mettre_a_jour_ytdlp():
    print(f"{Fore.YELLOW}🔄 Mise à jour de yt-dlp...")
    subprocess.run(["pip3", "install", "--upgrade", "yt-dlp"], check=True)
    print(f"{Fore.GREEN}✅ yt-dlp mis à jour avec succès !")

def verifier_mise_a_jour_ytdlp():
    try:
        result = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
        version_installee = result.stdout.strip()

        result = subprocess.run(["pip", "index", "versions", "yt-dlp"], capture_output=True, text=True)
        versions_disponibles = result.stdout

        if version_installee not in versions_disponibles:
            print(f"{Fore.CYAN}⚠️ Nouvelle version disponible : mise à jour en cours...")
            mettre_a_jour_ytdlp()
    except Exception as e:
        print(f"{Fore.RED}❌ Erreur lors de la vérification de la mise à jour : {e}")

def verifier_url(url):
    return validators.url(url)

def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def my_hook(d):
    global progress_bar

    if d['status'] == 'downloading':
        percent_str = d.get('_percent_str', '0%')
        percent_str_clean = remove_ansi_escape_sequences(percent_str)
        try:
            percent = float(percent_str_clean.strip('%'))
        except ValueError:
            percent = 0.0

        if progress_bar is None:
            progress_bar = tqdm(total=100, bar_format=f"{Fore.GREEN}⬇️  |{{bar}}| {{percentage:.0f}}%", colour="green")
        progress_bar.n = percent
        progress_bar.refresh()

    elif d['status'] == 'finished':
        if progress_bar:
            progress_bar.close()
            print(f"\n{Fore.GREEN}✅ Téléchargement terminé, conversion en MP4 en cours...")

def telecharger_video(url, audio_only=False, format_video="mp4", output_dir="~/Downloads/", playlist=False):
    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
        'outtmpl': f"{output_dir}/%(title)s.%(ext)s",
        'merge_output_format': format_video,
        'progress_hooks': [my_hook],
        'noplaylist': not playlist,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"{Fore.RED}❌ Erreur lors du téléchargement : {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🎥 Téléchargeur de vidéos avancé avec yt-dlp")

    parser.add_argument("url", help="URL de la vidéo à télécharger")
    parser.add_argument("--audio", action="store_true", help="Télécharger uniquement l'audio")
    parser.add_argument("--format", default="mp4", help="Format de sortie (mp4, mkv, webm...)")
    parser.add_argument("--output", default="~/Downloads/", help="Dossier de destination")
    parser.add_argument("--playlist", action="store_true", help="Télécharger une playlist complète")
    parser.add_argument("--update", action="store_true", help="Mettre à jour yt-dlp")

    args = parser.parse_args()

    if not verifier_url(args.url):
        print(f"{Fore.RED}❌ L'URL fournie n'est pas valide.")
        sys.exit(1)

    if args.update:
        mettre_a_jour_ytdlp()
        sys.exit(0)
    else:
        verifier_mise_a_jour_ytdlp()

    telecharger_video(
        url=args.url,
        audio_only=args.audio,
        format_video=args.format,
        output_dir=args.output,
        playlist=args.playlist
    )

    print(f"{Fore.CYAN}🎉 Fichier disponible dans : {os.path.expanduser(args.output)}")
