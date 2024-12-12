from VirtualCoin import Block
import re

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