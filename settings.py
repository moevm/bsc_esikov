import os
import sys
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if not os.path.exists(dotenv_path):
    print("Файл .env не существует в корневой директории")
    sys.exit(-1)

load_dotenv(dotenv_path)

try:
    settings = {
        'GITHUB_TOKEN': os.environ['GITHUB_TOKEN'],
    }
except KeyError as e:
    print("Файл .env не содержит переменную окружения " + str(e)[1:-1])
    sys.exit(-1)
