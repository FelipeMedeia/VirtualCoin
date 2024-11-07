from Block import*
from BlockChain import*


if __name__ == "__main__":

    blockchain = BlockChain()

    print("##--------------------------------------------------------------##")
    print("##---------------------Começando o DigCoin----------------------##")
    print("")
    print("")

    lastBlock = blockchain.latestBlock()

    blockchain.newData(transmissor="00Userfs000", receptor="00Kingsd00000", quantity=15)
    blockchain.newData(transmissor="00Userkf1000", receptor="00Queenjf00000", quantity=20)
    blockchain.newData(transmissor="00User2000", receptor="00Magic00000", quantity=11)

    lastHash = lastBlock.calcHash()
    block = blockchain.constructBlock(lastHash, blockchain.current_data)

    #Bloco com erro nos endereços
    lastBlock = blockchain.latestBlock()

    blockchain.newData(transmissor="0User000", receptor="00King00000", quantity=10)
    blockchain.newData(transmissor="00User1000", receptor="0Queen00000", quantity=25)
    blockchain.newData(transmissor="00Magic00000", receptor="00User2000", quantity=13)

    lastHash = lastBlock.calcHash()
    block = blockchain.constructBlock(lastHash, blockchain.current_data)

    for block in blockchain.chain:
     print(block,'\n')



    # Modifique o endereço para ter novas analises
    user = "00User2000"
    transactions = blockchain.searchDataUser(user)


    # Exibindo as transações encontradas
    print(f"\nTransações encontradas para o usuário {user}:")
    for address in transactions:
        print(f"Transmissor: {address['transmissor']}, Receptor: {address['receptor']}, Quantidade: {address['quantity']}")

    print("\n##----------------Terminando teste com DigCoin------------------##")
    print("##--------------------------------------------------------------##")
    print("")
    print("")