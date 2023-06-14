# A step-by-step explanation of the provided "Blockchain 101" implementation

1. The Block class represents a block in the blockchain. Each block contains an index, a timestamp, some data, a hash of the previous block, a nonce (a random number used in mining), and its own hash.

2. The calculate_hash method calculates the hash of the block by combining the index, timestamp, data, previous hash, and nonce using the SHA-256 hashing algorithm.

3. The mine_block method is responsible for mining a new block. It repeatedly calculates the hash of the block and increments the nonce until the hash meets a certain difficulty requirement. In this implementation, the difficulty is defined as the number of leading zeros the hash must have.

4. The Blockchain class represents the blockchain itself. It initializes with a genesis block (the first block) and a difficulty level for mining new blocks.

5. The create_genesis_block method creates the first block in the blockchain with an index of 0, the current timestamp, the string "Genesis Block" as data, and a previous hash of "0".

6. The get_latest_block method returns the most recently added block in the blockchain.

7. The add_block method adds a new block to the blockchain. It sets the previous hash of the new block to the hash of the latest block, then mines the new block by repeatedly calculating the hash until it meets the difficulty requirement. Finally, it appends the new block to the chain.

8. The is_chain_valid method checks the validity of the entire blockchain. It iterates over each block starting from the second block (since the first block is the genesis block) and verifies that the hash of each block is valid and that the previous hash matches the hash of the previous block.

9. Usage example: The code creates a Blockchain instance and adds three blocks to it. Each block contains a unique index, the current timestamp, and some data. After adding the blocks, it checks the validity of the blockchain using the is_chain_valid method. It then modifies the data of the second block to simulate tampering and checks the validity again to show that the tampering is detected.
