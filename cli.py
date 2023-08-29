import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
alchemy_url = os.getenv("ALCHEMY_URL")
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Print if web3 is successfully connected
print(w3.is_connected())

# Get the latest block number
latest_block = w3.eth.block_number
print(latest_block)

# Get the balance of an account
#balance = w3.eth.get_balance('0x742d35Cc6634C0532925a3b844Bc454e4438f44e')
#print(balance)

# Get the information of a transaction
#tx = w3.eth.get_transaction('0xbde52a2e10c85ef4779244cfb786ce25dea1cb11639cb997b858e6fb6cde06c5')
#print(tx)

#blockz = w3.eth.get_block(latest_block)
#print(blockz)

traces = w3.eth.trace_block(latest_block)
print(traces)
