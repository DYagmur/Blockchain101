import hashlib
import datetime

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


# Usage example
blockchain = Blockchain()

# Adding blocks to the blockchain
blockchain.add_block(Block(1, datetime.datetime.now(), {"amount": 4}, ""))
blockchain.add_block(Block(2, datetime.datetime.now(), {"amount": 10}, ""))
blockchain.add_block(Block(3, datetime.datetime.now(), {"amount": 8}, ""))

# Checking if the blockchain is valid
print("Is blockchain valid? ", blockchain.is_chain_valid())

# Modifying data in a block (tampering)
blockchain.chain[1].data = {"amount": 100}

# Rechecking validity after tampering
print("Is blockchain valid after tampering? ", blockchain.is_chain_valid())
