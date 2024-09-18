from web3 import Web3
import json

from django.shortcuts import render
from social.models import User as OurUser

def get_tournaments():
    # Connect to Ganache
    ganache_url = "http://ganache:8545"
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    # Check if connection is successful
    if web3.is_connected():
        print("Connected to Ethereum")
    else:
        print("Failed to connect")

    # Get the contract ABI and address
    with open('/blockchain/build/contracts/Tournament.json') as f:
        contract_json = json.load(f)
        contract_abi = contract_json['abi']

    # contract_address = '0x6B130A87fD200bEb185Eb5426144E7f473AF9Ef9' # get from deploying with truffle
    # read contract adress from file
    with open('/blockchain/build/contract_address.txt', 'r') as file:
        contract_address = file.read().replace('\n', '')
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    # Set the default account
    web3.eth.default_account = web3.eth.accounts[0]
    matches = contract.functions.getMatches().call()
    return matches


def tournament_view(request):
    tournaments = get_tournaments()
    tournaments_parsed = []

    for t in tournaments:
        # t has the following structure ('xxxxxxx', 'player_id_1', 'player_id_2', 'player_id_3', 'player_id_4', '1-0', '1-0', '1-0')
        t_parsed = {
            'tournament_id': t[0],
            'user1': OurUser.objects.get(id=int(t[1])),
            'user2': OurUser.objects.get(id=int(t[2])),
            'user3': OurUser.objects.get(id=int(t[3])),
            'user4': OurUser.objects.get(id=int(t[4])),
            'score_match_1_2': t[5],
            'score_match_2_3': t[6],
            'score_match_final': t[7]
        }

        tournaments_parsed.append(t_parsed)
    

    context = {
        "tournaments": tournaments_parsed
    }

    if 'HX-Request' in request.headers:
        return render(request, 'tournaments/tournaments.html', context)
    else:
        return render(request, 'tournaments/tournaments_full.html', context)
    

    