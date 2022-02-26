from web3 import Web3
import math
import abi
import dotenv, os

dotenv.load_dotenv('.env')


how_many_plants = 1

# print(dir(contract.functions.plantSeeds))
bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

address = web3.toChecksumAddress(os.environ['ADDRESS'])

contract_adres = web3.toChecksumAddress("0x685bfdd3c2937744c13d7de0821c83191e3027ff")
contract = web3.eth.contract(address=contract_adres, abi=abi.ABI)
 
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
       
    plant_growing = contract.functions.hatcheryPlants(address).call()
    with open('log.txt','a') as file:
        file.write(f"Before plant: {plant_growing} TX: {web3.toHex(txn)} After plant: {plant_growing +1}\n")


def main():
    if ready_plant() >= how_many_plants:
        send_transaction()


if __name__ == "__main__":
    main()
    