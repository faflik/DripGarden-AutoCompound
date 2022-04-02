from web3 import Web3
import math
import abi
import dotenv, os, sys, time
   
# path to working directory  
dir_path = os.path.dirname(os.path.realpath(__file__))

HOW_MANY_PLANTS = 1 # if 1 compound each plant, e.g 5 - wait for 5 plant to compound
MAX_PLANTS = 20000   # compound to this value and stop
MIN_BALANCE = 0.02  # minimum account BNB balance below which stop compound
LP_DAY = 3.500      # Limit Lp per Day. Below plant seeds, above sell seeds

dotenv.load_dotenv(dir_path + '/.env')

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
try:
    address = web3.toChecksumAddress(os.environ['ADDRESS'])
    balance = web3.eth.getBalance(os.environ['ADDRESS'])
    balance = web3.fromWei(balance, 'ether')
except:
    with open(dir_path + '/log.txt','a') as file:
        file.write("Wrong dirpath\n")
    sys.exit()
contract_adres = web3.toChecksumAddress("0x685bfdd3c2937744c13d7de0821c83191e3027ff")
contract = web3.eth.contract(address=contract_adres, abi=abi.ABI)

plant_growing = contract.functions.hatcheryPlants(address).call()


def lpDay():
    lp = contract.functions.calculateSeedSell(plant_growing * 86400).call()
    lp_day = (lp*0.95) / 1000000000000000000
    lp_day = round(lp_day,4)
    return lp_day

def ready_plant():
    readyplant = contract.functions.getUserSeeds(address).call()
    readyplant = math.floor(readyplant/2592000)
    return readyplant

def plantSeed():
    nonce = web3.eth.get_transaction_count(address)
    
    tx = contract.functions.plantSeeds(address).buildTransaction({
        'nonce': nonce,
        'gas': 100000, # that's enough
        'gasPrice': web3.toWei('5','gwei'),
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=os.environ['KEY'])
    txn = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    with open(dir_path + '/log.txt','a') as file:
        file.write(f"{time.strftime(format('%d.%m %H:%M'))} Plant {ready_plant()} - {lpDay()} lpDay\n")

def sellSeed():
    nonce = web3.eth.get_transaction_count(address)

    tx = contract.functions.sellSeeds().buildTransaction({
        'nonce': nonce,
        'gas': 500000, # that's enough
        'gasPrice': web3.toWei('5','gwei'),
    })

    signed_tx = web3.eth.account.sign_transaction(tx, private_key=os.environ['KEY'])
    txn = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    with open(dir_path + '/log.txt','a') as file:
        file.write(f"{time.strftime(format('%d.%m %H:%M'))} Sell {ready_plant()} - {lpDay()} lpDay\n")


def main():
    if balance < MIN_BALANCE:
        with open(dir_path + '/log.txt','a') as file:
            file.write(f"{time.strftime(format('%d.%m %H:%M'))} Balance too low - {lpDay()} lpDay\n")
        sys.exit()

    if plant_growing >= MAX_PLANTS:
        with open(dir_path + '/log.txt','a') as file:
            file.write(f"{time.strftime(format('%d.%m %H:%M'))} Plants limit reached - {lpDay()} lpDay\n")
        sys.exit()

    if ready_plant() >= HOW_MANY_PLANTS:
        if lpDay()>=LP_DAY:
            sellSeed()
        else:
            plantSeed()

if __name__ == "__main__":
    main()

