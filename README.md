# Montando uma BlockChain básica

O próposito do desafio é montar uma blockChain simples, para isso usarei a linguagem Python.
Minha atual versão é a **Python 3.12.3** e como IDE pode ser uma dica usar o [VSCode](https://code.visualstudio.com/download).
Para verificar a versão do seu Python, você pode usar o seguinte comando:

 ```
  python --version

```
Caso não tenha uma versão instalada, pode acessar esse link, e preferencialmente, busque por alguma das versões do python 3.
[Python Download](https://www.python.org/downloads/)
Levando em consideração que já está com tudo configurado, e conseguiu fazer o gitClone( Caso tenha alguma dúvida de como conseguir o projeto para teste, dê uma olhada em como clonar um repósitorio, [como fazer um gitclone ](https://docs.github.com/pt/repositories/creating-and-managing-repositories/cloning-a-repository)) deste repósitorio.Após todo o processo, já possiu o python, está usando o VsCode também, ou e qualquer outra IDE, mas está conseguindo acessar o arquivo, pode seguir a diante. Para testar o código basta abrir o terminal do VsCode, por exemplo, e usar o comando a seguir:

```
python VirtualCoin.py

```
Ou pode entrar no arquivo VirtualCoin e no canto superior direito aparecerá um ícone semelhante a um *play* tipo este,  <img src="image.png" alt="play" width="20"/>. Clique nele e o programa irá rodar.


## Falando sobre as linhas do código

### Para contrução usei as Classes:

A classe de bloco para ajudar na contrução dos blocos...

```
  class Block:
 
 # Modelo padrão dos Blocos
 def __init__():
 

 # Função para calcular o hash de cada novo bloco
 def calcHash():
  
 # Função que irá transformar em String
 def __str__():
 
```
Para os blocos temos os seguintes atributos:

```
 def __init__():
  self.index = index
  self.hash = hash
  self.beforeHash = beforeHash
  self.data = data
  self.timestamp = timestamp or time.time()
```
A função hash irá pegar o valor do index, o hash_anterior(beforeHash), os dados(data) referentes as transações e o tempo(timestamp), assim usando a *haslib* irá gerar um hash pra cada bloco:

```
 def calcHash(self):
  block_data = f"{self.index}{self.beforeHash}{self.data}{self.timestamp}"
  return hashlib.sha256(block_data.encode()).hexdigest() 
```
Essa última apenas está transformando em String:

```
 def calcHash(self):
   def __str__(self):
  return "Index-{}\nHASH-{}\nPREVIOUS HASH-{}\nDATA-{}\nTIME-{}\n".format(self.index, self.hash, self.beforeHash, self.data, self.timestamp)
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
Segue o mesmo próposito de iniciar a classe, nessa a chain vai ser a lista encadeada dos blocos, os dados atuais que serão adicionados no bloco e o bloco genesis, que é o primeiro bloco da cadeia.

```
 def __init__(self):
  self.chain = []
  self.current_data = []
  self.genesisBlock()

```
Para a construção dos blocos, o genesis é o primeiro bloco da cadeia e usando a função construct que vai receber os dados do hash do bloco anterior e os dados. Antes de adicionar o bloco vai validar verificando os hashs e o tempo, se tudo estiver correto o bloco será adicionado, se não existe algum problema.


```
 def genesisBlock(self):
   self.constructBlock(beforeHash='0', data='Genesis Block!')

 def constructBlock(self, beforeHash, data):
    # Cria um novo bloco com índice baseado no tamanho atual da cadeia
    block = Block(index=len(self.chain), hash='', beforeHash=beforeHash, data=data)
    block.hash = block.calcHash()

    if self.validityBlockChain(block):
        print(f"Bloco {block.index} adicionado com sucesso.\n")
        self.chain.append(block)
    else:
        print(f"Existe algum empedimento para inserir o bloco {block.index} na BlockChain!")
    
    # Limpa dados atuais, para gerar erro de validação, comentar a parte abaixo
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

```

A função newdata vai adicionar os dados da transação no bloco, recebendo quem maandou, quem vai receber e a quantidade. A função latestBlock vai pegar o último bloco da corrente e a makeBlock vai receber os dados para montar o bloco, passando todos os parametros finais.

```
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

```

## Novas modificações

Para essa nova implementação foi planejado acrescentar um sistema de mineração de blocos semelhante ao PoW, com isso foi adicionado o NONCE e a dificuldade. Também foi alterado a criação do hash, passando o nonce como um atributo.

```
def miner_block(self):
    while not self.hash.startswith('0' * self.difficulty):
        self.nonce += 1
        self.hash = self.calcHash()

```

Foi tmabém adicionado uma regra de validação para os endereços e um sistema de busca simples que mostra uma relação de todas as transações para um endereço que for passado.

```
  # Vai validar os endereços
  def validityAddress(self, address):
    padrao_address = r"^00.*[a-zA-Z0-9]{5}$"
    if re.match(padrao_address, address):
      return True
    else:
      return False


# Vai buscar as transações do endereço
  def searchDataUser(self, user):
  searchTransactions = []

  for block in self.chain:
    if block.index == 0:
      continue
    for address in block.data: 
        if address['transmissor'] == user or address['receptor'] == user:
            searchTransactions.append(address)
  
  return searchTransactions
```