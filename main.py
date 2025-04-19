from web3 import Web3
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich import print
import os, time

# Load .env
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

# Banner
sign = """[bold cyan]
   ██████╗  █████╗ ███╗   ███╗███╗   ███╗ █████╗ 
  ██╔════╝ ██╔══██╗████╗ ████║████╗ ████║██╔══██╗
  ██║  ███╗███████║██╔████╔██║██╔████╔██║███████║
  ██║   ██║██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║
  ╚██████╔╝██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║
   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
[/bold cyan]
"""
console = Console()
console.print(sign)

# Prompt user
amount_per_tx = float(Prompt.ask("➤  💰 How much ETH per deposit?"))
tx_count = int(Prompt.ask("➤  🔁 How many times do you want to repeat the deposit?"))

# Web3 setup
RPC_URL = "https://arb1.arbitrum.io/rpc"
w3 = Web3(Web3.HTTPProvider(RPC_URL))
assert w3.is_connected(), "[red]➤  ✘ RPC Connection Failed!"

account = w3.eth.account.from_key(PRIVATE_KEY)

# ABI & Contract
CONTRACT_ADDRESS = "0xC5bf05cD32a14BFfb705Fb37a9d218895187376c"
CONTRACT_ABI = [
    {
        "inputs": [],
        "name": "depositETH",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    }
]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Function deposit
def deposit_eth(amount_eth, nonce):
    value = w3.to_wei(amount_eth, 'ether')
    gas_limit = contract.functions.depositETH().estimate_gas({'from': WALLET_ADDRESS, 'value': value})

    base_fee = w3.eth.fee_history(1, 'latest')['baseFeePerGas'][0]
    max_priority_fee = w3.to_wei(1, 'gwei')
    max_fee = base_fee + max_priority_fee

    txn = contract.functions.depositETH().build_transaction({
        'from': WALLET_ADDRESS,
        'value': value,
        'gas': gas_limit,
        'maxPriorityFeePerGas': max_priority_fee,
        'maxFeePerGas': max_fee,
        'nonce': nonce,
        'chainId': 42161,
    })

    signed_txn = w3.eth.account.sign_transaction(txn, PRIVATE_KEY)
    txn_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"[green]➤  ✓ Tx Sent:[/green] {w3.to_hex(txn_hash)} | [cyan]Amount:[/cyan] {amount_eth} ETH")

# Execute loop
start_nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)

for i in range(tx_count):
    try:
        deposit_eth(amount_per_tx, start_nonce + i)
        time.sleep(5)
    except Exception as e:
        print(f"[red]➤  ✘ Error on tx {i+1}:[/red] {e}")
        break
else:
    print("[bold green]➤  All done :)[/bold green]")

