import discord
from discord.ext import tasks
from datetime import datetime, timedelta
import os
import json

# --- KONFIGURATION ---
TOKEN = 'YOUR_BOT_TOKEN_HERE'
CHANNEL_ID = 1494018148704456704

# Deine Musikbot-IDs
IGNORE_IDS = [1481973009454727319, 1493317338320076870, 1488612071120830514, 1493194051170865152, 1494823684337041499]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIMESTAMP_FILE = os.path.join(BASE_DIR, "last_clean.txt")
VOICE_FILE = os.path.join(BASE_DIR, "voice_sessions.json") 
HISTORY_FILE = os.path.join(BASE_DIR, "name_history.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

# --- SPRACH-MODULE ---
LANGUAGES = {
    "ger": {
        "previously": "Zuvor",
        "join": "Beitritt",
        "leave": "Verlassen",
        "server_join": "Server-Beitritt",
        "server_leave": "Server-Verlassen",
        "change_label": "🔄 Änderung:",
        "change_main": "Hat seinen Hauptprofilnamen geändert",
        "change_serv": "Hat seinen Servernamen geändert",
        "clean_msg": "Hausputz: {} Nachrichten entfernt.",
        "status_msg": "Noch {}T {}Std bis zur Reinigung.",
        "lang_set": "Sprache auf **Deutsch** umgestellt.",
        "backup_info": "🤖 **Hausputz beendet:** Um die Übersicht zu wahren, wurden alle Nachrichten gelöscht. Die letzten 30 Log-Einträge wurden vorab gesichert und hier wiederhergestellt.\n📅 **Nächster Hausputz am: {}**"
    },
    "eng": {
        "previously": "Previously",
        "join": "Joined",
        "leave": "Left",
        "server_join": "Server Join",
        "server_leave": "Server Leave",
        "change_label": "🔄 Change:",
        "change_main": "Changed their main profile name",
        "change_serv": "Changed their server nickname",
        "clean_msg": "Auto-Clean: {} messages removed.",
        "status_msg": "{}d {}h remaining until clean.",
        "lang_set": "Language set to **English**.",
        "backup_info": "🤖 **Clean-up finished:** Channel was cleared for readability. The last 30 log entries were backed up and restored below.\n📅 **Next clean-up on: {}**"
    }
}

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# --- HILFSFUNKTIONEN ---
def get_lang():
    if not os.path.exists(SETTINGS_FILE): return "eng" 
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f).get("lang", "eng")
    except: return "eng"

def set_lang(lang_code):
    with open(SETTINGS_FILE, "w") as f:
        json.dump({"lang": lang_code}, f)

def load_voice_sessions():
    if not os.path.exists(VOICE_FILE): return {}
    try:
        with open(VOICE_FILE, "r") as f:
            return json.load(f)
    except: return {}

def save_voice_sessions(data):
    with open(VOICE_FILE, "w") as f:
        json.dump(data, f)

def load_history():
    if not os.path.exists(HISTORY_FILE): return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except: return {}

def save_history(data):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_previous_names(user_id, current_old_name):
    history = load_history()
    u_id = str(user_id)
    known_names = history.get(u_id, [])
    if isinstance(known_names, str): known_names = [known_names]
    previous_names_to_return = known_names.copy()
    if not known_names or known_names[-1] != current_old_name:
        known_names.append(current_old_name)
    if len(known_names) > 3: known_names = known_names[-3:]
    history[u_id] = known_names
    save_history(history)
    previous_names_to_return.reverse()
    return previous_names_to_return

def get_now():
    return datetime.now().strftime("%d.%m.%y %H:%M")

def update_timestamp(dt):
    try:
        with open(TIMESTAMP_FILE, "w", encoding="utf-8") as f:
            f.write(dt.strftime("%Y-%m-%d %H:%M:%S"))
            f.flush()
            os.fsync(f.fileno())
        return True
    except Exception as e:
        print(f"[{get_now()}] ❌ Zeitstempel-Fehler: {e}")
        return False

