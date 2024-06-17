
# Videos Downloader

![Videos Downloader](Videos_Downloader.gif)

## About

**Videos Downloader** is a Telegram Bot to download videos from many platform like _**YouTube**_, **_Facebook_**, **_Instagram_**,
only you need video link for download it.
This Bot is programmed with Python language and with `python-telegram-bot` library.

You can use it **Free** from [Bot link](https://t.me/abrtjuig_bot).

## How it works

When `start` the bot:

1. You should choose bot language, **English** or **Arabic**.
2. Then you should choose the platform you want, **YouTube** or **Facebook** or **Instagram**.
3. if your choice is **YouTube**:
   - The Bot will ask you if you want download **video** or **playlist**.
   - Then will ask you to enter your video link.
   - The bot get all video **qualities** available and show it in the Keyboard below.
   - Choose one of them, and it will download your video.
4. if your choice is **Facebook** or **Instagram**:
   - The Bot will ask you to Enter your video link, and it will download your video in the highest quality available.

## Library's

- **python-telegram-bot:** This library provides a pure Python, asynchronous interface for the Telegram Bot API.
- **pytube:** This library for downloading YouTube Videos.
- **instaloader:** This library for downloading pictures (or videos) along with their captions and other metadata from Instagram.
- **yt_dlp:** This library is a feature-rich command-line audio/video downloader.
- **os:** Operating System library, and it is already exist.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ruwo36/downloader.git
   ```

2. Install dependencies:

   ```bash
   pip install python-telegram-bot pytube instaloader yt_dlp
   ```
   **_OR:_**
   ```bash
   pip install python-telegram-bot
   pip install pytube
   pip install instaloader
   pip install yt_dlp
   ```

## Usage

1. Get you telegram API Key from [BotFather](https://t.me/BotFather), and push it in this line from `main` function in our code:

   ```python
   application = Application.builder().token("YOUR_TOKEN").build()
   ```

2. Run the program:

   ```bash
   python main.py
   ```

   After run this command you can use it from your telegram bot.

## Example

```bash
python main.py
```
Show it in my [LinkedIn](https://www.linkedin.com/in/ali-n-ajeeb), I post a video it.

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License - see the [LICENSE](LICENSE) file for details.

And media is licensed under the Copyright, if you want use it or author design contact with us.

## Contact

For any inquiries or support, please contact:
- [my Gmail](mailto:mayasajeeb123@gmail.com), or [my Business Gmail](mailto:it.academy.info1@gmail.com).
- [LinkedIn](https://www.linkedin.com/in/ali-n-ajeeb).
