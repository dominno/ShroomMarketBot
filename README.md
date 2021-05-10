## Bot interacting with a fantasy marketplace on Ethereum blockchain

This is an experimental project to build a bot that automates operations of fantasy magic shrooms vendors.
The bot is listening for new orders and confirm them if they are valid and goods are in inventory.
Please use it at your own risk and for educational purposes only.

The goal is to automate operations of fantasy magic shrooms vendor Charlie by writing a bot transacting on
Ethereum.
Charlie delivers goods to customers by revealing secret locations where shrooms are hidden. Since finding
good secret locations and hiding shrooms takes time, Charlie’s inventory in any given moment is limited.
Normally Charlie publishes a list of offers. Customer picks an offer, calls Ethereum smart contract, locking
funds and specifying offer id. Charlie periodically checks Ethereum for new orders. If order sum corresponds
to the offer id and Charlie has the goods, he calls the contract, taking the money and revealing the secret
location to the customer only. Charlie uses etherscan.io and Metamask to interact with Ethereum and finds
it very tedious.
To help Charlie, bot should listen for new orders and confirm them if they are valid and goods are in inventory.
Offer is a yaml file with following fields:
- genus: string
- mass: int
- price: int
- id: string
Charlie accepts DAI only: https://www.coingecko.com/en/coins/dai

Contract ABI and source code are both here:
https://gist.github.com/paulperegud/c4762ba1741494a4479d8290474a91b8

# How to setup local env

1. Build local env using docker with
    $ make build
2. Deploy contract with
    $ make deploy_contract
    $ #### Contract deployed to following address ####
    $ 0x476e098d28bBC11B5ff96c45eA04c57A02AD4830
3. Run in project dir
    $ cp src/.env.dist src/.env
4. Update src/.env file to include contract address
5. Run bot with
    $ make run_bot

# how to list offers as customer

$ make store ARGS="--offers"

*******************
genus: Basidiomycota
mass: 20
price: 100
id: 3434
location: *********
*******************
genus: Tricholomataceae
mass: 40
price: 200
id: 8654
location: *********

# how to buy offer

Required params:

 - order_id: int
 - customer_pubk: str
 - price: int
 - buyer: address
 - seller: address

$ make store ARGS="--buy 3434 XXXXX 100 0xb3cC81d316e67DE761E0aefBc35C70D76965dD05 0xbD004d9048C9b9e5C4B5109c68dd569A65c47CF9"

# Inventory structure 

Inventory is a directory that hold yaml files, with following structure 

    genus: text
    mass: int
    price: int
    id: int
    location: text

If offer is confirmed then yaml file will be update with key 'sold'

# How to change inventory path while bot is running 

$ make store ARGS="--inventory=/usr/src/app/inventory/inventory_2"

