## Bot interacting with a fantasy marketplace on Ethereum blockchain

This is an experimental project to build a bot that automates operations of fantasy magic shrooms vendors.
The bot is listening for new orders and confirm them if they are valid and goods are in inventory.
Please use it at your own risk and for educational purposes only.

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

