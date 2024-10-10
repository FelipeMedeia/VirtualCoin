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
