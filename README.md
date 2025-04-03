# 🎥 Téléchargeur Universel de Vidéos avec `yt-dlp`

Ce script Python permet de **télécharger n'importe quelle vidéo** (ou seulement l’audio) depuis **YouTube, Twitter, TikTok, Instagram, Facebook, et bien d’autres**, grâce à l’outil `yt-dlp`.

## ✨ Fonctionnalités

- ✅ Téléchargement de vidéos ou seulement de l'audio
- ✅ Compatible avec des centaines de sites
- ✅ Conversion dans différents formats (`mp4`, `mkv`, `webm`, etc.)
- ✅ Téléchargement de playlists complètes
- ✅ Mise à jour automatique de `yt-dlp`
- ✅ Interface CLI claire et personnalisable
- ✅ Barre de progression avec `tqdm`

## 📦 Installation

1. Clone ce dépôt :

```bash
git clone https://github.com/ton-utilisateur/video-downloader.git
cd video-downloader
```

2. Installe les dépendances :

```bash
pip install -r requirements.txt
```

3. (Facultatif) Crée un fichier `.env` :

```bash
cp .env.example .env
```

## 🚀 Utilisation

### Téléchargement simple

```bash
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Options

| Option        | Description                                                  |
|---------------|--------------------------------------------------------------|
| `--audio`     | Télécharge uniquement l’audio                                 |
| `--format`    | Spécifie le format de sortie (`mp4`, `mkv`, `webm`, etc.)     |
| `--output`    | Répertoire de destination (par défaut : `~/Downloads/`)       |
| `--playlist`  | Télécharge une playlist complète                              |
| `--update`    | Met à jour `yt-dlp` à la dernière version                     |

### Exemples

- 🎵 Télécharger une vidéo en audio MP3 :

```bash
python main.py "URL" --audio --format mp3
```

- 📁 Changer le dossier de destination :

```bash
python main.py "URL" --output "/chemin/vers/mon/dossier"
```

- 📺 Télécharger une playlist complète :

```bash
python main.py "URL-de-playlist" --playlist
```

- 🔄 Forcer la mise à jour de `yt-dlp` :

```bash
python main.py --update
```

## 🧪 Développement

Si tu souhaites modifier ou améliorer ce script :

- Le fichier principal est `main.py`
- Toutes les dépendances sont listées dans `requirements.txt`
- Tu peux ajouter des variables d’environnement via `.env`

## 🧼 Astuce : créer un alias Bash

Ajoute cette ligne dans ton `~/.bashrc` ou `~/.zshrc` :

```bash
alias dlvid="python /chemin/vers/video-downloader/main.py"
```

---

## ❓ FAQ

**Q : Pourquoi utiliser `yt-dlp` plutôt que `youtube-dl` ?**  
R : `yt-dlp` est un fork plus actif et maintenu, avec plus de fonctionnalités (meilleur support des plateformes modernes).

**Q : Le téléchargement échoue avec certaines URL ?**  
R : Assure-toi d’avoir bien la dernière version avec `--update`. Certains sites changent souvent leur structure.

**Q : Le format de sortie n’est pas reconnu ?**  
R : Installe `ffmpeg` si ce n’est pas déjà fait (`sudo apt install ffmpeg` ou `brew install ffmpeg`).

---

## 📜 Licence

MIT © Sunvy. Utilisation libre, modification encouragée.
