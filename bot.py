import asyncio
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
DOWNLOAD_DIR = Path(os.getenv("DOWNLOAD_DIR", "downloads"))

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is missing. Copy .env.example to .env and add the token from BotFather."
    )

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = Router()


def safe_filename(filename: str, fallback: str) -> str:
    """Remove unsafe path characters and keep the file inside DOWNLOAD_DIR."""
    filename = Path(filename or fallback).name
    filename = re.sub(r"[^\w.()\- ]+", "_", filename, flags=re.UNICODE).strip()
    return filename or fallback


def unique_path(user_id: int, filename: str) -> Path:
    user_dir = DOWNLOAD_DIR / str(user_id)
    user_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    filename = safe_filename(filename, "file")
    return user_dir / f"{timestamp}_{filename}"


async def save_telegram_file(
    message: Message,
    file_id: str,
    filename: str,
) -> Path:
    telegram_file = await message.bot.get_file(file_id)
    user_id = message.from_user.id if message.from_user else 0
    destination = unique_path(user_id, filename)
    await message.bot.download(telegram_file, destination=destination)
    return destination


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        "أهلًا بك! أرسل لي صورة أو فيديو أو ملفًا صوتيًا، وسأقوم بتنزيله وحفظه.\n\n"
        "استخدم /help لعرض التعليمات."
    )


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "الملفات المدعومة:\n"
        "• الصور\n"
        "• الفيديوهات\n"
        "• الصوتيات\n"
        "• الملفات المرسلة كمستند\n\n"
        "أرسل الملف مباشرة إلى البوت، وسيتم حفظه داخل مجلد downloads."
    )


@router.message(F.photo)
async def photo_handler(message: Message) -> None:
    photo = message.photo[-1]
    path = await save_telegram_file(message, photo.file_id, f"photo_{message.message_id}.jpg")
    await message.answer(f"تم تنزيل الصورة وحفظها باسم:\n{path.name}")


@router.message(F.video)
async def video_handler(message: Message) -> None:
    video = message.video
    filename = video.file_name or f"video_{message.message_id}.mp4"
    path = await save_telegram_file(message, video.file_id, filename)
    await message.answer(f"تم تنزيل الفيديو وحفظه باسم:\n{path.name}")


@router.message(F.audio)
async def audio_handler(message: Message) -> None:
    audio = message.audio
    filename = audio.file_name or f"audio_{message.message_id}.mp3"
    path = await save_telegram_file(message, audio.file_id, filename)
    await message.answer(f"تم تنزيل الصوت وحفظه باسم:\n{path.name}")


@router.message(F.voice)
async def voice_handler(message: Message) -> None:
    path = await save_telegram_file(
        message,
        message.voice.file_id,
        f"voice_{message.message_id}.ogg",
    )
    await message.answer(f"تم تنزيل الرسالة الصوتية وحفظها باسم:\n{path.name}")


@router.message(F.document)
async def document_handler(message: Message) -> None:
    document = message.document
    filename = document.file_name or f"document_{message.message_id}"
    path = await save_telegram_file(message, document.file_id, filename)
    await message.answer(f"تم تنزيل الملف وحفظه باسم:\n{path.name}")


@router.message()
async def unsupported_handler(message: Message) -> None:
    await message.answer("أرسل صورة أو فيديو أو ملفًا صوتيًا، وسأقوم بتنزيله.")


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
