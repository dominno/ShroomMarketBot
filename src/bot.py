import os
import logging
import sys

from time import sleep
from typing import Generator

from web3._utils.filters import LogFilter

from contract import ContractManager
from customer import Inventory
from conf import settings



logger = logging.getLogger(__name__)


def to_bytes(value):
    return bytes(str(value), 'utf-8')


class ShroomMarketBot:
    """
    Bot interacting with a fantasy marketplace on Ethereum blockchain
    """

    def __init__(self):
        self.contract_mgr = ContractManager()
        self.contract = self.contract_mgr.get_contract(settings.SHROOM_MARKET_CONTRACT_ADDRESS, "contracts/abi.json")
        self.inventory = Inventory(user="bot", inventory_path=settings.INVENTORY_PATH)
        self.ask_filter = self.get_filter()
        
    def run(self):
        """
        run the bot, bot will check blockchain for new orders every [CHECK_BLOCKCHAIN_EVERY] seconds
        """
        while True:
            self.check_inventory_change()
            self.confirm_new_orders()
            sleep(settings.CHECK_BLOCKCHAIN_EVERY)

    def get_filter(self) -> LogFilter:
        """
        return LogFilter instance for Ask event
        """
        return self.contract.events.Ask.createFilter(fromBlock="latest")

    def check_inventory_change(self):
        """
        Checks if inventory path was changed, and creates new Inventory instance
        """
       
        if settings.INVENTORY_PATH and settings.INVENTORY_PATH != self.inventory.path:
            print(f'#### ShroomMarketBot: change inventory {settings.INVENTORY_PATH} ####', file=sys.stdout)
            self.inventory = Inventory(user="bot", inventory_path=settings.INVENTORY_PATH)

    def confirm_new_orders(self):
        """
        Checks blockchain for new Ask events, validate if ask 
        offer is valid and then confirm the order on the blockchain by calling confirm function on the smart contract.
        """
        for customer, seller, total in self.get_new_events():
            offer = self.get_valid_offer(seller, customer, total)
            if offer:
                self.confirm_order(offer, seller, customer, total)
            else:
                print(f'#### ShroomMarketBot: offer was not valid  ####', file=sys.stdout)

    def get_new_events(self) -> Generator[tuple, None, None]:
        """
        return Generator that produce tuples of customer, seller, total
        """    
        print('#### ShroomMarketBot: checking for new events ####', file=sys.stdout)
        events = self.ask_filter.get_new_entries()
        if events:
            print('#### ShroomMarketBot: found new events ####', file=sys.stdout)
            for event in events:
                yield event['args']['customer'], event['args']['seller'], event['args']['total']

    def get_valid_offer(self, seller:str, customer:str, total:int) -> dict:
        """
        Checks which offer is the one that customer wants to buy, returns None if there is no valid offer
        :param customer: Address as str
        :param seller: Address as str
        :param total: Offer total
        """ 
        for offer in self.inventory.offers.values():
            if not offer.get('sold') and offer['price'] == total:
                ask_id = self.contract.functions.get_ask_id(seller, to_bytes(offer['id']), customer).call()
                ask_total = self.contract.functions.asks(ask_id).call()
                if ask_total == total:
                    offer['sold'] = True
                    self.inventory.update_offer(offer)
                    return offer

    def confirm_order(self, offer: dict, seller: str, customer: str, total: int):
        """
        Confirm order on the blockchain
        :param offer: offer dict
        :param customer: Address as str
        :param seller: Address as str
        :param total: Offer total
        """    
        offer_id = offer['id']

        print(f'#### ShroomMarketBot: Got new valid order:{offer_id}, making order confirm  ####', file=sys.stdout)
        tx_hash = self.contract.functions.confirm(
            customer,
            to_bytes(offer_id),
            total,
            to_bytes(offer['location'])
        ).transact({'from': seller})
        self.contract_mgr.w3.eth.wait_for_transaction_receipt(tx_hash)


if __name__ == "__main__":
    print('#### ShroomMarketBot: starting ####', file=sys.stdout)
    print(f'#### ShroomMarketBot: using inventory {settings.INVENTORY_PATH} ####', file=sys.stdout)
    print(f'#### ShroomMarketBot: checking orders on contract {settings.SHROOM_MARKET_CONTRACT_ADDRESS} ####', file=sys.stdout)

    try:    
        bot = ShroomMarketBot()        
        bot.run()
    except KeyboardInterrupt:
        exit(0)
            
        












