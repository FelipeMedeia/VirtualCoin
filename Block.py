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
  block_data = f"{self.index}{self.beforeHash}{self.data}{self.timestamp}"
  return hashlib.sha256(block_data.encode()).hexdigest()
 
 def __str__(self):
  return f"Index-{self.index}\nHASH-{self.hash}\nPREVIOUS HASH-{self.beforeHash}\nDATA-{self.data}\nTIME-{self.timestamp}\n"
