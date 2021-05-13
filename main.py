from app import app
#  check .env file and settings app
from src.settings import settings


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
