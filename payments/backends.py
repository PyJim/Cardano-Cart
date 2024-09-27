import requests
import os
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Constants
BLOCKFROST_API_URL = "https://cardano-mainnet.blockfrost.io/api/v0"
BLOCKFROST_PROJECT_ID = os.getenv('BLOCKFROST_PROJECT_ID')

# Function to verify the transaction
def verify_payment(transaction_id, seller_address, expected_amount):
    url = f"{BLOCKFROST_API_URL}/txs/{transaction_id}/utxos"
    headers = {
        'project_id': BLOCKFROST_PROJECT_ID
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        tx_data = response.json()
        
        # Check outputs to verify the payment
        for output in tx_data['outputs']:
            if output['address'] == seller_address:
                # Blockfrost returns amount as a list of dictionaries (because of multi-assets)
                for amount in output['amount']:
                    if amount['unit'] == 'lovelace':  # ADA amount is in Lovelace (1 ADA = 1,000,000 Lovelace)
                        ada_amount = int(amount['quantity']) / 1_000_000
                        if ada_amount >= expected_amount:
                            return True  # Payment verified
                        
    return False  # Payment verification failed


