<img width="1024" height="559" alt="7e4a01c5-3d1e-44d6-b650-9e57aa88a082" src="https://github.com/user-attachments/assets/1594de5b-87d6-49bc-bbbf-c6f3dc4f57f6" />


# 🐧 Pingu-Logs | Discord Activity & Auto-Clean Bot

A lightweight, reliable Discord bot designed to log voice channel activity, member joins/leaves, and perform a **full channel wipe** every 13 days to stay within Discord's message limits and keep things tidy.

## ✨ Features

* **Voice Tracking:** Logs whenever a user joins or leaves a voice channel.
* **Member Logs:** Tracks new members joining or leaving the server.
* **Smart Auto-Clean:** Automatically performs a **complete purge** of the log channel every 13 days. It uses a persistent `last_clean.txt` file, so the timer doesn't reset even if the bot restarts.
* **Manual Clear:** Admins can use `§clear` to wipe the last 1000 messages manually.
* **Persistence:** Uses absolute path handling and disk-syncing to ensure your timestamps are never lost.

---

## 🚀 Installation

### 1. Prerequisites
* Python 3.8 or higher
* A Discord Bot Token ([Discord Developer Portal](https://discord.com/developers/applications))

### 2. Setup
Clone this repository or download the files:

```bash
git clone [https://github.com/Kartus22/pingu-logs.git](https://github.com/Kartus22/pingu-logs.git)
cd pingu-logs

3. Install Dependencies
Bash

pip install discord.py

4. Configuration

Open logs.py and fill in your details:

    TOKEN: Your Discord Bot Token.

    CHANNEL_ID: The ID of the channel where logs should be posted and cleaned.

🛠 Usage

Simply run the bot:
Bash

python3 logs.py

Commands
Command	Permission	Description
§clear	Manage Messages	Deletes the last 1000 messages in the current channel.
📁 File Structure

    logs.py: The main bot script.

    last_clean.txt: Stores the last cleanup timestamp (Unix/Linux LF format).

    requirements.txt: List of necessary Python packages.

🛡 Permissions

Make sure your bot has a role with the following permissions in your log channel:

    View Channel

    Send Messages

    Manage Messages (Required for Purge)

    Read Message History

💡 Pro-Tip for Linux Users

If you are editing the configuration via FTP/Filezilla, ensure your editor uses LF (Unix) line endings to prevent formatting errors with the timestamp file.
📝 License

This project is open-source and free to use (MIT License).
