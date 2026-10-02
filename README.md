# Telegram Media Bot

بوت Telegram بسيط يستقبل الصور والفيديوهات والملفات الصوتية والمستندات، ثم ينزّلها ويحفظها داخل مجلد `downloads`.

> BotFather ينشئ البوت ويعطيك التوكن فقط. هذا المشروع هو الكود الذي يشغّل البوت.

## التشغيل على Windows

1. افتح `@BotFather` في Telegram وأرسل `/newbot`، ثم انسخ التوكن.
2. انسخ `.env.example` إلى ملف جديد باسم `.env`.
3. افتح `.env` وضع التوكن مكان `put_your_bot_token_here`.
4. افتح PowerShell داخل هذا المجلد ونفّذ:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py bot.py
```

بعد ظهور رسالة التشغيل، افتح البوت وأرسل له صورة أو فيديو أو صوتًا.

## ملاحظات

- الملفات المحمّلة تُحفظ داخل `downloads/<telegram-user-id>/`.
- لا ترفع ملف `.env` إلى GitHub؛ التوكن موجود فيه ويجب أن يبقى سريًا.
- البوت لا يستطيع تسجيل الدخول إلى بوت Telegram آخر كأنه مستخدم. يمكن للمستخدم إعادة توجيه الملف من البوت الآخر إلى هذا البوت.
