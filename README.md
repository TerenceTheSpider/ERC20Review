# ERC-20 Review

## Contains tools for analyzing ERC20 wallets

### review-wallet.py

#### Overview:

The review-wallet.py Python script will review a root wallet to determine the remaining balance of the wallet, and all the sub-wallets that it has transferred to. 

It will output the wallet tree, which is all the paths tokens for the specified contract have taken out of the root wallet. It will also include a date (YYYY-MM-DD) of the last action each wallet address has taken for the specified contract. At the end, it will output the full list of wallets in the tree, sorted by remaining balance, again includeing the date  of the last action the wallet has taken. Finally, it will output the total balance of tokens across the root wallet and all the sub-wallets.

#### Setup:
You will need an Etherscan.io API key. You can register for a free account here: https://etherscan.io/apis. Once you have your API key, you will need to plug this into the Python script in the `my_apikey` variable.

The script has a `token_contract_address`, which is currently set to the contract address for the MDX ERC20 token.

The script has a list of known wallets that are defined for various exchange addresses (Uniswap, Binance, EtherDelta, & Bilaxy) as well as the address that tracks MetaMask fees. The code for `known_wallets` can be updated as needed to include whatever list of known wallets you want to be used for the review.

If you are using the script to analyze multiple root wallets, it is possible the root wallets may share some of the same downstream wallets. You can define which root wallet to associate each repeated address with in `crossed_wallets` along with a name, to prevent double counting.

There is a `max_recursive_level` which is used to limit how many levels the script will go when building the sub-wallet tree. It is currently set to 20. It can be increased if you expect there to be longer branches of the tree.

#### Input Parameters:

The script takes one parameter: `root_wallet`. This is the root wallet that you want to do the review of.

#### Usage:

```
python review-wallet.py 0x908016087ba547b675aa9e680e77e639203c8df1
```

#### Example Output:
![image](https://user-images.githubusercontent.com/101527190/158078880-c486813e-b0b2-4e2a-9875-413ee2d90662.png)
