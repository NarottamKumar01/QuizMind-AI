import os

from dotenv import load_dotenv


# Load environment variables

load_dotenv()


class Config:

    # Flask Secret Key

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "default-secret-key"
    )


    # Database

    DATABASE = "database/database.db"


    # Upload Settings

    UPLOAD_FOLDER = "uploads"


    # Allowed File Extensions

    ALLOWED_EXTENSIONS = {

        "pdf",
        "docx",
        "pptx"

    }


    # Maximum Upload Size

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024   # 16 MB



# ----------------------------
# File Extension Checker
# ----------------------------

def allowed_file(filename):

    return (

        "." in filename

        and

        filename.rsplit(".",1)[1].lower()

        in Config.ALLOWED_EXTENSIONS

    )