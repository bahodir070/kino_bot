import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# TOKEN - Railway'da env dan o'qiladi
TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Kanallar ro'yxati (o'z kanallaringiz bilan almashtiring!)
KANALLAR = [
    {"username": "@kanal1", "name": "1-kanal", "link": "https://t.me/kanal1"},
    {"username": "@kanal2", "name": "2-kanal", "link": "https://t.me/kanal2"},
    {"username": "@kanal3", "name": "3-kanal", "link": "https://t.me/kanal3"},
    {"username": "@kanal4", "name": "4-kanal", "link": "https://t.me/kanal4"},
    {"username": "@kanal5", "name": "5-kanal", "link": "https://t.me/kanal5"},
]

# Kino kodlari
KINOLAR = {
    "KINO001": "https://t.me/your_channel/video1",
    "KINO002": "https://t.me/your_channel/video2",
}

# Obunani tekshirish
def tekshir_obuna(user_id):
    tekshirilmagan = []
    for kanal in KANALLAR:
        try:
            holat = bot.get_chat_member(kanal["username"], user_id).status
            if holat in ['left', 'kicked']:
                tekshirilmagan.append(kanal)
        except:
            tekshirilmagan.append(kanal)
    return tekshirilmagan

# Tugmalar
def obuna_tugmalari(kanallar):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for kanal in kanallar:
        keyboard.add(InlineKeyboardButton(f"➕ {kanal['name']}", url=kanal['link']))
    keyboard.add(InlineKeyboardButton("✅ Tekshirish", callback_data="tekshir"))
    return keyboard

def asosiy_tugmalar():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🎬 Kod kiritish", callback_data="kod"),
        InlineKeyboardButton("📋 Kanallar", callback_data="kanallar")
    )
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    text = f"🎬 Assalomu alaykum {message.from_user.first_name}!\n\nKino kodlari botiga xush kelibsiz!"
    
    tekshirilmagan = tekshir_obuna(user_id)
    if tekshirilmagan:
        bot.send_message(message.chat.id, text, reply_markup=obuna_tugmalari(tekshirilmagan))
    else:
        bot.send_message(message.chat.id, "✅ Obuna tasdiqlandi!\n\n🎬 Kod kiriting: /code KINO001", reply_markup=asosiy_tugmalar())

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.from_user.id
    
    if call.data == "tekshir":
        tekshirilmagan = tekshir_obuna(user_id)
        if tekshirilmagan:
            bot.edit_message_text("❌ Kanallarga obuna bo'ling:", call.message.chat.id, call.message.message_id, reply_markup=obuna_tugmalari(tekshirilmagan))
        else:
            bot.edit_message_text("✅ Obuna tasdiqlandi!", call.message.chat.id, call.message.message_id, reply_markup=asosiy_tugmalar())
    elif call.data == "kod":
        bot.send_message(call.message.chat.id, "🎬 Kodni kiriting:\nMisol: /code KINO001")
    elif call.data == "kanallar":
        text = "📋 Kanallar:\n\n"
        for i, k in enumerate(KANALLAR, 1):
            text += f"{i}. {k['name']}\n"
        bot.send_message(call.message.chat.id, text)
    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['code'])
def kod(message):
    user_id = message.from_user.id
    tekshirilmagan = tekshir_obuna(user_id)
    if tekshirilmagan:
        bot.reply_to(message, "❌ Avval kanallarga obuna bo'ling!", reply_markup=obuna_tugmalari(tekshirilmagan))
        return
    try:
        kod = message.text.split()[1].upper()
    except:
        bot.reply_to(message, "❌ Format: /code KINO001")
        return
    if kod in KINOLAR:
        bot.reply_to(message, f"✅ Kod qabul qilindi!\n\n🎬 Kino: {KINOLAR[kod]}")
    else:
        bot.reply_to(message, "❌ Xato kod!")

print("🎬 Bot ishga tushdi...")
bot.infinity_polling()