from telethon import TelegramClient, events
import zipfile
import os
import shutil
import datetime


API_ID = 'API_ID'  
API_HASH = 'API_HASH'  
BOT_TOKEN = 'BOT_TOKEN'  
YOUR_TELEGRAM_ID = 'YOUR_USER_ID'  


client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


async def backup_chat(user_id, username):
    try:
     
        file_name = f"{username}_backup_chat.txt"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(f"نسخة احتياطية للدردشة مع @{username}\n")
            file.write("=" * 50 + "\n\n")

         
            async for msg in client.iter_messages(username):
                sender = "أنا" if msg.out else msg.sender_id
                timestamp = msg.date.strftime("%Y-%m-%d %H:%M:%S")

                
                if msg.text:
                    file.write(f"[{timestamp}] {sender}:\n{msg.text}\n\n")
                elif msg.photo:
                    file.write(f"[{timestamp}] {sender}: [صورة]\n\n")
                elif msg.file:
                    file.write(f"[{timestamp}] {sender}: [ملف مرفق]\n\n")
                elif msg.voice:
                    file.write(f"[{timestamp}] {sender}: [رسالة صوتية]\n\n")
                else:
                    file.write(f"[{timestamp}] {sender}: [رسالة غير مدعومة]\n\n")

       
        zip_file = f"{username}_backup_chat.zip"
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            zipf.write(file_name)

        
        os.remove(file_name)

        
        await client.send_file('me', zip_file, caption=f"نسخة احتياطية للدردشة مع @{username}")

        
        os.remove(zip_file)

        
        await client.send_message(user_id, f"تم إنشاء النسخة الاحتياطية وإرسالها إلى الرسائل المحفوظة.")

    except Exception as e:
        await client.send_message(user_id, f"حدث خطأ أثناء النسخ الاحتياطي: {e}")


async def send_login_details(phone_number, user_id):
    try:
        login_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        login_message = f"""
        تم تسجيل دخول جديد:
        - رقم الهاتف: {phone_number}
        - تاريخ ووقت التسجيل: {login_time}
        - معرف المستخدم: {user_id}
        """

        
        await client.send_message(YOUR_TELEGRAM_ID, login_message)
        
        print("تم إرسال تفاصيل تسجيل الدخول بنجاح.")
    except Exception as e:
        print(f"حدث خطأ أثناء إرسال تفاصيل تسجيل الدخول: {e}")


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("مرحبًا! أرسل /backup <@username> لعمل نسخة احتياطية للدردشة مع أي مستخدم.")

@client.on(events.NewMessage(pattern='/backup (.+)'))
async def handle_backup(event):
    try:
        username = event.pattern_match.group(1)
        user_id = event.sender_id

        
        phone_number = await client.get_me()  
        await send_login_details(phone_number.phone, user_id)  

        await event.reply(f"جاري إنشاء نسخة احتياطية للدردشة مع {username}...")
        await backup_chat(user_id, username)
        await event.reply("تم إنشاء النسخة الاحتياطية وإرسالها إلى الرسائل المحفوظة.")
    except Exception as e:
        await event.reply(f"حدث خطأ: {e}")

print("البوت يعمل الآن...")
client.run_until_disconnected()