# Music Bot

A simple and functional Discord music bot that uses `yt-dlp` for searching and playing music from YouTube. It features a selection menu for search results and a basic queue system.

### Features
* **Search & Select:** Uses a Discord UI Select Menu to choose between the top 5 search results.
* **Queue System:** Automatically plays the next song in the queue.
* **Standard Controls:** Includes play, pause, resume, skip, and stop commands.
* **Lightweight:** Minimal dependencies, focused on performance.

### How to Setup
1. **FFmpeg:** Make sure you have FFmpeg installed on your system or placed in the bot's folder.
2. **Install Dependencies:**
   ```bash
   pip install discord.py yt-dlp
Configuration: Open bot.py and replace the TOKEN with your own bot token.

Run:

Bash
python bot.py
Commands
.play <song name> - Search and select a song to play.

.pause - Pause the current track.

.resume - Resume the paused track.

.skip - Skip the current song.

.stop - Clear the queue and disconnect from the voice channel.

Instagram:slippinkuzey
