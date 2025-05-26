import os
import telebot
from youtube_transcript_api import YouTubeTranscriptApi

# Telegram Bot Token (replace with your own token securely in production)
BOT_TOKEN = "7687006033:AAHvdF3NQpzGKQ14liHDtVDEsPy0jZVWwJY"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "স্বাগতম! YouTube ভিডিওর লিংক পাঠান, আমি টেক্সট পাঠাবো।")

@bot.message_handler(func=lambda message: True)
def get_text(message):
    try:
        link = message.text.strip()

        # Extract video ID
        if "v=" in link:
            video_id = link.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in link:
            video_id = link.split("youtu.be/")[-1].split("?")[0]
        else:
            bot.reply_to(message, "দয়া করে সঠিক YouTube লিংক দিন।")
            return

        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = "\n".join([i['text'] for i in transcript])

        # Send to user
        bot.reply_to(message, text[:4000])  # Telegram 4096 char limit

    except Exception as e:
        print("Error:", e)
        bot.reply_to(message, "সম্ভবত ভিডিওতে সাবটাইটেল নেই, বা সমস্যা হচ্ছে।")

bot.polling()
