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
    self.reward = 100 if self.index == 0 else self.reward +25

    for transaction in self.data:
      if not self.index == 0:
        self.reward += transaction.get('cost', 0)
 
 def __str__(self):
  return f"Index-{self.index}\nHASH-{self.hash}\nPREVIOUS HASH-{self.beforeHash}\nDATA-{self.data}\nTIME-{self.timestamp}\nNONCE-{self.nonce}\nResource-{self.reward}"

####################################################################

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
    else:
        print(f"Existe algum empedimento para inserir o bloco {block.index} na BlockChain!")
    
    self.current_data = []
    return block

 def is_valid_block(self, block):
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

  if not wallet.get('owner'):
    wallet['owner'] = owner

  if wallet.get('digcoin') is None:
    wallet['digcoin'] = 0.0

  if wallet.get('digcoin') == '':
    wallet['digcoin'] = self.get_wallet_balance(owner)

  for block in self.chain[1:]:
    for dado in block.data:
      if dado['transmissor'] == wallet['owner']:
        wallet['digcoin'] -= dado['quantity']

      if dado['receptor'] == wallet['owner']:
        wallet['digcoin'] += dado['quantity']

  if wallet['digcoin'] < (quantity + cost):
    print(f'Error: Valor de {wallet['digcoin']} insuficiente!')
    return False
  
  wallet['digcoin'] -= (quantity + cost)
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
    tx_data = f'{transaction['transmissor']}{transaction['receptor']}{transaction['quantity']}'.encode()
    message_hash = hashlib.sha256(tx_data).digest()

    vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=SECP256k1)
    vk.verify(bytes.fromhex(transaction['signature']), message_hash, sigdecode=sigdecode_der)
    print("Assinatura válida!") 
    return True
  except Exception as e:
    print("Assinatura inválida! Erro: {e}")
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
        balance -= (transaction['quantity']+transaction['cost'])
      if transaction['receptor'] == user:
        balance += transaction['quantity']

  return max(balance, 0)


 def latestBlock(self):
  return self.chain[-1]


 def makeBlock(blockData):
  return Block(blockData.index['index'],
              blockData.hash['hash'],
              blockData.beforeHash['beforeHash'],
              blockData.data['data'],
              blockData.timestamp['timestamp'],
              blockData.resource['resource'])

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