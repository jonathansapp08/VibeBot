# VibeBot
Discord bot that plays music.

With the loss of our favorite music bots, VibeBot was created to fill that void.

## Supported sources

VibeBot supports the following sources:

* YouTube
* Spotify (Work in Progress)
* SoundCloud (Work in Progress)

---

## Setup

1. Create a bot on [Discord's Developer Portal](https://discord.com/developers/applications). For step by step instructions you can use [this](https://realpython.com/how-to-make-a-discord-bot-python/) as a reference. You'll need the bot created/added to your guild and the authentication token ready. 

2. Clone the repository
```
git clone https://github.com/jonathansapp08/VibeBot.git
```

3. In the console change your directory to the folder you just cloned and install the dependencies
```
cd VibeBot/
pip install -r requirements.txt
```

4. Download [FFmpeg](https://www.ffmpeg.org/). Optionally you can install FFmpep from the console.

macOS
```
brew install ffmpeg
```

Ubuntu
```
sudo apt install ffmpeg
```

5. Export token for vibe.py. Optionally you could use and .env file but that is not discussed here.
```
export token='<TOKEN_FOR_DISCORD_BOT>'
```

6. Run vibe.py.
```
python vibe.py
``` 

---
## Usage
Once the script is running you are free to begin using VibeBot! For a list of commands type:

```
!help
```
