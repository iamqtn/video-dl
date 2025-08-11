# 🎥 Téléchargeur Universel de Vidéos avec `yt-dlp`

Ce script Python te permet de **télécharger n'importe quelle vidéo (ou seulement l’audio)** depuis **YouTube, Twitter, TikTok, Instagram, Facebook**, et bien d’autres plateformes supportées par [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).

## ✨ Fonctionnalités

- ✅ Téléchargement de vidéos ou uniquement de l'audio
- ✅ Compatible avec **des centaines de sites**
- ✅ Conversion dans différents formats (`mp4`, `mkv`, `webm`, `mp3`, etc.)
- ✅ Téléchargement de **playlists complètes**
- ✅ Mise à jour automatique de `yt-dlp`
- ✅ Interface CLI simple, colorée et ergonomique
- ✅ Barre de progression dynamique avec `tqdm`
- ✅ Messages colorés avec `colorama`
- ✅ Vérification automatique de la validité de l’URL

## 📦 Installation

1. Clone ce dépôt :

```bash
git clone https://github.com/iamqtn/video-dl.git
cd video-dl
```

2. (Recommandé) Crée un environnement virtuel :

```bash
python3 -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate sous Windows
```

3. Installe les dépendances :

```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

### Téléchargement simple

```bash
python main.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Options disponibles

| Option        | Description                                                    |
|---------------|----------------------------------------------------------------|
| `--audio`     | Télécharge uniquement l’audio                                  |
| `--format`    | Spécifie le format de sortie (`mp4`, `mkv`, `mp3`, etc.)       |
| `--output`    | Dossier de destination (défaut : `~/Downloads/`)               |
| `--playlist`  | Télécharge toute la playlist si l’URL en contient une          |
| `--update`    | Force la mise à jour de `yt-dlp`                               |

### Exemples

- 🎵 Télécharger une vidéo YouTube en MP3 :

```bash
python main.py "https://www.youtube.com/watch?v=..." --audio --format mp3
```

- 📁 Spécifier un dossier personnalisé :

```bash
python main.py "https://..." --output "/chemin/vers/mon/dossier"
```

- 📺 Télécharger une playlist entière :

```bash
python main.py "https://www.youtube.com/playlist?list=..." --playlist
```

- 🔄 Mettre à jour `yt-dlp` :

```bash
python main.py --update
```

## 🧪 Développement

- Le fichier principal est `main.py`
- Toutes les dépendances sont listées dans `requirements.txt`
- Tu peux créer un fichier `.env` pour des variables personnalisées (facultatif)

## 🪤 Astuce : créer un alias Bash

Ajoute dans ton `~/.bashrc` ou `~/.zshrc` :

```bash
alias dlvid="python /chemin/vers/video-dl/main.py"
```

Et utilise simplement :

```bash
dlvid "https://www.youtube.com/watch?v=..."
```

---

## ❓ FAQ

**Q : Pourquoi `yt-dlp` au lieu de `youtube-dl` ?**  
R : Parce qu’il est **plus rapide, plus maintenu, et compatible avec plus de sites**.

**Q : Le téléchargement échoue ?**  
R : Lance avec `--update` pour t'assurer d'avoir la dernière version de `yt-dlp`.

**Q : Les formats ne marchent pas ?**  
R : Vérifie que `ffmpeg` est bien installé (`brew install ffmpeg` ou `sudo apt install ffmpeg`).

**Q : Comment contourner une vidéo géobloquée ?**  
R : Tu peux ajouter l’option `--proxy` avec un proxy/VPN configuré (support en cours d’intégration).

---

## 📜 Licence

MIT © iamqtn. Utilisation libre.
