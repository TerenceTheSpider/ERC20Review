# Calculates the tree of wallets and token balances for an ERC-20 root_wallet
# Powered by Etherscan.io APIs

# Example usage:
# python review-wallet.py 0x908016087ba547b675aa9e680e77e639203c8df1

import sys
import json
import urllib.request
from time import sleep
from datetime import datetime

# Init method. Setup all values here
def init():
	global my_apikey, token_contract_address, known_wallets
	global processed_wallets, root_wallet, wallet_timestamps
	global max_recursive_level
	
	# Validate input arguments and read in root_wallet
	if(len(sys.argv) != 2):
		raise Exception('Invalid number of arguments')
	root_wallet = sys.argv[1]
	print("root_wallet: " + root_wallet)
	
	max_recursive_level = 20 # Set to the maximum number of levels to trace before stopping
	my_apikey = "TODO" # Set to your etherscan API key
	token_contract_address = "0x947AEb02304391f8fbE5B25D7D98D649b57b1788" # MDX ERC20 contract
	known_wallets = {
		'0xbcdb9c58973b3d9b6b02282524dfc8ce63619696': 'Uniswap V3',
		'0xe495fdfabc7c51c0851e76543c0f552205414894': 'Uniswap V2',
		'0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be': 'Binance',
		'0x28c6c06298d514db089934071355e5743bf21d60': 'Binance 14',
		'0x11ededebf63bef0ea2d2d071bdf88f71543ec6fb': 'Metamask fees',
		'0x8d12a197cb00d4747a1fe03395095ce2a5cc6819': 'EtherDelta',
		'0xcce8d59affdd93be338fc77fa0a298c2cb65da59': 'Bilaxy 2'
	}
	processed_wallets = {} # Start empty
	wallet_timestamps = {} # Start empty
	
	define_crossed_wallets()

