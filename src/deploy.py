import os
import sys
from contract import ContractManager


contract_mgr = ContractManager()

tx_receipt = contract_mgr.deploy(bytecode_path="contracts/bytecode.txt", abi_path="contracts/abi.json")
print('#### Contract deployed to following address ####', file=sys.stdout)
print(tx_receipt.contractAddress, file=sys.stdout)



