from web3 import Web3
import math
import abi
import dotenv, os

dotenv.load_dotenv()

HOW_MANY_PLANTS = 1
MAX_PLANTS = 1000
MIN_BALANCE = 0.01

# print(dir(contract.functions.plantSeeds))
bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

address = web3.toChecksumAddress(os.environ['ADDRESS'])
balance = web3.eth.getBalance(os.environ['ADDRESS'])
balance = web3.fromWei(balance, 'ether')

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

    with open('log.txt','a') as file:
        file.write(f"Plant: {plant_growing} TX: {web3.toHex(txn)}\n")


def main():
    if balance < MIN_BALANCE:
        print('balance BNB too small')
        exit()
        
    if plant_growing >= MAX_PLANTS:
        print('plant limit reached ')
        exit()
        
    if ready_plant() >= HOW_MANY_PLANTS:
        send_transaction()
    else:
        print('not enought seed to plant')


if __name__ == "__main__":
    main()
    