# If you are using the script to analyze multiple root wallets, it is possible the root wallets
#  may share some of the same downstream wallets. Define which root wallet to associate them
#  with, along with a name to prevent double counting.
def define_crossed_wallets():
	global crossed_wallets
	crossed_wallets = {}
	if(root_wallet != "0x07d52307043d19627e26390397a02897c54101ef"):
		crossed_wallets['0x07d52307043d19627e26390397a02897c54101ef'] = "Dumper 1"
		crossed_wallets['0xc8cf5271d906b453132f0d9949c2672eb34dbdfe'] = "Dumper 1"
		crossed_wallets['0x98265a1ff213dd8136e0bf58c2c40cb47d2b8648'] = "Dumper 1"
		crossed_wallets['0x819b06a41620ace5b0d8e8faf165d8e4f80efa38'] = "Dumper 1"
		crossed_wallets['0x077edcc92337ed87c5d8f975f955a25465a5d950'] = "Dumper 1"
		crossed_wallets['0x726761f25224bba69e01edd13423741fad393ffa'] = "Dumper 1"
		crossed_wallets['0x5d6b47ea96fc54481d747db5756bd6660615a547'] = "Dumper 1"
		crossed_wallets['0x0c098eae4bea41a98ad9954a041a215be7348992'] = "Dumper 1"
		crossed_wallets['0x4034a3c94d1efe61d4a047f5a223b385b065eb0c'] = "Dumper 1"
		crossed_wallets['0xcfa912db879d4b84eedffc646272bd05a3e67b62'] = "Dumper 1"
	if(root_wallet != "0x329e6bc06ea9b1de17fccf369d155ffea7d6a383"):
		crossed_wallets['0x329e6bc06ea9b1de17fccf369d155ffea7d6a383'] = "Dumper 2"
		crossed_wallets['0x03dd885e424c230cb88dafb0fbeaf0da43a388cc'] = "Dumper 2"
		crossed_wallets['0x7fdd7cfafca3c851d47f36e90a7f134f720e7c91'] = "Dumper 2"
		crossed_wallets['0xd0c133cd3f98614d02a5a406cc1951c82c59a9c7'] = "Dumper 2"
		crossed_wallets['0x236ebb94bba9f915bcd822c0b7c4b7308057881b'] = "Dumper 2"
		crossed_wallets['0xa98545c768b0b705ce86c54367bcf0207fc00af5'] = "Dumper 2"
		crossed_wallets['0x39c91c5ea63f1773e7dc514453d18a0679f51fa8'] = "Dumper 2"
		crossed_wallets['0x6a8802aefc31189900555e2fa6f5e42a43e4235c'] = "Dumper 2"
		crossed_wallets['0xbac57c1d7857d04081996a846deb85ca58ea775e'] = "Dumper 2"
		crossed_wallets['0x04a5a94ceda835fa2cfe9961aba3856245ece825'] = "Dumper 2"
		crossed_wallets['0x84f0269d04300b20c69d6d118db4372052e94ea4'] = "Dumper 2"
	if(root_wallet != "0xe4fe9d9b6d1a69f0fc5ef21b1e6b525782054aa5"):
		crossed_wallets['0xe4fe9d9b6d1a69f0fc5ef21b1e6b525782054aa5'] = "Dumper 3"
		crossed_wallets['0x45067981ee0202d3475bfc0ccd5ca202eafb9317'] = "Dumper 3"
		crossed_wallets['0x2ca93a8b9eb89ffd813cd410253e3353ccb76eea'] = "Dumper 3"
		crossed_wallets['0x28e3453ed30d5409a1f447394db25145b56c6351'] = "Dumper 3"
	if(root_wallet != "0xbf570dc3e242ecae46fad456b19e03789c30f961"):
		crossed_wallets['0xbf570dc3e242ecae46fad456b19e03789c30f961'] = "Dumper 4"
	if(root_wallet != "0x87c9559a0a62ea8ffe73a83b5eaa523009e13b84"):
		crossed_wallets['0x87c9559a0a62ea8ffe73a83b5eaa523009e13b84'] = "Dumper 5"
	if(root_wallet != "0x64d9473bff00d3acf9912590197bcb2d0aa17eb7"):
		crossed_wallets['0x64d9473bff00d3acf9912590197bcb2d0aa17eb7'] = "Dumper 6"
		crossed_wallets['0xd102a8522c579a696ca81d07cc7d1a2b19bed394'] = "Dumper 6"
		crossed_wallets['0x6518706f44424508d9df737d2aeb76302eb879e2'] = "Dumper 6"
		crossed_wallets['0xe302e981ec1acce168dc550e6842a00ae66554fc'] = "Dumper 6"
		crossed_wallets['0x511487cda31b0cd0c4f2d7365d102c49dbe4ffca'] = "Dumper 6"
		crossed_wallets['0xd980ba486a9a75d47896e2fea54b02cb257e7605'] = "Dumper 6"
		crossed_wallets['0xa195855f71d6472b6b52a9ff62cc405d2dc966e6'] = "Dumper 6"
		crossed_wallets['0xc054b461e7cb8254a48f65a52c4136c3382020ee'] = "Dumper 6"
	if(root_wallet != "0x7dbb492871b8b1da6d9ff3cd3e4e7a2e2916093d"):
		crossed_wallets['0x7dbb492871b8b1da6d9ff3cd3e4e7a2e2916093d'] = "Dumper 7"
		crossed_wallets['0x1095a8d900e33c95f729e5a830581f29d86755f1'] = "Dumper 7"
		crossed_wallets['0x819950e173c10c737e00863924e8c247133ea5eb'] = "Dumper 7"
		crossed_wallets['0xfd25294fcb651035ef708d0c868f0eb906010b85'] = "Dumper 7"
		crossed_wallets['0x463b63a478c54c73b35c26e20733c62e535b22e0'] = "Dumper 7"
		crossed_wallets['0xef26ac0bc61da8ec02e4612620a0ff275f8fd3af'] = "Dumper 7"
		crossed_wallets['0xaad644800c3beb0ba68da6626a991eb8e2b204f6'] = "Dumper 7"
	if(root_wallet != "0x8fa02742886f451c1f62ea13fe5f259b0460230f"):
		crossed_wallets['0x8fa02742886f451c1f62ea13fe5f259b0460230f'] = "Dumper 8"
		crossed_wallets['0x38d471967fc2b3541df6d9ac1f3fb3efdd7d3674'] = "Dumper 8"
		crossed_wallets['0xa5838c514016aa93340dcd948c2168e72e359b0d'] = "Dumper 8"
	if(root_wallet != "0x9d11a3b119a3a52a5646cbf53a0151e673e913f5"):
		crossed_wallets['0x9d11a3b119a3a52a5646cbf53a0151e673e913f5'] = "Dumper 9"
		crossed_wallets['0xe81fa2296e7c18587bdab05cd81ee4cfb6a1144d'] = "Dumper 9"
		crossed_wallets['0x2f99c21533657e8050fe3c60ea61d1c63b96d415'] = "Dumper 9"
		crossed_wallets['0x3f148d7e56443ae03f049a34622eaeb8e0dd4081'] = "Dumper 9"
		crossed_wallets['0x30a21ece1aeefcd4b5fd4c9369e9b3183ee1d00b'] = "Dumper 9"
		crossed_wallets['0x72ec0976403a750ff76e8aec1982609e5ddf9103'] = "Dumper 9"
		crossed_wallets['0x05ff93312c6c0f5df2b3409a561770849ec1d9d5'] = "Dumper 9"
		crossed_wallets['0x5ba6b2b284f60dafaa7b51ce622b3ecd0c5bf0fb'] = "Dumper 9"
	if(root_wallet != "0x908016087ba547b675aa9e680e77e639203c8df1"):
		crossed_wallets['0x908016087ba547b675aa9e680e77e639203c8df1'] = "Dumper 10"
	if(root_wallet != "0x74de5d4fcbf63e00296fd95d33236b9794016631"):
		crossed_wallets['0x74de5d4fcbf63e00296fd95d33236b9794016631'] = "Hub Wallet"
		crossed_wallets['0xa6615d4df10389718d5d7e05a0843d7e84965b2b'] = "Hub Wallet"
		crossed_wallets['0x27239549dd40e1d60f5b80b0c4196923745b1fd2'] = "Hub Wallet"

