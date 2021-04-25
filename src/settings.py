import os
import sys
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')

if not os.path.exists(dotenv_path):
    print("File .env does not exist in the root directory")
    sys.exit(-1)

load_dotenv(dotenv_path)

try:
    settings = {
        'GITHUB_TOKEN': os.environ['GITHUB_TOKEN'],
    }
except KeyError as e:
    print("File .env does not contain an environment variable " + str(e)[1:-1])
    sys.exit(-1)
