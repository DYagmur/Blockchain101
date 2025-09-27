# improved_blockchain.py
import hashlib
import json
import time
import datetime
from typing import List

try:
    from ecdsa import SigningKey, VerifyingKey, NIST384p
    ECDSA_AVAILABLE = True
except Exception:
    ECDSA_AVAILABLE = False

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.signature = None  # base64 hex string

    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
        }

    def calculate_hash(self):
        return hashlib.sha256(json.dumps(self.to_dict(), sort_keys=True).encode()).hexdigest()

    def sign(self, signing_key: 'SigningKey'):
        """Sign the transaction with an ECDSA private key (if available)."""
        if not ECDSA_AVAILABLE:
            raise RuntimeError("ecdsa kütüphanesi yok. `pip install ecdsa` ile kur.")
        if signing_key.get_verifying_key().to_string().hex() != self.sender:
            raise RuntimeError("Bu anahtar bu göndericiye ait değil.")
        sig = signing_key.sign(self.calculate_hash().encode())
        self.signature = sig.hex()

    def is_valid(self):
        """If sender is 'SYSTEM' (mining reward), it's valid by definition."""
        if self.sender == 'SYSTEM':
            return True
        if self.signature is None:
            return False
        if not ECDSA_AVAILABLE:
            # Eğer ecdsa yoksa imza doğrulamasını atla ama uyar.
            print("UYARI: ecdsa yok, imza doğrulaması yapmıyorum.")
            return True
        try:
            vk = VerifyingKey.from_string(bytes.fromhex(self.sender), curve=NIST384p)
            return vk.verify(bytes.fromhex(self.signature), self.calculate_hash().encode())
        except Exception:
            return False

class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[Transaction], previous_hash: str = ''):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions  # list of Transaction
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def to_dict(self, include_hash=True):
        d = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [t.to_dict() for t in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        if include_hash:
            d['hash'] = self.hash
        return d

    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [t.to_dict() for t in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = 3
        self.mempool: List[Transaction] = []  # pending transactions
        self.mining_reward = 50.0

    def create_genesis_block(self):
        genesis_tx = Transaction("SYSTEM", "genesis", 0)
        genesis_block = Block(0, time.time(), [genesis_tx], "0")
        genesis_block.hash = genesis_block.calculate_hash()
        return genesis_block

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
        if not transaction.sender or not transaction.recipient:
            raise ValueError("Transaction must include sender and recipient.")
        if not transaction.is_valid():
            raise ValueError("Transaction is not valid.")
        self.mempool.append(transaction)

    def mine_pending_transactions(self, miner_address: str):
        # include reward tx + up to N transactions (simple selection)
        reward_tx = Transaction("SYSTEM", miner_address, self.mining_reward)
        block_txs = [reward_tx] + self.mempool[:]  # shallow copy
        new_block = Block(self.get_latest_block().index + 1, time.time(), block_txs, self.get_latest_block().hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.mempool = []  # clear mempool; in real systems you'd remove only included txs
        return new_block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            cur = self.chain[i]
            prev = self.chain[i - 1]

            # hash integrity
            if cur.hash != cur.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False

            # previous link
            if cur.previous_hash != prev.hash:
                print(f"Invalid previous_hash at block {i}")
                return False

            # proof of work
            if cur.hash[:self.difficulty] != '0' * self.difficulty:
                print(f"Block {i} hasn't required proof of work.")
                return False

            # transactions valid
            for tx in cur.transactions:
                if not tx.is_valid():
                    print(f"Invalid transaction in block {i}")
                    return False

        return True

    def replace_chain(self, new_chain: List[Block]):
        """Basit: eğer yeni zincir daha uzunsa ve geçerliyse replace et."""
        if len(new_chain) <= len(self.chain):
            return False
        # validate new_chain (must convert raw dicts to Block if needed)
        # burada basit kontrol:
        # (kullanıcı ağ ile entegre ederse bu fonksiyon genişletilmeli)
        self.chain = new_chain
        return True

# --- Usage example ---
def demo():
    bc = Blockchain()
    print("Genesis hash:", bc.chain[0].hash)

    # Eğer ecdsa kuruluysa key çifti oluşturup kullan:
    if ECDSA_AVAILABLE:
        sk = SigningKey.generate(curve=NIST384p)
        vk = sk.get_verifying_key()
        sender_hex = vk.to_string().hex()
        tx1 = Transaction(sender_hex, "recipient_address", 10.0)
        tx1.sign(sk)
    else:
        # ecdsa yoksa 'sender' string olarak basit kullan
        tx1 = Transaction("alice", "bob", 10.0)

    bc.add_transaction(tx1)
    mined = bc.mine_pending_transactions("miner1")
    print("Mined block index:", mined.index, "hash:", mined.hash)

    # Blockchain valid mi?
    print("Valid chain?", bc.is_chain_valid())

    # Tamper testi
    bc.chain[1].transactions[1].amount = 999999  # değişiklik
    print("After tamper, valid?", bc.is_chain_valid())

if __name__ == "__main__":
    demo()
