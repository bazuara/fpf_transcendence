from web3 import Web3
import json

# Connect to Ganache
ganache_url = "http://ganache:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))


# Check if connection is successful
if web3.is_connected():
    print("Connected to Ethereum")
else:
    print("Failed to connect")

# Get the contract ABI and address
with open('/app/build/contracts/Tournament.json') as f:
    contract_json = json.load(f)
    contract_abi = contract_json['abi']

# contract_address = '0x6B130A87fD200bEb185Eb5426144E7f473AF9Ef9' # get from deploying with truffle
# read contract adrress from file
with open('/app/output/contract_address.txt', 'r') as file:
    contract_address = file.read().replace('\n', '')
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Set the default account
web3.eth.default_account = web3.eth.accounts[0]


def save_tournament(data):
    tx_hash = contract.functions.saveMatch(
        data["tournament_id"],
        data["player_id_1"],
        data["player_id_2"],
        data["player_id_3"],
        data["player_id_4"],
        data["score_match_1_2"],
        data["score_match_3_4"],
        data["score_match_final"]
    ).transact()

    # Wait for transaction to be mined
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt


def get_tournaments():
    matches = contract.functions.getMatches().call()
    return matches


# Example JSON data
tournament_data = {
    "tournament_id": "xxxxxxx",
    "player_id_1": "player_id_1",
    "player_id_2": "player_id_2",
    "player_id_3": "player_id_3",
    "player_id_4": "player_id_4",
    "score_match_1_2": "1-0",
    "score_match_3_4": "1-0",
    "score_match_final": "1-0"
}

tournament_data_2 = {
    "tournament_id": "2xxxxxx",
    "player_id_1": "player_id_1",
    "player_id_2": "player_id_2",
    "player_id_3": "player_id_3",
    "player_id_4": "player_id_4",
    "score_match_1_2": "1-0",
    "score_match_3_4": "1-0",
    "score_match_final": "1-0"
}

tournament_data_3 = {
    "tournament_id": "3xxxxxx",
    "player_id_1": "player_id_1",
    "player_id_2": "player_id_2",
    "player_id_3": "player_id_3",
    "player_id_4": "player_id_4",
    "score_match_1_2": "1-0",
    "score_match_3_4": "1-0",
    "score_match_final": "1-0"
}

# Save the tournament data
save_tournament(tournament_data)
save_tournament(tournament_data_2)
save_tournament(tournament_data_3)

# Get all matches
matches = get_tournaments()
for match in matches:
    print(match)