import hashlib
import time
import re

class Block:
 
 def __init__(self, index, hash, beforeHash, data, timestamp=None, difficulty=4):
  
  self.index = index
  self.hash = hash
  self.beforeHash = beforeHash
  self.data = data
  self.timestamp = timestamp or time.time()
  self.nonce = 0
  self.difficulty = difficulty

 def calcHash(self):
  block_data = f"{self.index}{self.beforeHash}{self.data}{self.timestamp}{self.nonce}"
  return hashlib.sha256(block_data.encode('utf-8')).hexdigest()
 
 def miner_block(self):
    while not self.hash.startswith('0' * self.difficulty):
        self.nonce += 1
        self.hash = self.calcHash()
 
 def __str__(self):
  return f"Index-{self.index}\nHASH-{self.hash}\nPREVIOUS HASH-{self.beforeHash}\nDATA-{self.data}\nTIME-{self.timestamp}\nNONCE-{self.nonce}"

####################################################################

class BlockChain:
 
 def __init__(self):
  
  self.chain = []
  self.current_data = []
  self.difficulty = 4
  self.genesisBlock()

 def genesisBlock(self):
   self.constructBlock(beforeHash='0', data='Genesis Block!')

 def constructBlock(self, beforeHash, data):
    block = Block(index=len(self.chain), hash='', beforeHash=beforeHash, data=data)
    block.hash = block.calcHash()

    if self.validityBlockChain(block):
        block.miner_block()
        self.chain.append(block)
        print(f"Bloco {block.index} adicionado com sucesso.\n")
    else:
        print(f"Existe algum empedimento para inserir o bloco {block.index} na BlockChain!")
    
    self.current_data = []

    return block

 def validityBlockChain(self, block):
  for i in range(0, len(self.chain)):
    if block.beforeHash != self.latestBlock().hash:
      return False
    if block.hash != block.calcHash():
      return False
    if self.latestBlock().calcHash() != self.latestBlock().hash:
      print(f"Erro de hash no bloco {i}")
      return False
    if block.timestamp < self.latestBlock().timestamp:
      return False
    if not block.data:
      return False


  return True
 

 def validityAddress(self, address):
    padrao_address = r"^00.*[a-zA-Z0-9]{5}$"
    if re.match(padrao_address, address):
      return True
    else:
      return False


 def newData(self, transmissor, receptor, quantity):
  if not self.validityAddress(transmissor):
    print(f"Erro: O endereço do transmissor {transmissor} não é válido!")
    return 
  if not self.validityAddress(receptor):
    print(f"Erro: O endereço do receptor {receptor} não é válido!")
    return
  self.current_data.append({
    "transmissor": transmissor,
    "receptor": receptor,
    "quantity": quantity
 })


 def searchDataUser(self, user):
  searchTransactions = []

  for block in self.chain:
    if block.index == 0:
      continue
    for address in block.data: 
        if address['transmissor'] == user or address['receptor'] == user:
            searchTransactions.append(address)
  
  return searchTransactions

 def latestBlock(self):
  return self.chain[-1]


 def makeBlock(blockData):
  return Block(blockData.index['index'],
              blockData.hash['hash'],
              blockData.beforeHash['beforeHash'],
              blockData.data['data'],
              blockData.timestamp['timestamp'])

###############################################################


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