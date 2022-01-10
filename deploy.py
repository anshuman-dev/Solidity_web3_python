# Read our solidity file

from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

#This function looks for any .env file and then loads it
load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


# Complie our Solidity
install_solc("0.6.0")
compiled_sol = compile_standard(
    # You can read about the following stuff at pysolcx github doc section
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode for deploying. JSON PARSING
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# Now deploy. But where? Which blockchain?
# Step - 1: Connect to Ganache blockchain
#w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
#Following to connect with a Mainnet - RINKEBY:
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/a71563cebbe546148425d043ecbc1ae1"))

#chain_id = 1337  # Select the chain id
#Refer to chainlist.org anytime if you want chain id of a blockchain.
chain_id = 4
my_address = "0x94B4e66bB4b9394669Aaa78ea6EEa12d38d985fC"  # Choose any fake address from Ganache



private_key = os.getenv("PRIVATE_KEY")  # Always remember to put 0x at start of private key
# Step - 2: Now create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Step - 3: Build the transaction for deployment. It has 3 steps itself:
# Build the contract Deploy Transaction -> Sign the transaction -> Send the transaction
# Obtaining nonce
nonce = w3.eth.getTransactionCount(my_address)
# This is a transaction object <-> NOT WORKING
transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id, "gasPrice": w3.eth.gas_price,"from": my_address, "nonce": nonce})
#Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
#Send the transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployment Finished")
#Now the contract has been deployed.
#Now to interact and work with the contract
# We need : Contract address and Contract ABI
#You can directly hardcode the address but am deriving it from transaction receipt
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi =abi)

#When making interactions with the blockchain there are two ways to interact with them:
#1. Call -> Simulate making the call and getting a return value. They don't make a state change
#2. Transact -> Actually making a state change
print(simple_storage.functions.retrieve().call())
print("Updating Contract")
#Well following did NOT return anything. Why? There is no return in function in the solidity
#print(simple_storage.functions.store(88).call())
#ANOTHER TRANSACTION STARTS HERE:
store_transaction = simple_storage.functions.store(88).buildTransaction(
    {"chainId": chain_id,"gasPrice": w3.eth.gas_price, "from": my_address, "nonce": nonce + 1}
)
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

#Now the state should be changed. Verified by:
print("Contract updated with new value")
print(simple_storage.functions.retrieve().call())