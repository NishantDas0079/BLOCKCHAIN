import hashlib
import json
import time
from datetime import datetime

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate SHA256 hash of the block contents"""
        block_string = json.dumps({
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """Mine block with Proof of Work"""
        print(f"Mining block {self.index}...")
        start_time = time.time()
        
        # Create target string with leading zeros (based on difficulty)
        target = "0" * difficulty
        
        # Keep changing nonce until hash meets difficulty requirement
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        mining_time = time.time() - start_time
        print(f"Block {self.index} mined in {mining_time:.2f} seconds")
        print(f"  Nonce: {self.nonce}")
        print(f"  Hash: {self.hash}")
        return True
    
    def to_dict(self):
        """Convert block to dictionary for display"""
        return {
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce
        }

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.pending_transactions = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first (genesis) block"""
        print("Creating Genesis Block...")
        genesis_block = Block(0, ["Genesis Transaction"], time.time(), "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        print("Genesis block created!\n")
    
    def get_last_block(self):
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_transaction(self, transaction):
        """Add a new transaction to pending list"""
        self.pending_transactions.append(transaction)
        print(f"Added transaction: {transaction}")
    
    def mine_pending_transactions(self):
        """Mine all pending transactions into a new block"""
        if not self.pending_transactions:
            print("No pending transactions to mine!")
            return False
        
        print(f"\nMining {len(self.pending_transactions)} pending transactions...")
        
        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.pending_transactions.copy(),
            timestamp=time.time(),
            previous_hash=last_block.hash
        )
        
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        
        # Clear pending transactions
        self.pending_transactions = []
        
        print(f"Block {new_block.index} added to blockchain!")
        return True
    
    def is_chain_valid(self):
        """Validate the entire blockchain"""
        print("\nValidating blockchain...")
        
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                print(f"ERROR: Block {current_block.index} hash is invalid!")
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                print(f"ERROR: Block {current_block.index} has wrong previous hash!")
                return False
            
            # Check Proof of Work
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"ERROR: Block {current_block.index} doesn't meet difficulty requirement!")
                return False
        
        print("Blockchain is valid!")
        return True
    
    def display_chain(self):
        """Display the entire blockchain"""
        print("\n" + "="*60)
        print("BLOCKCHAIN LEDGER")
        print("="*60)
        
        for block in self.chain:
            block_data = block.to_dict()
            print(f"\nBlock #{block_data['index']}")
            print(f"  Timestamp: {block_data['timestamp']}")
            print(f"  Transactions: {block_data['transactions']}")
            print(f"  Previous Hash: {block_data['previous_hash'][:20]}...")
            print(f"  Hash: {block_data['hash']}")
            print(f"  Nonce: {block_data['nonce']}")
            print("-"*40)
        
        print(f"\nTotal Blocks: {len(self.chain)}")
        print("="*60)

def main():
    print("="*60)
    print("SIMPLE BLOCKCHAIN WITH PROOF OF WORK")
    print("="*60)
    
    # 1. Create blockchain with difficulty 2 (start with 2 zeros)
    print("\n1. Initializing blockchain with difficulty 2...")
    blockchain = Blockchain(difficulty=2)
    
    # 2. Add some transactions
    print("\n2. Adding transactions...")
    blockchain.add_transaction("Alice -> Bob: 50 BTC")
    blockchain.add_transaction("Bob -> Charlie: 25 BTC")
    blockchain.add_transaction("Charlie -> David: 10 BTC")
    
    # 3. Mine pending transactions into a block
    blockchain.mine_pending_transactions()
    
    # 4. Add more transactions
    print("\n3. Adding more transactions...")
    blockchain.add_transaction("David -> Eve: 5 BTC")
    blockchain.add_transaction("Eve -> Alice: 2 BTC")
    
    # 5. Mine second block
    blockchain.mine_pending_transactions()
    
    # 6. Display the blockchain
    blockchain.display_chain()
    
    # 7. Validate the chain
    if blockchain.is_chain_valid():
        print("\nBLOCKCHAIN VALIDATION SUCCESSFUL!")
    else:
        print("\nBLOCKCHAIN VALIDATION FAILED!")
    
    # 8. Demonstrate tamper detection
    print("\n" + "="*60)
    print("TAMPER DETECTION DEMONSTRATION")
    print("="*60)
    
    print("\nAttempting to tamper with block 1...")
    blockchain.chain[1].transactions = ["Alice -> Bob: 500 BTC"]  # Tamper!
    
    if not blockchain.is_chain_valid():
        print("\nTAMPER DETECTED! Blockchain is invalid after tampering.")
    
    print("\n" + "="*60)
    print("BLOCKCHAIN DEMONSTRATION COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()