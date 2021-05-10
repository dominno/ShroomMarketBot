import json
import os
import sys

from web3 import Web3
from pathlib import Path
from settings import GANACHE_URL, ROOT_DIR



def get_w3():
    print(f'connecting to {GANACHE_URL}', file=sys.stdout)
    return Web3(Web3.HTTPProvider(GANACHE_URL))


class ContractManager:
    """
    This call manage web3 Contract interaction
    """
    
    def __init__(self):
        self.w3 = get_w3()

    def get_contract(self, address: str, abi_path: str):
        """
        Returns web3 Contract instance for given address and abi_path
        """
        with open(os.path.join(ROOT_DIR, abi_path), 'r') as abi:
            return self.w3.eth.contract(address=address, abi=json.load(abi))
    
    def deploy(self, bytecode_path: str, abi_path: str):
        """
        Deploy contract using bytecode_path, abi_path and deploy_address
        """
        self.w3.eth.defaultAccount = self.w3.eth.accounts[0]
        with open(os.path.join(ROOT_DIR, bytecode_path), 'r') as bytecode:
            with open(os.path.join(ROOT_DIR, abi_path), 'r') as abi:
                contract = self.w3.eth.contract(abi=json.load(abi), bytecode=bytecode.read())
                tx_hash = contract.constructor().transact()
                tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
                return tx_receipt