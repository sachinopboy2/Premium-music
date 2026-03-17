from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.API_ID = int(getenv("API_ID", 0))
        self.API_HASH = getenv("API_HASH")

        self.BOT_TOKEN = getenv("BOT_TOKEN")
        self.MONGO_URL = getenv("MONGO_URL")

        self.LOGGER_ID = int(getenv("LOGGER_ID", 0))
        self.OWNER_ID = int(getenv("OWNER_ID", 0))

        self.DURATION_LIMIT = int(getenv("DURATION_LIMIT", 60)) * 60
        self.QUEUE_LIMIT = int(getenv("QUEUE_LIMIT", 20))
        self.PLAYLIST_LIMIT = int(getenv("PLAYLIST_LIMIT", 20))

        self.SESSION1 = getenv("SESSION", "BQFYxG8ALnr-PNBIs5SHqY69zuK3uMeDED3WkXwigDljMG8Y5ooWW8h2nI8DFfGSs6AC4W2WgTbJLNdm5Ecl8dAGtOfLknQLU2VtOosXBISmwgrdZZZD1IKRNf4G3Pw0PpKTVRaOzd5FfGUms5y7ZBkYkMgpWArWCugr9y9QP99KhsVc5054w38dvNKv8MTLWOvoURCH-EHv6WeL_ytvm_eVABlNA_ZZoivFQ-dj7j4BGZpq8Dc73zqXygJ8QGWUawNyUXKSnOBGvCf9EXktqJpT370yTU9UzHXR5XrlR24TPcdvlhLJG9u0pePjWmJmtZ2fQvXUCZZUTdxKMyqLgXmIwmtq1gAAAAHYWpZnAA")
        self.SESSION2 = getenv("SESSION2", None)
        self.SESSION3 = getenv("SESSION3", None)

        self.SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/nobmz")
        self.SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/nobmz")

        self.AUTO_LEAVE: bool = getenv("AUTO_LEAVE", "False").lower() == "true"
        self.AUTO_END: bool = getenv("AUTO_END", "False").lower() == "true"
    
        self.THUMB_GEN: bool = getenv("THUMB_GEN", "True").lower() == "true"
        self.VIDEO_PLAY: bool = getenv("VIDEO_PLAY", "True").lower() == "true"

        self.LANG_CODE = getenv("LANG_CODE", "en")

        self.COOKIES_URL = [
            url for url in getenv("COOKIES_URL", "").split(" ")
            if url and "batbin.me" in url
        ]
        self.DEFAULT_THUMB = getenv("DEFAULT_THUMB", "https://files.catbox.moe/odpfbw.jpg")
        self.PING_IMG = getenv("PING_IMG", "https://files.catbox.moe/odpfbw.jpg")
        self.START_IMG = getenv("START_IMG", "https://files.catbox.moe/odpfbw.jpg")

    def check(self):
        missing = [
            var
            for var in ["API_ID", "API_HASH", "BOT_TOKEN", "MONGO_URL", "LOGGER_ID", "OWNER_ID", "SESSION1"]
            if not getattr(self, var)
        ]
        if missing:
            raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")
