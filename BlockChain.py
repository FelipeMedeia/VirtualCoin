from VirtualCoin import Block

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
        print(f"Bloco {block.index} adicionado com sucesso.\n")
        self.chain.append(block)
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