# import all variables from ./env.local
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    print("Hello World!")
    import os

    print(os.getenv('BOT_TOKEN'))
