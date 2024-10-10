from Block import*
from BlockChain import*


if __name__ == "__main__":

    blockchain = BlockChain()

    print("##--------------------------------------------------------------##")
    print("##---------------------Começando o DigCoin----------------------##")
    print("")
    print("")

    lastBlock = blockchain.latestBlock()

    blockchain.newData(transmisor="0", receptor="The King", quantity=1)
    blockchain.newData(transmisor="1", receptor="The Queen", quantity=2)
    blockchain.newData(transmisor="2", receptor="The Magic", quantity=1)

    lastHash = lastBlock.calcHash()
    block = blockchain.constructBlock(lastHash, blockchain.current_data)

    
    lastBlock = blockchain.latestBlock()

    blockchain.newData(transmisor="3", receptor="The King", quantity=2)
    blockchain.newData(transmisor="4", receptor="The Queen", quantity=3)
    blockchain.newData(transmisor="5", receptor="The Magic", quantity=2)

    lastHash = lastBlock.calcHash()
    block = blockchain.constructBlock(lastHash, blockchain.current_data)

    lastBlock = blockchain.latestBlock()

    blockchain.newData(transmisor="6", receptor="The King", quantity=1)
    blockchain.newData(transmisor="7", receptor="The Queen", quantity=2)
    blockchain.newData(transmisor="8", receptor="The Magic", quantity=1)

    lastHash = lastBlock.calcHash()
    block = blockchain.constructBlock(lastHash, blockchain.current_data)


    for block in blockchain.chain:
     print(block)

    print("##----------------Terminando teste com DigCoin------------------##")
    print("##--------------------------------------------------------------##")
    print("")
    print("")