import os
import sys
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if not os.path.exists(dotenv_path):
    print("Файл .env с параметрами не существует в корневой директории")
    sys.exit(-1)

load_dotenv(dotenv_path)

settings = {
    'GITHUB_TOKEN': os.getenv('GITHUB_TOKEN'),
}
