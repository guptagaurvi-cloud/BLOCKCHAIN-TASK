#Importing libraries
import hashlib
import time
from datetime import datetime

#Creating block for Blockchain
class Block:

  def __init__(self,index,data,prev_hash):
    
    #Block properties initialisation
    self.index = index
    self.data = data
    self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    self.previous_hash = prev_hash
    self.nonce = 0
    self.hash = self.calculate_hash()

  def calculate_hash(self):

    transactions = "".join(self.data)

    #Generate SHA 256 hash for block
    block_hash = (
    transactions + 
    str(self.timestamp)+
    str(self.index)+
    str(self.nonce)+
    self.previous_hash )

    return hashlib.sha256(block_hash.encode()).hexdigest()
  
  
  def mine_block(self,difficulty):

    #Mine block using Proof Of Work
    print(f"\nMining Block {self.index}...")
     
    while not self.hash.startswith("0"*difficulty):
      self.nonce += 1
      self.hash = self.calculate_hash()
    
    print("Transactions:")
    for transaction in self.data:
      print("->",transaction)
    print("Nonce found:", self.nonce)
    print("Hash:",self.hash)
    print("================================================================================================================")

#Creating Blockchain
class Blockchain:

  def __init__(self):
    self.difficulty = int(input("Enter difficulty: "))
    print("\nMining difficulty:",self.difficulty)
    print("Valid hashes must start with:","0"*self.difficulty)
    print("================================================================================================================")
    self.chain = [self.genesis_block()]

  #Creating first block of Blockchain
  def genesis_block(self):
    genesis = Block(0,["Genesis Block"],"0")
    genesis.mine_block(self.difficulty)
    return genesis
  
  #Adding and linking the blocks in Blockchain
  def add_block(self,block):
    block.previous_hash = self.chain[-1].hash
    block.mine_block(self.difficulty)
    self.chain.append(block)

  #Blockchain Validation
  def chain_valid(self):
    for i in range(1,len(self.chain)):
      current_block = self.chain[i]
      previous_block = self.chain[i-1]
    
      if current_block.hash != current_block.calculate_hash():
        return False
      
      if current_block.previous_hash != previous_block.hash:
        return False
      
      if not current_block.hash.startswith("0"*self.difficulty):
        return False
      
    return True
    
  def print_blockchain_valid(self):
    print("\nBlockchain valid:",self.chain_valid())
    print("================================================================================================================")
    

my_blockchain = Blockchain()

block1 = Block(1,
    ["A pays B 5 BTC",
     "B pays C 2 BTC"],
     "")

block2 = Block(2,
    ["C pays D 1 BTC",
     "D pays E 3 BTC"],
    "")

block3 = Block(3,
    ["D pays A 4 BTC",
     "E pays B 2 BTC"],
    "")

block4 = Block(4,
    ["C pays E 1 BTC"],
    "")

my_blockchain.add_block(block1)
my_blockchain.add_block(block2)
my_blockchain.add_block(block3)
my_blockchain.add_block(block4)

my_blockchain.print_blockchain_valid()


# If we tamper the transaction(s)
print("\nOriginal data:",my_blockchain.chain[2].data)
my_blockchain.chain[2].data = ["A pays E"]
print("\nIf data is tampered...")
print("\nModified data:",my_blockchain.chain[2].data)

#Checking if still Blockchain valid 
my_blockchain.print_blockchain_valid()
