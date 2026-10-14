import telebot
from telebot import types
import random
import time

# Tokeningiz o'rnatildi
TOKEN = "8846680614:AAHDmr4C5sLsGan0MTprkx-TCgFCdwKtwN4"
bot = telebot.TeleBot(TOKEN)

users_data = {}
flood_control = {}

def get_user(chat_id):
    if chat_id not in users_data:
        users_data[chat_id] = {
            "tokens": 100,
            "squad": {
                "LW": None, "ST": None, "RW": None,
                "CM1": None, "CM2": None, "CDM": None,
                "LB": None, "CB1": None, "CB2": None, "RB": None,
                "GK": None
            },
            "inventory": []
        }
    return users_data[chat_id]

PLAYERS = [
    {"name": "Kylian Mbappé", "pos": "ST", "rating": 94, "rarity": "Icon/TOTY"},
    {"name": "Erling Haaland", "pos": "ST", "rating": 93, "rarity": "Icon/TOTY"},
    {"name": "Lionel Messi", "pos": "RW", "rating": 93, "rarity": "Icon/TOTY"},
    {"name": "Vinícius Jr.", "pos": "LW", "rating": 92, "rarity": "Elite"},
    {"name": "Kevin De Bruyne", "pos": "CM", "rating": 91, "rarity": "Elite"},
    {"name": "Jude Bellingham", "pos": "CM", "rating": 90, "rarity": "Elite"},
    {"name": "Rodri", "pos": "CDM", "rating": 91, "rarity": "Elite"},
    {"name": "Theo Hernández", "pos": "LB", "rating": 88, "rarity": "Gold"},
    {"name": "Virgil van Dijk", "pos": "CB", "rating": 90, "rarity": "Elite"},
    {"name": "William Saliba", "pos": "CB", "rating": 87, "rarity": "Gold"},
    {"name": "Achraf Hakimi", "pos": "RB", "rating": 87, "rarity": "Gold"},
    {"name": "Thibaut Courtois", "pos": "GK", "rating": 90, "rarity": "Elite"}
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    current_time = time.time()
    if chat_id in flood_control and current_time - flood_control[chat_id] < 1.5:
        bot.send_message(chat_id, "⚠️ Juda tez-tez yozayapsiz! Biroz kuting.")
        return
    flood_control[chat_id] = current_time

    user = get_user(chat_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📦 Pack ochish"), types.KeyboardButton("⚽ Tarkib (4-3-3)"))
    markup.add(types.KeyboardButton("💰 Balans"), types.KeyboardButton("🛒 Market"))

    bot.send_message(
        chat_id, 
        "⚽ **FC Mobile Pack Opener Botiga xush kelibsiz!**\n\n"
        "Paketlar oching, kuchli o'yinchilarni yig'ing va 4-3-3 tarkibingizni tuzing!", 
        reply_markup=markup, 
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text
    user = get_user(chat_id)

    current_time = time.time()
    if chat_id in flood_control and current_time - flood_control[chat_id] < 1.0:
        return
    flood_control[chat_id] = current_time

    if text == "📦 Pack ochish":
        if user["tokens"] < 20:
            bot.send_message(chat_id, "❌ Paket ochish uchun tokenlaringiz yetarli emas! (Kerak: 20 token)")
            return
        
        user["tokens"] -= 20
        player = random.choice(PLAYERS)
        user["inventory"].append(player)

        bot.send_message(
            chat_id, 
            f"🎉 **Tabriklaymiz! Siz yangi o'yinchi oldingiz:**\n\n"
            f"👤 Ismi: **{player['name']}**\n"
            f"📌 Pozitsiyasi: `{player['pos']}`\n"
            f"⭐ Reyting: **{player['rating']}**\n"
            f"💎 Kamyobligi: _{player['rarity']}_\n\n"
            f"📉 Qolgan tokenlar: {user['tokens']} ta",
            parse_mode="Markdown"
        )

    elif text == "⚽ Tarkib (4-3-3)":
        squad = user["squad"]
        squad_text = (
            "⚽ **Sizning 4-3-3 Tarkibingiz:**\n\n"
            f"LW: {squad['LW']['name'] if squad['LW'] else 'Boʻsh'} | ST: {squad['ST']['name'] if squad['ST'] else 'Boʻsh'} | RW: {squad['RW']['name'] if squad['RW'] else 'Boʻsh'}\n"
            f"CM1: {squad['CM1']['name'] if squad['CM1'] else 'Boʻsh'} | CDM: {squad['CDM']['name'] if squad['CDM'] else 'Boʻsh'} | CM2: {squad['CM2']['name'] if squad['CM2'] else 'Boʻsh'}\n"
            f"LB: {squad['LB']['name'] if squad['LB'] else 'Boʻsh'} | CB1: {squad['CB1']['name'] if squad['CB1'] else 'Boʻsh'} | CB2: {squad['CB2']['name'] if squad['CB2'] else 'Boʻsh'} | RB: {squad['RB']['name'] if squad['RB'] else 'Boʻsh'}\n"
            f"GK: {squad['GK']['name'] if squad['GK'] else 'Boʻsh'}"
        )
        bot.send_message(chat_id, squad_text, parse_mode="Markdown")

    elif text == "💰 Balans":
        bot.send_message(chat_id, f"💎 Sizning balansingiz: **{user['tokens']} token**", parse_mode="Markdown")

    elif text == "🛒 Market":
        bot.send_message(chat_id, "🛒 Market tez kunda ishga tushadi! Hozircha faqat paket ochib o'yinchilarni yig'ing.")

if __name__ == "__main__":
    print("Bot ishga tushdi...")
    bot.infinity_polling()

