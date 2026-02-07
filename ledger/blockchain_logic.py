import hashlib
import json
import time
from datetime import datetime
from typing import List, Dict, Optional

class Transaction:
    """Represents a single blockchain transaction"""
    
    def __init__(self, sender: str, receiver: str, amount: float, timestamp: float = None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = timestamp or time.time()
        self.transaction_id = self.generate_id()
    
    def generate_id(self) -> str:
        """Generate unique transaction ID"""
        transaction_string = f"{self.sender}{self.receiver}{self.amount}{self.timestamp}"
        return hashlib.sha256(transaction_string.encode()).hexdigest()[:16]
    
    def to_dict(self) -> Dict:
        """Convert transaction to dictionary"""
        return {
            'transaction_id': self.transaction_id,
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __str__(self):
        return f"TX_{self.transaction_id}: {self.sender} → {self.receiver}: {self.amount} BTC"

class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index: int, transactions: List[Transaction], 
                 previous_hash: str, timestamp: float = None):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp or time.time()
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA256 hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2) -> None:
        """Mine block using Proof of Work"""
        print(f"Mining block {self.index}...")
        start_time = time.time()
        
        target = "0" * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        mining_time = time.time() - start_time
        print(f"Block {self.index} mined in {mining_time:.2f} seconds")
        print(f"   Nonce: {self.nonce}")
        print(f"   Hash: {self.hash[:16]}...")
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'hash': self.hash,
            'previous_hash': self.previous_hash,
            'timestamp': datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            'nonce': self.nonce,
            'transaction_count': len(self.transactions),
            'transactions': [tx.to_dict() for tx in self.transactions]
        }
    
    def __str__(self):
        return f"Block #{self.index} [{self.hash[:16]}...] - {len(self.transactions)} transactions"

class Blockchain:
    """Main blockchain class managing the chain"""
    
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self.create_genesis_block()
    
    def create_genesis_block(self) -> None:
        """Create the first block in the chain"""
        genesis_transaction = Transaction(
            sender="0",
            receiver="Genesis",
            amount=0
        )
        
        genesis_block = Block(
            index=0,
            transactions=[genesis_transaction],
            previous_hash="0" * 64,
            timestamp=time.time()
        )
        
        self.chain.append(genesis_block)
        print("Genesis block created")
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_transaction(self, sender: str, receiver: str, amount: float) -> str:
        """Add a new transaction to pending pool"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        transaction = Transaction(sender, receiver, amount)
        self.pending_transactions.append(transaction)
        
        print(f"Transaction added: {transaction}")
        return transaction.transaction_id
    
    def mine_pending_transactions(self, miner_address: str = "System") -> Optional[Block]:
        """Mine all pending transactions into a new block"""
        if not self.pending_transactions:
            print("No pending transactions to mine")
            return None
        
        print(f"\nMining {len(self.pending_transactions)} pending transactions...")
        
        reward_transaction = Transaction(
            sender="0",
            receiver=miner_address,
            amount=6.25
        )
        
        transactions_to_mine = [reward_transaction] + self.pending_transactions
        
        latest_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            transactions=transactions_to_mine,
            previous_hash=latest_block.hash,
            timestamp=time.time()
        )
        
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        
        print(f"Block {new_block.index} added to blockchain!")
        return new_block
    
    def is_chain_valid(self) -> bool:
        """Validate the entire blockchain"""
        print("\nValidating blockchain...")
        
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {current_block.index}: Invalid hash")
                return False
            
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {current_block.index}: Invalid previous hash")
                return False
            
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"Block {current_block.index}: Invalid proof of work")
                return False
        
        print("Blockchain is valid!")
        return True
    
    def get_chain_data(self) -> List[Dict]:
        """Get entire chain as list of dictionaries"""
        return [block.to_dict() for block in self.chain]
    
    def get_total_transactions(self) -> int:
        """Get total number of transactions in blockchain"""
        total = 0
        for block in self.chain:
            total += len(block.transactions)
        return total
    
    def get_wallet_balance(self, address: str) -> float:
        """Calculate balance for a wallet address"""
        balance = 0.0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.receiver == address:
                    balance += transaction.amount
                if transaction.sender == address and transaction.sender != "0":
                    balance -= transaction.amount
        
        return balance
    
    def get_transaction_history(self, address: str) -> List[Dict]:
        """Get all transactions for a specific address"""
        history = []
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address or transaction.receiver == address:
                    history.append({
                        'block_index': block.index,
                        **transaction.to_dict()
                    })
        
        return history

# Singleton blockchain instance
blockchain = Blockchain(difficulty=2)