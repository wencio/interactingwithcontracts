from web3 import Web3
from solcx import compile_source

# connect to Ethereum node
web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/YOUR-PROJECT-ID"))

# set up accounts
account = web3.eth.account.from_key('YOUR-PRIVATE-KEY-HERE')

# compile contract source code
contract_source = """
pragma solidity ^0.8.0;

contract MyContract {
    uint256 public value;

    function setValue(uint256 _value) public {
        value = _value;
    }
}
"""
compiled_contract = compile_source(contract_source)

# deploy contract
contract_interface = compiled_contract['<stdin>:MyContract']
contract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
tx = {
    'from': account.address,
    'gas': 4000000,
    'gasPrice': web3.toWei('50', 'gwei'),
    'nonce': web3.eth.getTransactionCount(account.address),
    'data': contract_interface['bin']
}
signed_tx = account.sign_transaction(tx)
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
