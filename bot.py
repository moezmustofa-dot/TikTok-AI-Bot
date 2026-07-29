import os
import telebot
from openai import OpenAI

# Ambil token dari Environment Variables (aman dan tidak terekspos)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# 1. Perintah /start (Menyapa Anda di Telegram)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo Boss! Saya CEO AI TikTok Affiliate Anda. Ketik /riset untuk mencari ide produk hari ini, atau /bantuan untuk melihat daftar perintah.")

# 2. Perintah /bantuan
@bot.message_handler(commands=['bantuan'])
def send_help(message):
    help_text = (
        "🤖 **Daftar Perintah Bot Anda:**\n\n"
        "/riset - Meminta AI mencarikan ide produk tren TikTok.\n"
        "/naskah [nama produk] - Membuat skrip video pendek TikTok.\n"
        "/laporan - Cek status ringkasan harian."
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

# 3. Perintah /riset (Agen Market Intelligence)
@bot.message_handler(commands=['riset'])
def market_research(message):
    bot.reply_to(message, "🔍 Sedang memindai tren TikTok Shop... Mohon tunggu sebentar.")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Anda adalah pakar riset pasar TikTok Affiliate."},
                {"role": "user", "content": "Berikan 1 rekomendasi produk fiktif/nyata yang sedang tren untuk kategori Home & Living di TikTok, lengkap dengan perkiraan komisi afiliasinya dan alasan kenapa produk ini laku."}
            ]
        )
        result = response.choices[0].message.content
        bot.reply_to(message, f"📊 **Hasil Riset Hari Ini:**\n\n{result}", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Gagal meriset: {str(e)}")

# 4. Perintah /naskah [Nama Produk] (Agen Copywriting)
@bot.message_handler(commands=['naskah'])
def generate_script(message):
    # Mengambil teks setelah perintah /naskah
    product_name = message.text.replace('/naskah', '').strip()
    
    if not product_name:
        bot.reply_to(message, "⚠️ Tolong masukkan nama produknya juga. Contoh: `/naskah Pembersih Sepatu`", parse_mode="Markdown")
        return
        
    bot.reply_to(message, f"✍️ Sedang meracik naskah video TikTok untuk produk: *{product_name}*...", parse_mode="Markdown")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Anda adalah scriptwriter video pendek TikTok profesional berkonversi tinggi."},
                {"role": "user", "content": f"Buatkan naskah video 30 detik untuk produk '{product_name}' dengan struktur: 1. Hook (3 detik awal yang memancing rasa penasaran), 2. Masalah, 3. Solusi produk, 4. Call to Action (Arahkan ke keranjang kuning)."}
            ]
        )
        script_result = response.choices[0].message.content
        bot.reply_to(message, f"🎬 **Draf Naskah Siap Pakai:**\n\n{script_result}", parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Gagal membuat naskah: {str(e)}")

# Menjalankan Bot secara terus-menerus di Cloud
print("Bot sedang berjalan...")
bot.infinity_polling()