def print_clean_status():
    now = datetime.now()
    if not os.path.exists(TIMESTAMP_FILE): return
    with open(TIMESTAMP_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        try:
            last_clean = datetime.strptime(content, "%Y-%m-%d %H:%M:%S")
        except: return
    vergangene_zeit = now - last_clean
    if vergangene_zeit <= timedelta(days=13):
        verbleibend = timedelta(days=13) - vergangene_zeit
        l = LANGUAGES[get_lang()]
        print(f"[{get_now()}] ℹ️ Status: {l['status_msg'].format(verbleibend.days, verbleibend.seconds // 3600)}")

async def safe_send(channel, text):
    try:
        msg = await channel.send(text)
        return msg
    except: return None

# --- AUTOMATISCHER HAUSPUTZ MIT PRÄZISEM EMOJI-BACKUP ---
@tasks.loop(hours=1)
async def smart_clean_service():
    await client.wait_until_ready()
    ch = client.get_channel(CHANNEL_ID)
    if not ch: return
    now = datetime.now()
    if not os.path.exists(TIMESTAMP_FILE):
        update_timestamp(now)
        return
    with open(TIMESTAMP_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        try: last_clean = datetime.strptime(content, "%Y-%m-%d %H:%M:%S")
        except:
            update_timestamp(now)
            return
    
    if (now - last_clean) > timedelta(days=13):
        print(f"[{get_now()}] 🤖 13 Tage erreicht. Starte Reinigung mit Emoji-Backup...")
        try:
            backup = []
            # Exakte Symbole für die Logs
            log_symbols = ["📝", "🏷️", "🕒", "✅", "❌", "📥", "📤"]
            
            async for msg in ch.history(limit=300):
                # Wir sichern die Nachricht, wenn sie eines der Symbole enthält
                if any(sym in msg.content for sym in log_symbols):
                    # Keine Befehle oder Bot-Meldungen mitsichern
                    if not msg.content.startswith('§') and not msg.content.startswith('🤖'):
                        backup.append(msg.content)
                
                if len(backup) >= 30:
                    break
            
            backup.reverse()

            # Kanal leeren
            deleted = await ch.purge(limit=None)
            
            # Zeitstempel auf JETZT setzen
            update_timestamp(now)

            # Wiederherstellen
            if backup:
                for entry in backup:
                    await ch.send(entry)
            
            l = LANGUAGES[get_lang()]
            next_clean_date = (now + timedelta(days=13)).strftime("%d.%m.%Y %H:%M")
            await safe_send(ch, l['backup_info'].format(next_clean_date))
            
            print(f"[{get_now()}] ✅ Reinigung erledigt. {len(deleted)} gelöscht, {len(backup)} wiederhergestellt.")

        except Exception as e:
            print(f"[{get_now()}] ❌ Fehler beim Putzen: {e}")
    else:
        print_clean_status()

# --- EVENTS ---
@client.event
async def on_ready():
    print(f'=== {client.user} IST ONLINE ===')
    # Den direkten Aufruf hier haben wir entfernt, da der loop das sofort übernimmt.
    if not smart_clean_service.is_running():
        smart_clean_service.start()

@client.event
async def on_message(message):
    if message.author.id in IGNORE_IDS or message.author == client.user or message.guild is None:
        return
    content = message.content.lower()
    if content.startswith('§language'):
        if message.author.guild_permissions.manage_guild:
            parts = content.split()
            if len(parts) > 1 and parts[1] in ["ger", "eng"]:
                set_lang(parts[1])
                l = LANGUAGES[parts[1]]
                await safe_send(message.channel, f"✅ {l['lang_set']}")
    if content == '§clear':
        if message.author.guild_permissions.manage_messages:
            try:
                deleted = await message.channel.purge(limit=1000)
                l = LANGUAGES[get_lang()]
                msg = await safe_send(message.channel, f'🧹 **{l["clean_msg"].format(len(deleted))}**')
                if msg: await msg.delete(delay=10)
            except: pass

# --- LOG-EVENTS ---
@client.event
async def on_user_update(before, after):
    if before.id in IGNORE_IDS: return
    if before.name != after.name or before.display_name != after.display_name:
        ch = client.get_channel(CHANNEL_ID)
        if ch:
            l = LANGUAGES[get_lang()]
            alt = before.display_name if before.display_name else before.name
            neu = after.display_name if after.display_name else after.name
            prev = get_previous_names(before.id, alt)
            info = f" ({l['previously']}: {', '.join(prev)})" if prev else ""
            await safe_send(ch, f"📝 `{get_now()}` | **{l['change_label']}** {alt} ➔ **{neu}**{info} **({l['change_main']})**")

@client.event
async def on_member_update(before, after):
    if before.id in IGNORE_IDS: return
    if before.nick != after.nick:
        ch = client.get_channel(CHANNEL_ID)
        if ch:
            l = LANGUAGES[get_lang()]
            alt = before.nick if before.nick else before.name
            neu = after.nick if after.nick else after.name
            prev = get_previous_names(f"{before.id}_nick", alt)
            info = f" ({l['previously']}: {', '.join(prev)})" if prev else ""
            await safe_send(ch, f"🏷️ `{get_now()}` | **{l['change_label']}** {alt} ➔ **{neu}**{info} **({l['change_serv']})**")

@client.event
async def on_voice_state_update(member, before, after):
    if member.id in IGNORE_IDS: return
    ch = client.get_channel(CHANNEL_ID)
    if not ch: return
    l = LANGUAGES[get_lang()]
    now = datetime.now()
    sessions = load_voice_sessions()
    user_id = str(member.id)

    if before.channel is None and after.channel is not None:
        sessions[user_id] = now.timestamp()
        save_voice_sessions(sessions)
        await safe_send(ch, f"🕒 `{get_now()}` | ✅ **{l['join']}:** {member.display_name} ➔ {after.channel.name}")

    elif before.channel is not None and after.channel is None:
        info_str = ""
        if user_id in sessions:
            start_ts = sessions.pop(user_id)
            save_voice_sessions(sessions)
            
            start_dt = datetime.fromtimestamp(start_ts)
            end_dt = datetime.now()
            diff = end_dt - start_dt
            
            s_val = int(diff.total_seconds()) # Umbenannt in s_val
            h, r = divmod(s_val, 3600)
            m, sec = divmod(r, 60) # Umbenannt in sec
            
            if h > 0: dur = f"{h}h {m}m"
            elif m > 0: dur = f"{m}m {sec}s"
            else: dur = f"{sec}s"
            
            # HIER AUCH: Nur %H:%M (Stunden:Minuten)
            info_str = f" [{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')} | ⏱️ {dur}]"

        await safe_send(ch, f"🕒 `{get_now()}` | ❌ **{l['leave']}:** {member.display_name} ➔ {before.channel.name}{info_str}")

@client.event
async def on_member_join(member):
    if member.id in IGNORE_IDS: return
    ch = client.get_channel(CHANNEL_ID)
    if ch:
        l = LANGUAGES[get_lang()]
        # Hier display_name für den Server-Namen nutzen
        await safe_send(ch, f"📥 `{get_now()}` | **{l['server_join']}:** {member.display_name}")

@client.event
async def on_member_remove(member):
    if member.id in IGNORE_IDS: return
    ch = client.get_channel(CHANNEL_ID)
    if ch:
        l = LANGUAGES[get_lang()]
        # WICHTIG: Hier l['server_leave'] (oder wie dein Label für Verlassen heißt) nutzen
        # In deinem Sprach-Modul heißt es wahrscheinlich "server_leave"
        await safe_send(ch, f"📤 `{get_now()}` | **{l.get('server_leave', 'Verlassen')}:** {member.display_name}")

client.run(TOKEN)