# Montando uma BlockChain básica - Atualização em Todo o documento, atividade final

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

Para a contrução do bloco foi seguido um contexto de que o ele possuiria um index, um valor de hash, o hash do bloco anterior, os dados referente as transações, o momento da criação, nonce que será abordado na simulação de mineração juntamente com a dificuldade e por ultimo foi colocado o atributo referente a recompensa. Com isso a classe do bloco é composta pelo seu construtor, por uma função que irá calcular o hash, por uma que irá simular a mineração e uma que irá transformar o retorno em string.

A função hash irá pegar o valor do index, o hash_anterior(beforeHash), os dados(data) referentes as transações e o tempo(timestamp), assim usando a *haslib* irá gerar um hash pra cada bloco e a mine_block irá simular uma mineração desses blocos, para isso ela foi reescrita para que além de usar um sistema parecido com o PoW, com uma dificuldade e nonce, foi adicionado uma recompensa para cada bloco de 25 digcoins + a taxa, que é o valor que custa para cada transação (nesse caso, levando em consideração que cada bloco tem até 3 transações e a taxa fosse de 0.01 o bloco no final teria uma reward de 25 + 3*cost).

```
 def calcHash(self):
  block_data = f"{self.index}{self.beforeHash}{self.data}{self.timestamp}{self.nonce}"
  return hashlib.sha256(block_data.encode('utf-8')).hexdigest() 

  def mine_block(self):
  while not self.hash.startswith('0' * self.difficulty):
    
    self.nonce += 1
    self.hash = self.calcHash()

  self.reward = 100 if self.index == 0 else self.reward + 25

  if self.index !=0:
    for transaction in self.data:
      self.reward += transaction.get('cost', 0)
```
Essa a seguir apenas está retornando em String:

```
 def __str__(self):
  return f"Index-{self.index}\nHASH-{self.hash}\nPREVIOUS HASH-{self.beforeHash}\nDATA-{self.data}\nTIME-{self.timestamp}\nNONCE-{self.nonce}"

```

E a classe Bockchain para a montagem da Blockchain simples.

Segue o mesmo próposito de iniciar a classe, nessa a chain vai ser a lista encadeada dos blocos, os dados atuais que serão adicionados no bloco, e o bloco genesis, que é o primeiro bloco da cadeia.


Para a construção dos blocos, o genesis é o primeiro bloco da cadeia e usando a função construct que vai receber os dados do hash do bloco anterior e os dados. Antes de adicionar o bloco vai validar verificando os critérios para validação, se tudo estiver correto o bloco será adicionado, para isso as validações foram adicionadas, e para simulação de propagação, foi implementado a função propagate_block, que irá compartilhar com todos os outros nós quando um novo bloco for adicionado, nesse exemplo existe a propagação dos blocos para dois nós.


Seguindo teremos a função ` def is_valid_block(self, block) ` que irá analisar os blocos, se os dados para validação e se são consistentes, no final tem a função que valida os endereços ` def is_valid_address(self, address) `, assim ela estará montando um padrão para os endereços que são aceitos nessa blockchain.

A função newdata vai adicionar os dados da transação no bloco, recebendo quem mandou, quem vai receber e a quantidade. A função latestBlock vai pegar o último bloco da corrente e a makeBlock vai receber os dados para montar o bloco, passando todos os parametros finais.
Como uma adição agora em codigo final temos também a assinatura, algo similar à uma carteira e o custo que será debitado para cada transação relalizada pelo endereço em questão. E a função que valida as transações, que esta logo a seguir é onde, caso os dados estão corretos e 'válidos', será a transação então assinada, permitindo assim avaçar para sua inclusão ao bloco.


## Outras modificações

Foi também reorganizada a busca simples que mostra uma relação de todas as transações para um endereço que for passado. E outra que mostra a carteira, seguindo um passo só, no código ao escolher o user=endereço para busca, ambas as funções usarão o mesmo dado para trazer uma resposta.


# Vai buscar as transações do endereço

  ```
   def searchDataUser(self, user):
    user_transactions = []

    for block in self.chain[1:]:
      for transaction in block.data:
          if transaction['transmissor'] == user or transaction['receptor'] == user: 
              user_transactions.append(transaction)
    return user_transactions


  def get_wallet_balance(self, user):
    for transaction in self.transaction_history:
      for dado in self.chain[1:]:
        for tx in dado.data:
          if transaction['owner'] == user and tx['transmissor'] == user:
            transaction['digcoin'] -= (tx['cost']+tx['quantity'])

          if tx['receptor'] == user and transaction['owner'] == user:
            transaction['digcoin'] += (tx['cost']+tx['quantity'])


    return max(round(transaction['digcoin'],2), 0)
```

E por fim a class Node, que é basicamente a responsável pela propagação da blockchain e pelo tratamento de fork, ou seja, quando tiverem duas blockchains identicas, a com a cadeia maior prevalecerá, para isso também a função irá sincronixar os dados.


  ```
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
```