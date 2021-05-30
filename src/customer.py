import yaml
import argparse
import os
import sys
import logging

from contract import ContractManager
from pathlib import Path

from conf import settings


logger = logging.getLogger(__name__)


class Inventory:
    """
    Inventory class that manage operations on offers.
    """
    def __init__(self, user: str, inventory_path: str):
        self.user = user
        self.offers = {}
        self.path = inventory_path
        for offer_path in Path(inventory_path).rglob("*.yaml"):
            offer = yaml.load(offer_path.open(), Loader=yaml.CLoader)
            offer['path'] = str(offer_path)
            self.offers[offer['id']] = offer

    def update_offer(self, offer:dict):
        with open(offer['path'], 'w') as fp:
            offer_to_dump = offer.copy()
            del offer_to_dump['path']
            yaml.dump(offer_to_dump, fp)

    def print_offers(self):
        print('******offers*********', file=sys.stdout)
        for offer_id in self.offers:
            print('*******************', file=sys.stdout)
            for key in self.offers[offer_id]:
                value = self.offers[offer_id][key]
                if self.user != 'bot' and key == 'location':
                    value = '*********'                
                print(f'{key}: {value}', file=sys.stdout)

        
def buy(order_id: str, customer_pubk: str, price: int, buyer: str, seller: str):
    
    contract_mgr = ContractManager()
    contract = contract_mgr.get_contract(settings.SHROOM_MARKET_CONTRACT_ADDRESS, "contracts/abi.json")
    dai_contract = contract_mgr.get_contract(settings.DAI_CONTRACT_ADDRESS, "contracts/dai_abi.json")
    tx_hash = dai_contract.functions.approve(settings.SHROOM_MARKET_CONTRACT_ADDRESS, price).transact({'from': buyer})
    contract_mgr.w3.eth.wait_for_transaction_receipt(tx_hash)
    
    tx_hash = contract.functions.ask(bytes(customer_pubk, 'utf-8'), seller, bytes(str(order_id), 'utf-8'), price).transact({'from': buyer})
    info = contract_mgr.w3.eth.wait_for_transaction_receipt(tx_hash)    


def change_inventory(path):
    import dotenv
    dotenv_file = dotenv.find_dotenv()    
    dotenv.set_key(dotenv_file, "INVENTORY_PATH", path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--offers", help="list all offers", action='store_true'
    )
    parser.add_argument(
        "--buy",
        help="Send ask request to the contract, required params order_id, customer_pubk, price, buyer", nargs='*'
    )
    parser.add_argument(
        "--inventory",
        help="New inventory path"
    )

    options = parser.parse_args()
    inv = Inventory(user="customer", inventory_path=settings.INVENTORY_PATH)

    if options.offers:    
        inv.print_offers()        

    if options.buy:
        if len(options.buy) != 5:
            raise RuntimeError('Buy needs 4 params: order_id, customer_pubk, price, buyer, seler')
        order_id, customer_pubk, price, buyer, seler = options.buy
        try:
            buy(order_id, customer_pubk, int(price), buyer, seler)
        except ValueError as err:
            print(err)
    if options.inventory:
        change_inventory(options.inventory)
