import sys
sys.path.insert(1, '../..')
from common.config import nodeUri, contract, users, chainId
from libs.crabada.web3client.Web3Client import Web3Client
from pprint import pprint

# VARS
client = (Web3Client()
    .setNodeUri(nodeUri)
    .setAbi(contract['abi'])
    .setCredentials(users[0]['address'], users[0]['privateKey'])
    .setChainId(chainId)
    .init())

to = "0xBc3a38C981B13625FAF7729fF105Cb6E15bdDE3A"
valueInEth = 0.00001 # ETH / AVAX / etc
gas = 200000 # units
gasPrice = 25 # gwei

# TEST FUNCTIONS
def testBuildTransactionWithValue():
    tx = client.buildTransactionWithValue(to, valueInEth, gas, gasPrice)
    print(">>> TX")
    pprint(tx)

def testSignTransaction():
    tx = client.buildTransactionWithValue(to, valueInEth, gas, gasPrice)
    signedTx = client.signTransaction(tx)
    print(">>> SIGNED TX")
    pprint(signedTx)

def sendSignedTransaction():
    tx = client.buildTransactionWithValue(to, valueInEth, gas, gasPrice)
    signedTx = client.signTransaction(tx)
    txHash = client.sendSignedTransaction(signedTx)
    print(">>> TX SENT!")
    print("Hash = " + txHash)
    print("Waiting for transaction to finalize...")
    tx_receipt = client.w3.eth.wait_for_transaction_receipt(txHash)
    print(">>> TX IS ON THE BLOCKCHAIN :-)")
    pprint(tx_receipt)
    print(">>> ETH SPENT")
    print(client.w3.fromWei(tx_receipt['effectiveGasPrice']*tx_receipt['gasUsed'], 'ether'))

# EXECUTE
testBuildTransactionWithValue()
testSignTransaction()
if (len(sys.argv) > 1 and sys.argv[1] == '--send'):
    sendSignedTransaction()