from os import path, getenv
from dotenv import load_dotenv

PROJECT_DIR = path.abspath(path.dirname(__file__))
ENV_PATH = path.join(PROJECT_DIR, ".env")
load_dotenv(ENV_PATH)

SELLER = "0x4F520583303086612E68FD55BfB5569f5167C813"
GANACHE_URL = getenv("GANACHE_URL", "http://ganache:8545")
DAI_CONTRACT_ADDRESS = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
CHECK_BLOCKCHAIN_EVERY = 14
ROOT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
SHROOM_MARKET_CONTRACT_ADDRESS = getenv('SHROOM_MARKET_CONTRACT_ADDRESS')

