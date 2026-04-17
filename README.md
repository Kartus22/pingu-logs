<img width="1024" height="559" alt="7e4a01c5-3d1e-44d6-b650-9e57aa88a082" src="https://github.com/user-attachments/assets/1594de5b-87d6-49bc-bbbf-c6f3dc4f57f6" />

# 🐧 Pingu-Logs | Advanced Discord Activity, Name Tracking & Auto-Clean Bot

A lightweight, highly reliable, and **bilingual** (English/German) Discord bot designed to keep your server logs clean, compact, and informative. 

Pingu-Logs tracks voice channel activity, member joins/leaves, and features a **smart name-history system** that remembers previous usernames. To keep your log channel tidy and stay within Discord's message limits, it performs a complete automated channel wipe every 13 days.

## ✨ Features

* **🌍 Multi-Language Support:** Starts in English by default, but can be instantly switched to German via a simple command.
* **🕵️‍♂️ Smart Name Tracking:** Logs global profile name changes and local server nickname changes.
* **🧠 Multi-Stage Memory:** Remembers the last 3 previous names/nicknames of a user so admins always know who is who.
* **🎧 Voice Tracking:** Logs whenever a user joins or leaves a voice channel and calculates the exact duration of their session.
* **🧹 Smart Auto-Clean & Backup:** Automatically performs a complete purge of the log channel every 13 days. 
* **💾 Log Preservation:** Before cleaning, the bot secures the **last 30 log entries** and restores them after the wipe, so the history is never completely lost.
* **📅 Transparency:** After every cleanup, the bot posts a notification including the **exact date and time of the next scheduled houseputz**.
* **💾 Full Persistence:** Safely stores language settings, voice sessions, and name histories in local JSON files.

## Example Log Output

📥 `14:00` | **Server-Beitritt:** NewUser
🕒 `14:05` | ✅ **Beitritt:** NewUser ➔ General Voice
🕒 `15:30` | ❌ **Verlassen:** NewUser ➔ General Voice [⏱️ 1h 25m]
📝 `16:00` | 🔄 **Änderung:** NewUser ➔ CoolUser (Zuvor: OldUser1) **(Hat seinen Hauptprofilnamen geändert)**

---

## 🚀 Installation & Setup

### 1. Prerequisites
* Python 3.8 or higher
* A Discord Bot Token from the [Discord Developer Portal](https://discord.com/developers/applications)

### 2. Required Intents (Crucial!)
Enable the following **Privileged Gateway Intents** in your Bot settings:
* **Presence Intent** (to track name updates)
* **Server Members Intent** (to track joins/leaves)
* **Message Content Intent** (needed for commands)

### 3. Setup
```bash
git clone [https://github.com/Kartus22/pingu-logs.git](https://github.com/Kartus22/pingu-logs.git)
cd pingu-logs
pip install discord.py
4. ConfigurationOpen logs.py and update the configuration section:TOKEN: Paste your Discord Bot Token here.CHANNEL_ID: The ID of the channel where logs should be posted and cleaned.💻 CommandsCommandRequired PermissionDescription§language engManage ServerSwitches all bot outputs to English.§language gerManage ServerSwitches all bot outputs to German.§clearManage MessagesManually deletes the last 1000 messages in the channel.📁 File Structure (Auto-Generated)logs.py: The main bot script.settings.json: Stores your chosen language.name_history.json: Stores the previous 3 names of server members.voice_sessions.json: Temporarily stores active voice sessions.last_clean.txt: Stores the last auto-cleanup timestamp.🛡 Required Discord PermissionsEnsure the bot's role has these permissions in the log channel:View ChannelSend MessagesManage Messages (Required for Auto-Clean)Read Message History📝 LicenseThis project is open-source and free to use (MIT License).
```
<img width="1218" height="453" alt="pingubotlog" src="https://github.com/user-attachments/assets/28436748-987e-47e8-ac0b-3c66e9a6dc94" />

