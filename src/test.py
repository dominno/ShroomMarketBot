import pytest
import os
import tempfile
import shutil
import settings

from web3 import Web3, EthereumTesterProvider

from customer import Inventory
from contract import ContractManager
from customer import buy
from bot import ShroomMarketBot


@pytest.fixture()
def temp_dir():
    """
    Creates temp dir, sets  BASE_WORKDIR as tempdir
    """
    temp_dir = tempfile.TemporaryDirectory()
    os.environ["INVENTORY_PATH"] = temp_dir.name
    return temp_dir


@pytest.fixture
def contract(mocker, temp_dir):
    inv = Inventory(user="customer", inventory_path=temp_dir.name)
    offer1 = {
        'path': os.path.join(temp_dir.name, 'o1.yaml'),
        'genus': 'test',
        'mass': 20,
        'price': 10,
        'id': 1,
        'location': 'forest 1a'

    }
    offer2 = {
        'path': os.path.join(temp_dir.name, 'o2.yaml'),
        'genus': 'test',
        'mass': 20,
        'price': 20,
        'id': 2,
        'location': 'forest 1a'

    }
    inv.update_offer(offer1)
    inv.update_offer(offer2)
    bytecode_path = "contracts/bytecode.txt"
    abi_path = "contracts/abi.json"
    
    contract_mgr = ContractManager()
    tx_receipt = contract_mgr.deploy(bytecode_path=bytecode_path, abi_path=abi_path)
    os.environ['SHROOM_MARKET_CONTRACT_ADDRESS'] = tx_receipt.contractAddress
    return contract_mgr.get_contract(tx_receipt.contractAddress, abi_path)

def test_new_events_should_appear_after_buy(contract, temp_dir):
    bot = ShroomMarketBot()
    buy(5, 'test', 100, '0xb3cC81d316e67DE761E0aefBc35C70D76965dD05', '0xB31C99592bddF9AFdDCbDCC9c98DDbF98B256F23')
    buy(7, 'test', 200, '0xb3cC81d316e67DE761E0aefBc35C70D76965dD05', '0xB31C99592bddF9AFdDCbDCC9c98DDbF98B256F23')
    
    events = [(seller, customer, total) for seller, customer, total in bot.get_new_events()]
    assert events

def test_valid_order_should_be_confired_after_buy(contract, temp_dir):
    bot = ShroomMarketBot()
    buy(1, 'test', 10, '0xb3cC81d316e67DE761E0aefBc35C70D76965dD05', '0xbD004d9048C9b9e5C4B5109c68dd569A65c47CF9')
    bot.confirm_new_orders()
    assert 'sold' in bot.inventory.offers[1]

def test_invalid_order_should_not_be_confirmed(contract, temp_dir):
    bot = ShroomMarketBot()
    buy(1, 'test', 100, '0xb3cC81d316e67DE761E0aefBc35C70D76965dD05', '0xbD004d9048C9b9e5C4B5109c68dd569A65c47CF9')
    bot.confirm_new_orders()
    assert not 'sold' in bot.inventory.offers[1]

def test_already_sold_offer_should_not_be_confirmed(contract, temp_dir):
    bot = ShroomMarketBot()
    buy(1, 'test', 10, '0xb3cC81d316e67DE761E0aefBc35C70D76965dD05', '0xbD004d9048C9b9e5C4B5109c68dd569A65c47CF9')
    assert bot.get_valid_offer('0xbD004d9048C9b9e5C4B5109c68dd569A65c47CF9', '0xb3cC81d316e67DE761E0aefBc35C70D76965dD05', 10)
    bot.confirm_new_orders()
    assert not bot.get_valid_offer('0xbD004d9048C9b9e5C4B5109c68dd569A65c47CF9', '0xb3cC81d316e67DE761E0aefBc35C70D76965dD05', 10)
