from telnetlib import STATUS
from time import time
from web3 import Web3
import math
import abi
import dotenv, os, sys
import datetime

# absolute path to working directory e.g /home/USER/DripGarden-AutoCompound/   
PATH_TO_FILE = ''
HOW_MANY_PLANTS = 1 # if 1 compound each plant, e.g 5 - wait for 5 plant to compound
MAX_PLANTS = 2000   # compound to this value and stop
MIN_BALANCE = 0.01  # minimum account BNB balance below which stop compound

dotenv.load_dotenv(PATH_TO_FILE+'.env')

# Set time to use in logs later
now = datetime.datetime.now()

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
try:
    address = web3.toChecksumAddress(os.environ['ADDRESS'])
    balance = web3.eth.getBalance(os.environ['ADDRESS'])
    balance = web3.fromWei(balance, 'ether')
except:
    print('Set correct PATH_TO_FILE value')
    sys.exit()
contract_adres = web3.toChecksumAddress("0x685bfdd3c2937744c13d7de0821c83191e3027ff")
contract = web3.eth.contract(address=contract_adres, abi=abi.ABI)
 
plant_growing = contract.functions.hatcheryPlants(address).call()

def ready_plant():
    readyplant = contract.functions.getUserSeeds(address).call()
    readyplant = math.floor(readyplant/2592000)
    return readyplant

def send_transaction():      
    nonce = web3.eth.get_transaction_count(address)
    
    tx = contract.functions.plantSeeds(address).buildTransaction({
        'nonce': nonce,
        'gas': 2500000,
        'gasPrice': web3.toWei('5','gwei'),
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=os.environ['KEY'])
    txn = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    with open(PATH_TO_FILE+'log.txt','a') as file:
        file.write(f"{now} Plant: {plant_growing} TX: {web3.toHex(txn)}\n")
        

def main():
    if balance < MIN_BALANCE:
        # print('balance BNB too small')
        with open(PATH_TO_FILE+'log.txt','a') as file:
            file.write(f"{now} - balance BNB too small\n")
        sys.exit()
        
    if plant_growing >= MAX_PLANTS:
        # print('plant limit reached')
        with open(PATH_TO_FILE+'log.txt','a') as file:
            file.write(f"{now} - plant limit reached\n")
        sys.exit()
        
    if ready_plant() >= HOW_MANY_PLANTS:
        send_transaction()


if __name__ == "__main__":
    main()
    