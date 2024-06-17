from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from pytube import YouTube
import instaloader
import yt_dlp
import os

LANGUAGE_KEYBOARD = [['English'], ['العربية']]
BOT_LANGUAGE, PLATFORM, LINK, YOUTUBE_PLATFORM, RESOLUTION, MORE_VIDEOS = range(6)
bot_vars = {
    'bot_language': '',
    'platform': '',
    'youtube_choice': '',
    'link': '',
    'resolution': '',
}
check_more_video = False
youtube_video_title = ''


async def start(update: Update, context: CallbackContext) -> int:
    """Starts the bot and asks the user to select bot language."""
    user_full_name = update.message.from_user.full_name
    bot_message = f"Hi {user_full_name}, I am DownloaderBot.\nEnter /help to show command list\n\nNow pleas select bot language:"
    reply_markup = ReplyKeyboardMarkup(LANGUAGE_KEYBOARD, one_time_keyboard=True)
    await update.message.reply_text(bot_message, reply_markup=reply_markup)
    global check_more_video
    check_more_video = False
    return BOT_LANGUAGE


async def choice_platform(update: Update, context: CallbackContext) -> int:
    """Select bot language and choice the platform."""
    bot_language = update.message.text
    user_full_name = update.message.from_user.full_name
    bot_vars['bot_language'] = bot_language
    PLATFORM_KEYBOARD = [["YouTube"], ["Facebook"], ["Instagram"]]
    english_message = f"Hi {user_full_name}, I am DownloaderBot.I can download videos from many platform like:\n" \
                      "Facebook, YouTube, Instagram, I need only your video link.\n" \
                      "Pleas, choice your video's platform?"

    arabic_message = f"مرحبا {user_full_name} أنا أستطيع تحميل الفيديوهات من عدة منصات مثل:\n" \
                     "فيسبوك, يوتيوب, انستغرام أحتاج فقط إلى رابط الفيديو.\n" \
                     "من فضلك اختر المنصة التي تريد التحميل منها؟"
    if bot_language == 'English':
        await update.message.reply_text(english_message,
                                        reply_markup=ReplyKeyboardMarkup(PLATFORM_KEYBOARD, one_time_keyboard=True))
    elif bot_language == 'العربية':
        await update.message.reply_text(arabic_message,
                                        reply_markup=ReplyKeyboardMarkup(PLATFORM_KEYBOARD, one_time_keyboard=True))
    else:
        await update.message.reply_text('Pleas, press button from keyboard!')

    return PLATFORM


async def platform(update: Update, context: CallbackContext) -> int:
    """Enter video link"""
    global check_more_video
    if not check_more_video:
        platform_name = update.message.text
        bot_vars['platform'] = platform_name
        check_more_video = True
    YOUTUBE_PLATFORM_KEYBOARD = [["Videos"], ["Playlist"]]
    if bot_vars['bot_language'] == 'English':
        if bot_vars['platform'] == 'YouTube':
            await update.message.reply_text("OK, you want to download videos or playlist?",
                                            reply_markup=ReplyKeyboardMarkup(YOUTUBE_PLATFORM_KEYBOARD,
                                                                             one_time_keyboard=True))
            return YOUTUBE_PLATFORM
        else:
            await update.message.reply_text("OK, now enter video link(URL)",
                                            reply_markup=ReplyKeyboardMarkup([['/cancel']], one_time_keyboard=True))
            return LINK
    else:
        if bot_vars['platform'] == 'YouTube':
            await update.message.reply_text("حسنا, تريد تحميل فيديو أو قائمة تشغيل؟",
                                            reply_markup=ReplyKeyboardMarkup(YOUTUBE_PLATFORM_KEYBOARD,
                                                                             one_time_keyboard=True))
            return YOUTUBE_PLATFORM
        else:
            await update.message.reply_text("حسنا, الان أدخل رابط الفيديو",
                                            reply_markup=ReplyKeyboardMarkup([['/cancel']], one_time_keyboard=True))
            return LINK


async def youtube_platform_choice(update: Update, context: CallbackContext) -> int:
    """Download YouTube videos"""
    youtube_choice = update.message.text
    bot_vars['youtube_choice'] = youtube_choice
    if youtube_choice == "Videos":
        if bot_vars['bot_language'] == 'English':
            await update.message.reply_text("Enter the link of YouTube video")
        else:
            await update.message.reply_text("أدخل رابط فيديو اليوتيوب")
        return LINK
    elif youtube_choice == "Playlist":
        if bot_vars['bot_language'] == 'English':
            await update.message.reply_text("Enter the link of playlist")
        else:
            await update.message.reply_text("أدخل رابط قائمة التشغيل")
        return LINK
    else:
        return PLATFORM