# prints a json string in human readable form
def print_json(json_string):
	parsed = json.loads(json_string)
	print(json.dumps(parsed, indent=4, sort_keys=True))

# Prints a string indented for recursive_level
def print_with_recursive_level(recursive_level, output_string):
	for x in range(recursive_level):
		for x in range(4):
			output_string = " " + output_string
	print(output_string)

# Make http call, retry 3 times if failure
def make_http_call(url_str):
	#print(url_str)
	
	for x in range(3):
		try:
			response = urllib.request.urlopen(url_str)
			
			status_code = response.getcode()
			
			if(status_code == 200):
				response_body = response.read()
				#print_json(response_body)
				sleep(0.25) # Sleep to stay within API limit before next call
				return response_body
			else:
				print("HTTP Error: " + url_str + ", " + str(status_code) + ", try " + str(x))
				sleep(0.25) # Sleep to stay within API limit before next call
		except Exception as err:
			print("Exception caught: " + url_str + ", " + str(err) + ", try " + str(x))
			sleep(0.25) # Sleep to stay within API limit before next call
			pass

# EtherScan API Call: Returns the current balance of an ERC-20 token of an address.
def http_get_wallet_token_balance(wallet_address):
	url_str = "https://api.etherscan.io/api" \
		+ "?module=account" \
		+ "&action=tokenbalance" \
		+ "&contractaddress=" + token_contract_address \
		+ "&address=" + wallet_address \
		+ "&tag=latest" \
		+ "&apikey=" + my_apikey
	
	return make_http_call(url_str)

# Gets the integer token balance of wallet_address using http_get_wallet_token_balance
def get_wallet_token_balance(wallet_address):
	response = http_get_wallet_token_balance(wallet_address)
	parsed = json.loads(response)
	raw_token_balance = parsed["result"]
	token_balance = int(float(raw_token_balance) / 1000000000000000000)
	return token_balance

# EtherScan API Call: Returns the list of ERC-20 tokens transferred by an address.
def http_get_wallet_transfers(wallet_address):
	url_str = "https://api.etherscan.io/api" \
		+ "?module=account" \
		+ "&action=tokentx" \
		+ "&contractaddress=" + token_contract_address \
		+ "&address=" + wallet_address \
		+ "&apikey=" + my_apikey

	return make_http_call(url_str)

