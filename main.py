import yt_dlp
import sys
import validators
import requests
import subprocess
import re
import os
from requests.exceptions import RequestException
from tqdm import tqdm
import argparse

def mettre_a_jour_ytdlp():
    """Met à jour yt-dlp à la dernière version."""
    print("Mise à jour de yt-dlp...")
    subprocess.run(["pip3", "install", "--upgrade", "yt-dlp"], check=True)
    print("yt-dlp mis à jour !")

def verifier_mise_a_jour_ytdlp():
    """Vérifie si yt-dlp est à jour et met à jour si nécessaire."""
    try:
        result = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
        version_installee = result.stdout.strip()

        result = subprocess.run(["pip", "index", "versions", "yt-dlp"], capture_output=True, text=True)
        versions_disponibles = result.stdout

        if version_installee not in versions_disponibles:
            print("Nouvelle version de yt-dlp disponible, mise à jour en cours...")
            subprocess.run(["pip3", "install", "--upgrade", "yt-dlp"], check=True)
            print("Mise à jour effectuée !")
    except Exception as e:
        print(f"Erreur lors de la vérification de la mise à jour : {e}")

def verifier_url(url):
    """Vérifie si l'URL fournie est valide."""
    return validators.url(url)

def remove_ansi_escape_sequences(text):
    """Supprime les séquences d'échappement ANSI pour éviter les erreurs de conversion."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def my_hook(d):
    """Affiche la progression du téléchargement avec `tqdm`."""
    if d['status'] == 'downloading':
        percent_str = d.get('_percent_str', '0%')
        percent_str_clean = remove_ansi_escape_sequences(percent_str)
        try:
            percent = float(percent_str_clean.strip('%'))
        except ValueError:
            percent = 0
        tqdm(total=100, initial=percent).update(percent)
    elif d['status'] == 'finished':
        print("Téléchargement terminé, conversion en MP4...")

def telecharger_video(url, audio_only=False, format_video="mp4", output_dir="~/Downloads/", playlist=False):
    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
        'outtmpl': f"{output_dir}/%(title)s.%(ext)s",
        'merge_output_format': format_video,
        'progress_hooks': [my_hook],
        'noplaylist': not playlist,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Téléchargeur de vidéos avancé avec yt-dlp", add_help=True)

    parser.add_argument("url", help="URL de la vidéo à télécharger")
    parser.add_argument("--audio", action="store_true", help="Télécharger uniquement l'audio")
    parser.add_argument("--format", default="mp4", help="Format de sortie (mp4, mkv, webm...)")
    parser.add_argument("--output", default="~/Downloads/", help="Dossier de destination")
    parser.add_argument("--playlist", action="store_true", help="Télécharger une playlist complète")
    parser.add_argument("--update", action="store_true", help="Mettre à jour yt-dlp")

    args = parser.parse_args()

    if not args.update:
        verifier_mise_a_jour_ytdlp()

    if args.update:
        mettre_a_jour_ytdlp()
        sys.exit(0)

    telecharger_video(
        url=args.url,
        audio_only=args.audio,
        format_video=args.format,
        output_dir=args.output,
        playlist=args.playlist
    )