async def video_link(update: Update, context: CallbackContext) -> int:
    """Enter video link"""
    video_URL = update.message.text
    bot_vars['link'] = video_URL
    if bot_vars['platform'] == 'YouTube':
        if bot_vars['bot_language'] == 'English':
            await update.message.reply_text("Wait a second to find all available resolution....")
        else:
            await update.message.reply_text("انتظر لحظة لايجاد جميع جودات الفيديو المتاحة....")
        resolution = []
        resolution1 = []
        resolution2 = []
        youtube_downloader(video_URL, resolution, 0)
        RESOLUTION_KEYBOARD = []

        # Remove None value
        for item in resolution:
            if item is not None:
                resolution1.append(item)
            else:
                continue

        # Remove repeating values
        for value in resolution1:
            if len(resolution2) == 0:
                resolution2.append(value)
            else:
                check = True
                for element in resolution2:
                    if element == value:
                        check = False
                    else:
                        continue
                if check:
                    resolution2.append(value)

        # Build Resolution Keyboard
        for i in range(0, len(resolution2) - 1, 2):
            RESOLUTION_KEYBOARD.append([resolution2[i], resolution2[i + 1]])
        if len(resolution2) % 2 != 0:
            RESOLUTION_KEYBOARD.append([resolution2[i + 2]])

        # Create reply markup
        reply_markup = ReplyKeyboardMarkup(RESOLUTION_KEYBOARD, one_time_keyboard=True)

        if bot_vars['bot_language'] == 'English':
            await update.message.reply_text("This all available resolution, please choice one?",
                                            reply_markup=reply_markup)
        else:
            await update.message.reply_text("هذه جميع الجودات المتاحة, اختر واحدة؟", reply_markup=reply_markup)
        return RESOLUTION

    # Download Facebook Videos
    elif bot_vars['platform'] == 'Facebook':
        if bot_vars['bot_language'] == 'English':
            await update.message.reply_text("Wait a moment to download your video.....")
        else:
            await update.message.reply_text("انتظر دقيقة لتحميل الفيديو......")
        # try:
        ydl_opts = {
            'outtmpl': 'facebook_video.mp4',
            'format': 'best'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_URL])
        await update.message.reply_video('facebook_video.mp4')
        os.remove('facebook_video.mp4')
        # except:
        #     if bot_vars['bot_language'] == 'English':
        #         await update.message.reply_text("Somthing wrong in download this video!!")
        #     else:
        #         await update.message.reply_text("هناك خطأ بتحميل هذا الفيديو!!")

    # Download Instagram Videos
    elif bot_vars['platform'] == 'Instagram':
        if bot_vars['bot_language'] == 'English':
            await update.message.reply_text("Wait a moment to download your video.....")
        else:
            await update.message.reply_text("انتظر دقيقة لتحميل الفيديو......")
        # try:
        vid = instaloader.Instaloader()
        post = instaloader.Post.from_shortcode(vid.context, video_URL.split('/')[-2])
        video_file = vid.download_post(post, target='instagram_videos')
        for filename in os.listdir(r'.\instagram_videos'):
            if filename.endswith('.mp4'):
                instagram_video = os.path.join(r'.\instagram_videos', filename)
                break
        print("done1", video_file)
        if video_file:
            print("done2")
            await update.message.reply_video(instagram_video)
            for filename in os.listdir(r'.\instagram_videos'):
                os.remove(filename)
            print("done3")
        else:
            if bot_vars['bot_language'] == 'English':
                await update.message.reply_text("Somthing wrong in download this video!!")
            else:
                await update.message.reply_text("هناك خطأ بتحميل هذا الفيديو!!")
        # except:
        #     if bot_vars['bot_language'] == 'English':
        #         await update.message.reply_text("Somthing wrong in this URL!!")
        #     else:
        #         await update.message.reply_text("هناك خطأ بهذا الرابط!!")
    else:
        return BOT_LANGUAGE


async def resolution_selected(update: Update, context: CallbackContext) -> int:
    """download the video"""
    video_resolution = update.message.text
    bot_vars['resolution'] = video_resolution
    if bot_vars['bot_language'] == 'English':
        await update.message.reply_text("Wait a moment to download your video......")
    else:
        await update.message.reply_text("انتظر دقيقة لتحميل الفيديو......")
    video = youtube_downloader(bot_vars['link'], video_resolution, 1)
    await update.message.reply_video(video)
    global youtube_video_title
    os.remove(f'{youtube_video_title}.mp4')
    VIDEO_KEYBOARD = [["Yse"], ["No"]]
    reply_markup = ReplyKeyboardMarkup(VIDEO_KEYBOARD, one_time_keyboard=True)
    if bot_vars['bot_language'] == 'English':
        await update.message.reply_text("Do you want download more YouTube video?", reply_markup=reply_markup)
    else:
        await update.message.reply_text("هل تريد تحميل المزيد من فيديوهات اليوتيوب؟", reply_markup=reply_markup)
    return MORE_VIDEOS


