import discord
from discord.ext import tasks
from datetime import datetime, timedelta
import os

# --- CONFIGURATION ---
TOKEN = 'YOUR_BOT_TOKEN_HERE'
CHANNEL_ID = 000000000000000000

# Get absolute path to prevent folder confusion
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TIMESTAMP_FILE = os.path.join(BASE_DIR, "last_clean.txt")

intents = discord.Intents.all()
client = discord.Client(intents=intents)

def get_now():
    return datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

def update_timestamp(dt):
    """Force-writes the timestamp to the file and ensures it hits the disk."""
    try:
        with open(TIMESTAMP_FILE, "w", encoding="utf-8") as f:
            f.write(dt.strftime("%Y-%m-%d %H:%M:%S"))
            f.flush()
            os.fsync(f.fileno())
        print(f"[{get_now()}] 💾 File updated successfully to {dt.year}")
        return True
    except Exception as e:
        print(f"[{get_now()}] ❌ CRITICAL: Could not write to file: {e}")
        return False

@tasks.loop(hours=1) # Keeping 10s for your test
async def smart_clean_service():
    await client.wait_until_ready()
    ch = client.get_channel(CHANNEL_ID)
    if not ch: return

    now = datetime.now()
    
    if not os.path.exists(TIMESTAMP_FILE):
        update_timestamp(now)
        print(f"[{get_now()}] 📝 Created new timestamp file.")
        return

    with open(TIMESTAMP_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        try:
            last_clean = datetime.strptime(content, "%Y-%m-%d %H:%M:%S")
        except:
            print(f"[{get_now()}] ⚠️ Formatting error in file. Resetting...")
            update_timestamp(now)
            return

    elapsed = now - last_clean
    
    if elapsed > timedelta(days=13):
        print(f"[{get_now()}] 🤖 13 days reached (Diff: {elapsed.days} days). Cleaning...")
        try:
            deleted = await ch.purge(limit=None)
            
            # Update the file immediately
            if update_timestamp(now):
                temp_msg = await ch.send(f"🤖 **Auto-Clean:** {len(deleted)} messages removed.")
                await temp_msg.delete(delay=10)
            else:
                print(f"[{get_now()}] ❌ Purge done, but timestamp update FAILED!")
                
        except Exception as e:
            print(f"[{get_now()}] ❌ Error during purge: {e}")
    else:
        if now.minute < 30: 
            remaining = timedelta(days=13) - elapsed
            print(f"[{get_now()}] ℹ️ Status: {remaining.days}d {remaining.seconds // 3600}h remaining.")

@client.event
async def on_ready():
    print(f'=== {client.user} IS ONLINE ===')
    print(f'Looking for file at: {TIMESTAMP_FILE}')
    
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, "r") as f:
            print(f"Current file content: '{f.read().strip()}'")

    if not smart_clean_service.is_running():
        smart_clean_service.start()

# ... (Rest of your events like on_message, on_voice_state_update) ...

client.run(TOKEN)
