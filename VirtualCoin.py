import hashlib
import time


class Block:
 
 # Modelo padrão dos Blocos
 def __init__(self, index, hash, beforeHash, data, timestamp=None):
  
  self.index = index
  self.hash = hash
  self.beforeHash = beforeHash
  self.data = data
  self.timestamp = timestamp or time.time()

 # Função para calcular o hash de cada novo bloco
 def calcHash(self):
  block_data = f"{self.beforeHash}{self.data}{self.timestamp}"
  return hashlib.sha256(block_data.encode()).hexdigest()
 
 def __str__(self):
  return "Index-{}\nHASH-{}\nPREVIOUS HASH-{}\nDATA-{}\nTIME-{}\n".format(self.index, self.hash, self.beforeHash, self.data, self.timestamp)
  
# Classe da estrutura da nossa Blockhain
class BlockChain:
 
 # Modelo da blockchain 
 def __init__(self):
  
  self.chain = []
  self.current_data = []
  self.genesisBlock()

 # Essa função irá criar o Primeiro Bloco, ou Genesis Block
 def genesisBlock(self):
   self.constructBlock(beforeHash='0', data='Genesis Block!')

 # Aqui é onde os Blocos são montado
 def constructBlock(self, beforeHash, data):
    # Cria um novo bloco com índice baseado no tamanho atual da cadeia
    block = Block(index=len(self.chain), hash='', beforeHash=beforeHash, data=data)
    block.hash = block.calcHash()

    # Verifica a validade antes de adicionar
    if self.validityBlockChain(block):
        self.chain.append(block)
        print(f"Bloco {block.index} adicionado com sucesso.\n")
    else:
        print(f"Existe algum empedimento para inserir o bloco {block.index} na BlockChain!")
    
    # Limpa dados atuais, para gerar erro de validação, comentar a parte abaixo
    self.current_data = []

    return block
 

 # Aqui os Blocos serão validados
 def validityBlockChain(self, block):
  for i in range(1, len(self.chain)):
    if block.beforeHash != self.latestBlock().hash:
      return False
    if self.latestBlock().calcHash() != self.latestBlock().hash:
      return False
    if block.timestamp < self.latestBlock().timestamp:
      return False
  
  return True
 
  # Aqui dados serão adicionados ao Bloco
 def newData(self, transmisor, receptor, quantity):
  
  self.current_data.append({'transmisor': transmisor, 'receptor': receptor, 'quantity': quantity})

  return True

 def latestBlock(self):
  return self.chain[-1]
  

 def makeBlock(blockData):
   return Block(blockData.index['index'],
                blockData.hash['hash'],
                blockData.beforeHash['beforeHash'],
                blockData.data['data'],
                blockData.timestamp['timestamp'])
  

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