async def more_youtube_videos(update: Update, context: CallbackContext) -> int:
    """Do you want download more YouTube video"""
    more_video_choice = update.message.text
    if more_video_choice == "Yse":
        if bot_vars['bot_language'] == 'English':
            await update.message.reply_text("Ok")
        else:
            await update.message.reply_text("حسنا")
        return PLATFORM
    elif more_video_choice == "No":
        if bot_vars['bot_language'] == 'English':
            await update.message.reply_text("If you want download video from anther platform pleas enter /start \n"
                                            "Bye! I hope using me agine.", reply_markup=ReplyKeyboardRemove())
        else:
            await update.message.reply_text("إذا أردت تحميل فيديو من منصة أخرى أدخل start/ \n"
                                            "وداعا! أتمنى أن تستخدمني مرة أخرى.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


async def help_user(update: Update, context: CallbackContext) -> None:
    """Get help for user."""
    await update.message.reply_text(
        "Command List:\n"
        "/start -> Start DownloaderBot.\n"
        "/help -> Get command list and details for DownloaderBot.\n"
        "/contact -> Contact with DownloaderBot manager\n"
        "/cancel -> To cancel & ends any processing\n"
    )


async def contact(update: Update, context: CallbackContext) -> None:
    """Contact with us."""
    if bot_vars['bot_language'] == 'English':
        await update.message.reply_text(
            "You can contact with us:\n"
            "Telegram: @itAcademy12\n"
            "Gmail: it.academy.info1@gmail.com\n"
            "Facebook: https://www.facebook.com/profile.php?id=100084779713644\n"
        )
    else:
        await update.message.reply_text(
            "يمكنك التواص معنا عبر:\n"
            "Telegram: @itAcademy12\n"
            "Gmail: it.academy.info1@gmail.com\n"
            "Facebook: https://www.facebook.com/profile.php?id=100084779713644\n"
        )


async def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    if bot_vars['bot_language'] == 'English':
        await update.message.reply_text(
            "Bye! I hope using me agine.", reply_markup=ReplyKeyboardRemove()
        )
    else:
        await update.message.reply_text(
            "وداعا, أتمنى أن تستخدمني مرة ثانية.", reply_markup=ReplyKeyboardRemove()
        )
    return ConversationHandler.END


def youtube_downloader(video_URL: str, resolution, flag=1):
    """
    Download videos or get resolution.
    :param video_URL: The link of your video.
    :param resolution: Resolutions list.
    :param flag: flag with value 1 as default is to download video.
    flag with value 0 is to find the available resolution.
    :return: flag 1 return a video. flag 0 return a list from resolution
    in another case it returns error message.
    """
    try:
        yt = YouTube(video_URL)
        global youtube_video_title
        youtube_video_title = yt.title
        mp4_videos = yt.streams.filter(file_extension='mp4')
        if flag == 0:
            for res in range(len(mp4_videos)):
                resolution.append(mp4_videos[res].resolution)
            return resolution
        else:
            res_video = mp4_videos.filter(res=resolution).first()
            return res_video.download()
    except Exception as e:
        if bot_vars['bot_language'] == 'English':
            error_mes = f"{e} يوجد خطأ في تحميل الفيديو:"
        else:
            error_mes = f"Error in video downloading: {e}"
        return error_mes


def main() -> None:
    """Run the bot."""
    # Create the Application and pass bot token.
    application = Application.builder().token("YOUR_TOKEN").build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            BOT_LANGUAGE: [MessageHandler(filters.Regex("^(English|العربية)$"), choice_platform),
                           CommandHandler("start", start), CommandHandler("cancel", cancel)],
            PLATFORM: [MessageHandler(filters.Regex("^(YouTube|Facebook|Instagram)$"), platform),
                       CommandHandler("start", start), CommandHandler("cancel", cancel)],
            YOUTUBE_PLATFORM: [MessageHandler(filters.Regex("^(Videos|Playlist)$"), youtube_platform_choice),
                               CommandHandler("start", start), CommandHandler("cancel", cancel)],
            LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, video_link), CommandHandler("start", start),
                   CommandHandler("cancel", cancel)],
            RESOLUTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, resolution_selected),
                         CommandHandler("start", start), CommandHandler("cancel", cancel)],
            MORE_VIDEOS: [MessageHandler(filters.Regex("^(Yes|No)$"), more_youtube_videos),
                          CommandHandler("start", start), CommandHandler("cancel", cancel)],
        },
        fallbacks=[CommandHandler("cancel", cancel),
                   CommandHandler("help", help_user),
                   CommandHandler("contact", contact)],
    )
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