# Test if wallet address is in test_dictionary
def test_wallet_address(wallet_address, test_dictionary):
	if wallet_address in test_dictionary:
		return True
	else:
		return False

# Add wallet to processed_wallets and track wallet_timestamps
def add_wallet_to_dictionaries(wallet_address, last_transfer_date):
	global processed_wallets
	
	# Get the token balance for the wallet
	token_balance = get_wallet_token_balance(wallet_address)
	
	# Add the wallet_address and token_balance to the processed_wallets dictionary
	processed_wallets[wallet_address] = token_balance
	
	# Add the wallet last_transfer_date to the wallet_timestamps dictionary
	wallet_timestamps[wallet_address] = last_transfer_date

def get_last_transfer_date(parsed):
	# get the max timeStamp from results
	last_transfer_date = 0 #Start empty
	for transfer in parsed['result']:
		timeStamp = int(transfer['timeStamp'])
		if(timeStamp > last_transfer_date):
			last_transfer_date = timeStamp
	
	return datetime.utcfromtimestamp(last_transfer_date).strftime('%Y-%m-%d')

# Recursive function to build the wallet tree from wallet_address
def build_wallet_tree_recursive(recursive_level, wallet_address, max_level):
	# Test if max level has been reached
	if(recursive_level == max_level):
		print_with_recursive_level(recursive_level, "Recursive limit reached")
		return
	
	# Get all wallet_transfers for wallet_address
	response = http_get_wallet_transfers(wallet_address)
	parsed = json.loads(response)
	
	# Get last transfer date
	last_transfer_date = get_last_transfer_date(parsed)
	
	# Add the wallet to the processed_wallets dictionary
	add_wallet_to_dictionaries(wallet_address, last_transfer_date)
	
	# Output the wallet_address and last_transfer_date at recursive_level indentation
	output_str = wallet_address + " [" + last_transfer_date + "]"
	print_with_recursive_level(recursive_level, output_str)
	
	# Build a dictionary of 'to' wallets to process
	to_process_wallets = {} #Start empty
	for transfer in parsed['result']:
		to_wallet = transfer['to']
		if(to_wallet != wallet_address):
			to_process_wallets[to_wallet] = 1
	
	# Process each to_wallet in to_process_wallets dictionary
	for to_wallet in to_process_wallets:
		# If wallet is known wallet, print the known wallet and continue
		if(test_wallet_address(to_wallet, known_wallets)):
			print_with_recursive_level(recursive_level + 1, known_wallets[to_wallet])
			continue
		# If wallet has already been counted in another total, print the wallet and continue
		if(test_wallet_address(to_wallet, crossed_wallets)):
			print_with_recursive_level(recursive_level + 1, to_wallet + " (" + crossed_wallets[to_wallet] + ")")
			continue
		# If wallet is already processed, print the wallet and continue
		elif(test_wallet_address(to_wallet, processed_wallets)):
			output_str = to_wallet + " (repeated)"
			print_with_recursive_level(recursive_level + 1, output_str)
			continue
		# If wallet has not been processed yet, recursively call on new wallet
		else:
			build_wallet_tree_recursive(recursive_level + 1, to_wallet, max_level)

# Builds the wallet tree starting with wallet_address
def build_wallet_tree(wallet_address):
	print("Wallet tree:")
	build_wallet_tree_recursive(0, wallet_address, max_recursive_level)

# Outputs the wallets, by balance. Includes timestamp of last action
def output_sorted_wallets():
	# Sort wallets by balance
	sorted_wallets = sorted(processed_wallets.items(), key=lambda x: x[1], reverse=True)
	
	# Print wallet balances and calculate total
	wallets_total = 0
	print("\nRemaining wallet balances:")
	for i in sorted_wallets:
		output_string = str(i[0]) + " " + str(i[1]) + " " + wallet_timestamps[i[0]]
		print(output_string)
		wallets_total = wallets_total + i[1]

	print("\nTotal wallet balance:")
	print(str(wallets_total))

# Run the script
def main():
	init()

	build_wallet_tree(root_wallet)
	
	output_sorted_wallets()

main()
