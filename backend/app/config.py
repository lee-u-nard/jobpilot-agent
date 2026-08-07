import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///jobpilot.db")

    @staticmethod
    def validate():

        if not Config.ANTHROPIC_API_KEY:
            raise RunTimeError(
                "ANTHROPIC_API_KEY is not set. Copy env.example to .env and add your key."
            )