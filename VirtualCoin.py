import hashlib
import time
import re
from ecdsa import SECP256k1, SigningKey, VerifyingKey
from ecdsa.util import sigencode_der, sigdecode_der


class Block:
 
 def __init__(self, index, hash, beforeHash, data, timestamp=None, difficulty=4):
  
  self.index = index
  self.hash = hash
  self.beforeHash = beforeHash
  self.data = data
  if self.index == 0:
    self.timestamp = 1734037017
    self.nonce = 100
  else:
    self.timestamp = timestamp or time.time()
    self.nonce = 0
  self.difficulty = difficulty
  self.reward = 0

 def calcHash(self):
    block_data = f"{self.index}{self.beforeHash}{self.data}{self.timestamp}{self.nonce}"
    return hashlib.sha256(block_data.encode('utf-8')).hexdigest()
 
 def mine_block(self):
  while not self.hash.startswith('0' * self.difficulty):
    
    self.nonce += 1
    self.hash = self.calcHash()
  self.reward = 100 if self.index == 0 else self.reward + 25

  for transaction in self.data:
    if not self.index == 0:
      self.reward += transaction.get('cost', 0)
 
 def __str__(self):
  return f"Index-{self.index}\nHASH-{self.hash}\nPREVIOUS HASH-{self.beforeHash}\nDATA-{self.data}\nTIME-{self.timestamp}\nNONCE-{self.nonce}\nResource-{self.reward}"

#######################################################################

class BlockChain:
 
 def __init__(self):
  
  self.chain = []
  self.current_data = []
  self.transaction_history = []
  self.difficulty = 4
  self.genesisBlock()

 def genesisBlock(self):
   self.constructBlock(beforeHash='0', data='Genesis Block!')

 def constructBlock(self, beforeHash, data):
    block = Block(index=len(self.chain), hash='', beforeHash=beforeHash, data=data)
    block.hash = block.calcHash()

    
    block.mine_block()

    if self.is_valid_block(block):
      self.chain.append(block)
      print(f"Bloco {block.index} adicionado com sucesso. Recompensa de {block.reward} Digcoins.\n")

      self.propagate_block(block)
    else:
        print(f"Existe algum empedimento para inserir o bloco {block.index} na BlockChain!")
    
    self.current_data = []
    return block

 def propagate_block(self, block):

  print(f"Node {block.index} propagando bloco...")

  for node in Node.instances:
    if node.blockchain != self:
      node.blockchain.constructBlock(block.beforeHash, block.data)

 def is_valid_block(self, block):
  for i in range(0, len(self.chain)):
    if block.index != len(self.chain):
      return False
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
 

 def is_valid_address(self, address):
    address_pattern = r"[00]{2}.*[a-z]{32}$"
    return bool (re.match(address_pattern, address))


 def newData(self, transmissor, receptor, quantity, wallet=None):
  if not self.is_valid_address(transmissor):
    print(f"Erro: O endereço do transmissor {transmissor} não é válido!")
    return 
  if not self.is_valid_address(receptor):
    print(f"Erro: O endereço do receptor {receptor} não é válido!")
    return

  wallet = self.open_wallet(transmissor, receptor, quantity, wallet or {})
  
  if wallet:
    
    transaction = {
      'transmissor': transmissor,
      'receptor': receptor,
      'quantity': quantity,
      'signature': '',
      'saldo': wallet,
      'cost': 0.0129476
    }
    
    signed_transaction, public_key = self.sign_transaction(transaction)
    if self.validate_transaction(public_key, signed_transaction):
      self.current_data.append(signed_transaction)

  return self.current_data


 def open_wallet(self, owner, receptor, quantity, wallet, cost=0.0129476):

  if not isinstance(wallet, dict):
    print(f"Erro: O parametro wallet recebeu {type(wallet)}")
    return False

  if not wallet.get('owner'):
    wallet['owner'] = owner

  if wallet.get('digcoin') is None or wallet.get('digcoin') == '':
    wallet['digcoin'] = self.get_wallet_balance(owner)
  for block in self.chain[1:]:
    for dado in block.data:
      
      if dado['transmissor'] == wallet['owner']:
        wallet['digcoin'] -= (dado['quantity'] + dado['cost'])

      if dado['receptor'] == wallet['owner']:
        wallet['digcoin'] += dado['quantity']

  if wallet['digcoin'] < (quantity + cost):

    print(f"Error: Valor de {wallet['digcoin']} insuficiente!")
    return False
  
  wallet['digcoin'] -= (quantity + cost)
  wallet['digcoin'] = round(wallet['digcoin'], 2)
  return wallet['digcoin']


 def sign_transaction(self, transaction):

  transaction_data = f"{transaction['transmissor']}{transaction['receptor']}{transaction['quantity']}".encode() 
  message_hash = hashlib.sha256(transaction_data).digest()

  sk = SigningKey.generate(curve=SECP256k1)
  signature = sk.sign(message_hash, sigencode=sigencode_der)
  public_key = sk.get_verifying_key().to_string().hex()

  return {** transaction, 'signature': signature.hex()}, public_key


 def validate_transaction(self, public_key, transaction):

  try:
    tx_data = f"{transaction['transmissor']}{transaction['receptor']}{transaction['quantity']}".encode()
    message_hash = hashlib.sha256(tx_data).digest()

    vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)
    vk.verify(bytes.fromhex(transaction['signature']), message_hash, sigdecode=sigdecode_der)
    print("Assinatura válida!") 
    return True
  except Exception as e:
    print(f"Assinatura inválida! Erro: {e}")
  return False


 def searchDataUser(self, user):
  user_transactions = []

  for block in self.chain[1:]:
    for transaction in block.data:
        if transaction['transmissor'] == user or transaction['receptor'] == user: 
            user_transactions.append(transaction)
  return user_transactions

 def get_wallet_balance(self, user):
  balance = 0
  for block in self.chain[1:]:
    for transaction in block.data:
      if transaction['transmissor'] == user:
        balance = (transaction['saldo']+transaction['cost']+transaction['quantity'])
        balance -= (transaction['quantity']+transaction['cost'])
      if transaction['receptor'] == user:
        balance += transaction['quantity']

  return max(round(balance,2), 0)


 def latestBlock(self):
  return self.chain[-1]


 def makeBlock(blockData):
  return Block(
        index=blockData.index,
        hash=blockData.hash,
        beforeHash=blockData.beforeHash,
        data=blockData.data,
        timestamp=blockData.timestamp,
        difficulty=blockData.difficulty
    )


