from os import path, getenv
import dotenv

PROJECT_DIR = path.abspath(path.dirname(__file__))
ROOT_DIR = path.abspath(path.dirname(__file__) + "/..")
ENV_PATH = path.join(PROJECT_DIR, ".env")

defaults = {
    "GANACHE_URL": "http://ganache:8545",
    "DAI_CONTRACT_ADDRESS": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    "SELLER": "0x4F520583303086612E68FD55BfB5569f5167C813",
    "CHECK_BLOCKCHAIN_EVERY": 14,
    "PROJECT_DIR": PROJECT_DIR,
    "ROOT_DIR": ROOT_DIR,
    "ENV_PATH": ENV_PATH
}


class Settings:

    def __init__(self):
        dotenv.load_dotenv(ENV_PATH)

    def __getattribute__(self, name):
        default = defaults.get(name)
        if getenv(name, default) != dotenv.get_key(ENV_PATH, name):
            dotenv.load_dotenv(ENV_PATH, override=True)
        return getenv(name, default)

    def __setattr__(self, item, value):    
        dotenv.set_key(ENV_PATH, item, value)
        dotenv.load_dotenv(ENV_PATH, override=True)


settings = Settings()

