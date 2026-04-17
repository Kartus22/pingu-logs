<img width="1024" height="559" alt="7e4a01c5-3d1e-44d6-b650-9e57aa88a082" src="https://github.com/user-attachments/assets/1594de5b-87d6-49bc-bbbf-c6f3dc4f57f6" />

Markdown

# 🐧 Pingu-Logs | Advanced Discord Activity, Name Tracking & Auto-Clean Bot

A lightweight, highly reliable, and **bilingual** (English/German) Discord bot designed to keep your server logs clean, compact, and informative. 

Pingu-Logs tracks voice channel activity, member joins/leaves, and features a **smart name-history system** that remembers previous usernames. To keep your log channel tidy and stay within Discord's message limits, it performs a complete automated channel wipe every 13 days.

## ✨ Features

* **🌍 Multi-Language Support:** Starts in English by default, but can be instantly switched to German via a simple command.
* **🕵️‍♂️ Smart Name Tracking:** Logs global profile name changes and local server nickname changes.
* **🧠 Multi-Stage Memory:** Remembers the last 3 previous names/nicknames of a user so admins always know who is who.
* **🎧 Voice Tracking:** Logs whenever a user joins or leaves a voice channel and calculates the exact duration of their session.
* **📱 Compact UI:** Uses a modern, one-line formatting style with emojis to keep the log channel easily readable and prevent spam.
* **🧹 Smart Auto-Clean:** Automatically performs a complete purge of the log channel every 13 days. Uses persistent file saving so the timer doesn't reset even if the bot restarts. 
* **💾 Full Persistence:** Safely stores language settings, voice sessions, and name histories in local JSON files.

### Example Log Output
```text
📥 14:00 | Server Join: NewUser
🕒 14:05 | ✅ Joined: NewUser ➔ General Voice
🕒 15:30 | ❌ Left: NewUser ➔ General Voice [⏳ 1h 25m]
📝 16:00 | [Main Profile Name] NewUser ➔ CoolUser (Previously: OldUser1, OldUser2)

🚀 Installation & Setup
1. Prerequisites

    Python 3.8 or higher

    A Discord Bot Token from the Discord Developer Portal

2. Required Intents (Crucial!)

In the Discord Developer Portal, navigate to your Bot settings and enable the following Privileged Gateway Intents:

    Presence Intent (needed to track name updates)

    Server Members Intent (needed to track joins/leaves)

    Message Content Intent (needed for commands)

3. Setup

Clone this repository or download the files:
Bash

git clone [https://github.com/Kartus22/pingu-logs.git](https://github.com/Kartus22/pingu-logs.git)
cd pingu-logs

4. Install Dependencies
Bash

pip install discord.py

5. Configuration

Open logs.py in your text editor and update the top configuration section:

    TOKEN: Paste your Discord Bot Token here. Never share this publicly!

    CHANNEL_ID: Replace with the ID of the channel where logs should be posted and cleaned.

🛠 Usage

Simply run the bot:
Bash

python3 logs.py

Note: The bot will automatically create necessary .json and .txt files on its first run. You do not need to create them manually.
💻 Commands
Command	Required Permission	Description
§language eng	Manage Server	Switches all bot outputs to English.
§language ger	Manage Server	Switches all bot outputs to German.
§clear	Manage Messages	Manually deletes the last 1000 messages in the channel.
📁 File Structure (Auto-Generated)

    logs.py: The main bot script.

    settings.json: Remembers your chosen language.

    name_history.json: Stores the previous 3 names of server members.

    voice_sessions.json: Temporarily stores active voice sessions to calculate duration.

    last_clean.txt: Stores the last auto-cleanup timestamp.

🛡 Required Discord Permissions

Make sure your bot's role has the following permissions in your dedicated log channel:

    View Channel

    Send Messages

    Manage Messages (Required for Purge / Auto-Clean)

    Read Message History

📝 License

This project is open-source and free to use (MIT License).
```
<img width="1218" height="453" alt="pingubotlog" src="https://github.com/user-attachments/assets/28436748-987e-47e8-ac0b-3c66e9a6dc94" />