class Node:
  instances = []

  def __init__(self, id, blockchain):
    self.id = id
    self.blockchain = blockchain
    Node.instances.append(self)

  def resolve_fork(self, other_node):
      print(f"Node {self.id} resolvendo fork...")

      if len(other_node.blockchain.chain) > len(self.blockchain.chain):
          print(f"Node {self.id} adotando cadeia mais longa do Node {other_node.id}.")
          self.blockchain.chain = other_node.blockchain.chain
          self.blockchain.current_data = other_node.blockchain.current_data

          self.synchronize_transactions(other_node)

  def synchronize_transactions(self, other_node):
          print(f"Node {self.id} sincronizando transações com Node {other_node.id}...")
          for block in other_node.blockchain.chain:
              for transaction in block.data:
                  if transaction not in self.blockchain.transaction_history:
                      self.blockchain.transaction_history.append(transaction)

 
######################################################################
if __name__ == "__main__":


    print("##--------------------------------------------------------------##")
    print("##---------------------Começando o DigCoin----------------------##")
    print("")
    print("")

    
    blockchain = BlockChain()
    blockchain1 = BlockChain()

    lastBlock = blockchain.latestBlock()

    blockchain.newData(transmissor="00mnbvmnbbcvxdsfarweqthygdferwkijh",
     receptor="00lpoimnbbcvxdsfarweqthygdferwkijh",
     quantity=25, wallet={'owner': '', 'digcoin': 50})

    blockchain.newData(transmissor="00mkloiuhbcvxdsfarweqthygdferwkijh",
     receptor="00polouibbcmnbvcarweqthygdferwkijh",
     quantity=90, wallet={'owner': '', 'digcoin': 80})

    blockchain.newData(transmissor="00mnbvmnbbcvxdsfarweqthygdnbhgytrf",
     receptor="00mkloiuhbcvxdsfarweqthygdferwkijh",
     quantity=11, wallet={'owner': '', 'digcoin': 15})

    lastHash = lastBlock.calcHash()
    block = blockchain.constructBlock(lastHash, blockchain.current_data)

    lastBlock = blockchain.latestBlock()

    blockchain.newData(transmissor="0User000", receptor="00King00000", 
    quantity=10, wallet={'owner': '', 'digcoin': 50})

    blockchain.newData(transmissor="00polouibbcmnbvcarweqthygdferwkijh", 
    receptor="00mnbvmnbbcvxdsfarweqthygdferwkijh", 
    quantity=25, wallet={'owner': '', 'digcoin': 45})

    blockchain.newData(transmissor="00lpoimnbbcvxdsfarweqthygdferwkijh", 
    receptor="00mkloiuhbcvxdsfarweqthygdferwkijh", 
    quantity=10, wallet={'owner': '', 'digcoin': 60})


    lastHash = lastBlock.calcHash()
    block = blockchain.constructBlock(lastHash, blockchain.current_data)


    lastBlock = blockchain1.latestBlock()

    blockchain1.newData(transmissor="00mnbvmnbbcvxdsfarweqthygdferwkijh",
     receptor="00lpoimnbbcvxdsfarweqthygdferwkijh",
      quantity=25, wallet={'owner': '', 'digcoin': 50})

    blockchain1.newData(transmissor="00mkloiuhbcvxdsfarweqthygdferwkijh",
     receptor="00polouibbcmnbvcarweqthygdferwkijh",
     quantity=90, wallet={'owner': '', 'digcoin': 80})

    blockchain1.newData(transmissor="00mnbvmnbbcvxdsfarweqthygdnbhgytrf",
     receptor="00mkloiuhbcvxdsfarweqthygdferwkijh",
     quantity=11, wallet={'owner': '', 'digcoin': 15})

    lastHash = lastBlock.calcHash()
    block = blockchain1.constructBlock(lastHash, blockchain1.current_data)

    lastBlock = blockchain1.latestBlock()

    blockchain1.newData(transmissor="0User000", receptor="00King00000", 
    quantity=10, wallet={'owner': '', 'digcoin': 50})

    blockchain1.newData(transmissor="00polouibbcmnbvcarweqthygdferwkijh", 
    receptor="00mnbvmnbbcvxdsfarweqthygdferwkijh", 
    quantity=25, wallet={'owner': '', 'digcoin': 45})


    blockchain1.newData(transmissor="00lpoimnbbcvxdsfarweqthygdferwkijh", 
    receptor="00mkloiuhbcvxdsfarweqthygdferwkijh", 
    quantity=13, wallet={'owner': '', 'digcoin': 60})


    lastHash = lastBlock.calcHash()
    block = blockchain1.constructBlock(lastHash, blockchain1.current_data)


    lastBlock = blockchain1.latestBlock()

    blockchain1.newData(transmissor="00mkloiuhbcvxdsfarweqthygdferwkijh", 
    receptor="00polouibbcmnbvcarweqthygdferwkijh", 
    quantity=10, wallet={'owner': '', 'digcoin': ''})


    lastHash = lastBlock.calcHash()
    block = blockchain1.constructBlock(lastHash, blockchain1.current_data)


    node1 = Node(id=1, blockchain=blockchain)
    node2 = Node(id=2, blockchain=blockchain1)

    for block in blockchain.chain:
     print(block,'\n')


    time.sleep(2)
    node1.resolve_fork(node2)
    

    for block in blockchain1.chain:
      print(block, '\n')
    

    # Modifique o endereço para ter novas analises
    user = "00lpoimnbbcvxdsfarweqthygdferwkijh"
    transactions = blockchain1.searchDataUser(user)

    wallet = blockchain1.get_wallet_balance(user)
    print(f"Owner: {user}, Saldo: {wallet} DigCoins.")


    # Exibindo as transações encontradas
    print(f"\nTransações encontradas para o usuário {user}:")
    for address in transactions:
        print(f"Transmissor: {address['transmissor']}, Receptor: {address['receptor']}, Enviados: {address['quantity']}.")

    print("\n##----------------Terminando teste com DigCoin------------------##")
    print("##--------------------------------------------------------------##")
    print("")
    print("")