import os
from dotenv import load_dotenv

load_dotenv()

ALOGRITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET_KEY = os.getenv("SECRET_KEY")
