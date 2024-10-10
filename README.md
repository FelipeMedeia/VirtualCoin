# Making a Virtual Coin

For test this simple experiment do you need use a python language. 
My Python Version is **Python 3.12.3**
for verify your, use:
 ```
  python --version

```
For test this code use:

```
python VirtualCoin.py

```

### Para contrução usei as Classes:

Bloco para ajudar na contrução dos blocos...

```
  class Block:
 
 # Modelo padrão dos Blocos
 def __init__():
 

 # Função para calcular o hash de cada novo bloco
 def calcHash():
  
 # Função que irá transformar em String
 def __str__():
 
```
E a classe Bockchain para a montagem da Blockchain simples.

```
# Classe da estrutura da nossa Blockhain
class BlockChain:
 

 # Modelo da blockchain 
 def __init__(self):




 # Essa função irá criar o Primeiro Bloco, ou Genesis Block
 def genesisBlock(self):




 # Aqui é onde os Blocos são montados
 def constructBlock(self, beforeHash, data):





 # Aqui os Blocos serão validados
 def validityBlockChain(self, block, beforeBlock):


 
 # Aqui dados serão adicionados ao Bloco
 def newData(self, transmisor, receptor, quantity):



 def latestBlock(self):




 def add_blocks(self, details):
   



 def makeBlock(blockData):



```