import hashlib
import time

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
