from web3 import Web3
import json

from django.shortcuts import render
from social.models import User as OurUser

def load_contract():
    # Connect to Ganache
    ganache_url = "http://ganache:8545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    # Check if connection is successful
    if not web3.is_connected():
        raise Exception("Failed to connect to Ethereum")

    # Get the contract ABI and address if file is not openable, raise an exception
    try:
        with open('/blockchain/build/contracts/Tournament.json', 'r') as f:
            contract_json = json.load(f)
            contract_abi = contract_json['abi']
    except:
        raise Exception("Failed to load contract ABI")

    # read contract address from file
    try:
        with open('/blockchain/build/contract_address.txt', 'r') as file:
            contract_address = file.read().replace('\n', '')
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    except:
        raise Exception("Failed to load contract address")

    # Set the default account
    web3.eth.default_account = web3.eth.accounts[0]
    return contract, web3

blockchain_contract, web3_instance = load_contract()
    
def get_tournaments():
    matches = blockchain_contract.functions.getMatches().call()
    return matches

def save_tournament(data):
    tx_hash = blockchain_contract.functions.saveMatch(
        data["player_id_1"],
        data["player_id_2"],
        data["player_id_3"],
        data["player_id_4"],
        data["score_match_1_2"],
        data["score_match_3_4"],
        data["score_match_final"]
    ).transact()

    # Wait for transaction to be mined
    receipt = web3_instance.eth.wait_for_transaction_receipt(tx_hash)
    return receipt


def tournament_view(request):
    tournaments = get_tournaments()
    tournaments_parsed = []

    for t in tournaments:
        t_parsed = {
            'user1': OurUser.objects.get(id=int(t[0])),
            'user2': OurUser.objects.get(id=int(t[1])),
            'user3': OurUser.objects.get(id=int(t[2])),
            'user4': OurUser.objects.get(id=int(t[3])),
            'winner1': OurUser.objects.get(id=int(t[0])) if t[4][0] > t[4][2] else OurUser.objects.get(id=int(t[1])),
            'winner2': OurUser.objects.get(id=int(t[2])) if t[5][0] > t[5][2] else OurUser.objects.get(id=int(t[3])),
            'score_match_1_2': t[4],
            'score_match_3_4': t[5],
            'score_match_final': t[6]
        }

        tournaments_parsed.append(t_parsed)
    

    context = {
        "tournaments": tournaments_parsed
    }

    if 'HX-Request' in request.headers:
        return render(request, 'tournaments/tournaments.html', context)
    else:
        return render(request, 'tournaments/tournaments_full.html', context)
    
