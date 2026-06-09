import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from database import (
    init_db,
    save_photo,
    get_all_photos
)

TOKEN = os.getenv("BOT_TOKEN")


async def receive_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    username = update.effective_user.username

    if not username:
        username = update.effective_user.first_name

    photo = update.message.photo[-1]

    file_id = photo.file_id

    save_photo(username, file_id)

    await update.message.reply_text(
        "Photo saved successfully."
    )


async def gallery(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    photos = get_all_photos()

    if not photos:
        await update.message.reply_text(
            "No photos uploaded yet."
        )
        return

    for username, file_id in photos:

        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=file_id,
            caption=f"Uploaded by @{username}"
        )



def main():

    init_db()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            receive_photo
        )
    )

    app.add_handler(
        CommandHandler(
            "gallery",
            gallery
        )
    )

    print("Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()