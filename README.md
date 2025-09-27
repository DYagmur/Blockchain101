# Python Blockchain Implementation

This repository contains two versions of a simple blockchain implementation in Python:  

1. **Blockchain 101 (Basic Version)** → for understanding the fundamentals.  
2. **Improved Blockchain** → with transactions, mining rewards, proof-of-work validation, and optional digital signatures.  

---

## 📘 Step-by-Step Explanation: Blockchain 101

1. **`Block` class**  
   - Represents a block in the blockchain.  
   - Contains an `index`, `timestamp`, `data`, a `previous_hash`, a `nonce`, and its own `hash`.

2. **`calculate_hash` method**  
   - Combines the block’s index, timestamp, data, previous hash, and nonce.  
   - Uses the SHA-256 hashing algorithm to generate the block’s hash.

3. **`mine_block` method**  
   - Mines a new block by repeatedly calculating the hash and incrementing the nonce.  
   - Continues until the hash meets the **difficulty requirement** (number of leading zeros).

4. **`Blockchain` class**  
   - Represents the blockchain itself.  
   - Initializes with a **genesis block** and sets a difficulty for mining.

5. **`create_genesis_block` method**  
   - Creates the first block in the chain (index `0`, data = `"Genesis Block"`, previous hash = `"0"`).

6. **`get_latest_block` method**  
   - Returns the most recently added block.

7. **`add_block` method**  
   - Links a new block to the latest block by setting its `previous_hash`.  
   - Mines the block until it meets the difficulty requirement.  
   - Appends the mined block to the chain.

8. **`is_chain_valid` method**  
   - Checks blockchain integrity.  
   - Verifies that:  
     - Each block’s hash is correct.  
     - Each `previous_hash` matches the actual hash of the previous block.

9. **Usage Example**  
   - Create a blockchain, add a few blocks, and check validity.  
   - Modify a block’s data to simulate tampering → the blockchain becomes invalid.

---

## 🚀 Simple Blockchain (Improved Version)

This is an **educational blockchain implementation** that extends the basic version with more realistic features.

### ✨ Features

- ✅ Genesis block creation  
- ✅ Proof-of-Work mining (adjustable difficulty)  
- ✅ Transactions (sender, recipient, amount, timestamp)  
- ✅ Mempool (pending transactions)  
- ✅ Mining reward for block creators  
- ✅ Chain validation (hashes, links, PoW, transactions)  
- ✅ Optional **digital signatures** (`ecdsa`) for transaction authenticity  
- ✅ Simple consensus rule: *Longest valid chain wins*  

---

## 🏗️ Classes Overview

### 1. `Transaction`
- Represents a transfer of value between `sender` and `recipient`.  
- Stores `amount` and `timestamp`.  
- Has a `calculate_hash` method for unique ID.  
- Can be **digitally signed** with ECDSA.  

### 2. `Block`
- Contains:
  - `index`
  - `timestamp`
  - `transactions` (list of `Transaction` objects)
  - `previous_hash`
  - `nonce`
  - `hash`
- Uses deterministic JSON (`sort_keys=True`) for hashing.  
- Includes `mine_block(difficulty)` → Proof-of-Work.

### 3. `Blockchain`
- Manages the full chain + pending transactions (mempool).  
- Provides methods:
  - `add_transaction(transaction)` → validates and adds to mempool.  
  - `mine_pending_transactions(miner_address)` → mines a block with pending tx + reward.  
  - `is_chain_valid()` → validates blocks, links, PoW, and signatures.  
  - `replace_chain(new_chain)` → replaces with a longer valid chain.  

---

## 📝 Usage Example

```python
from improved_blockchain import Blockchain, Transaction

# Create blockchain
bc = Blockchain()

# Create a transaction (without signature)
tx1 = Transaction("Alice", "Bob", 10.0)
bc.add_transaction(tx1)

# Mine pending transactions
bc.mine_pending_transactions("Miner1")

print("Blockchain valid?", bc.is_chain_valid())

# Try tampering
bc.chain[1].transactions[1].amount = 999999
print("Valid after tampering?", bc.is_chain_valid())



---

## Optional: Digital Signatures



pip install ecdsa





from improved_blockchain import Transaction
from ecdsa import SigningKey, NIST384p

# Generate private/public key pair
sk = SigningKey.generate(curve=NIST384p)
vk = sk.get_verifying_key()

sender_hex = vk.to_string().hex()

# Create and sign transaction
tx = Transaction(sender_hex, "Bob", 5.0)
tx.sign(sk)

print("Transaction valid?", tx.is_valid())












## ⚠️ Security Notes

This project is for learning purposes only.
It is not secure for production or real money.

Limitations:

No peer-to-peer networking

No persistent storage

Simple consensus (longest chain wins)

No double-spend or Sybil attack protection

🔮 Future Improvements

Merkle Trees for transaction integrity

Peer-to-peer networking (Flask / FastAPI + sockets)

Persistent storage (e.g., SQLite, LevelDB)

Advanced consensus mechanisms (PoS, PBFT, etc.)

Transaction fees & prioritization

Unit tests and fuzz testing
