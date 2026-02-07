# Blockchain Core: Technical Foundations (Units 1-3)

## 🏗️ Architectural Components

### 1. Cryptographic Primitives
#### Hash Functions (SHA256)
Input → Padding (to 512 bits) → Message Schedule → 64 Compression Rounds → Output (256 bits)

Properties:

Deterministic: H(x) = y always

Pre-image Resistance: Given y, hard to find x where H(x) = y

Collision Resistance: Hard to find x₁ ≠ x₂ where H(x₁) = H(x₂)

Avalanche Effect: Δinput → Δ~50% output bits

Fixed Output: Always 256 bits


#### Merkle Trees
```
           Root Hash
          /         \
         /           \
    Hash(AB)       Hash(CD)
    /      \       /      \
Hash(A)  Hash(B) Hash(C) Hash(D)
```

Properties:

Efficient verification: O(log n) proof size

Tamper evidence: Root changes if any leaf changes

Bitcoin: SPV (Simplified Payment Verification)


#### Digital Signatures (ECDSA)

Sign: s = k⁻¹(z + rd) mod n
Verify: R' = (s⁻¹z)G + (s⁻¹r)*Q

Where:

d: Private key (256-bit)

Q: Public key (d*G)

k: Ephemeral key (random)

z: Hash of message


### 2. Block Structure
```python
class BlockHeader:
    version: uint32           # Block version (4 bytes)
    prev_block_hash: bytes32  # Previous block hash (32 bytes)
    merkle_root: bytes32      # Merkle root of transactions (32 bytes)
    timestamp: uint32         # Unix timestamp (4 bytes)
    bits: uint32              # Difficulty target (4 bytes)
    nonce: uint32             # Proof-of-Work nonce (4 bytes)
    # Total: 80 bytes
    
class Block:
    header: BlockHeader
    transaction_count: varint
    transactions: List[Transaction]
```

# 3. Network Protocol (Bitcoin P2P)
```
Message Structure:
┌──────────┬──────────────┬────────────┬────────────┐
│ Magic    │ Command      │ Length     │ Checksum   │
│ (4 bytes)│ (12 bytes)   │ (4 bytes)  │ (4 bytes)  │
└──────────┴──────────────┴────────────┴────────────┘
│ Payload (variable length)                         │
└───────────────────────────────────────────────────┘

Protocol Messages:
- version: Handshake initiation
- verack: Acknowledgment
- inv: Inventory advertisement
- getdata: Request specific data
- tx: Transaction propagation
- block: Block propagation
```

# 4. Transaction Lifecycle
```
1. Creation: User creates unsigned transaction
2. Signing: ECDSA signature with private key
3. Propagation: Broadcast to P2P network
4. Validation: Nodes verify (signature, double-spend, format)
5. Mempool: Valid transactions wait for inclusion
6. Mining: Miner includes in block
7. Confirmation: Block added to chain (6 confirmations = ~1 hour)
```

# ⚙️ Consensus Algorithms
# Proof of Work (Bitcoin)
```
Mathematical Problem:
Find nonce such that: SHA256(SHA256(block_header)) < target

Difficulty Adjustment:
new_target = old_target * (actual_time / expected_time)

Security: 51% attack requires controlling >50% of network hash rate
Energy: ~150 TWh/year (more than Argentina)
```

# Proof of Stake (Ethereum 2.0)
```
Validator Selection:
Probability ∝ Stake * Time

Finality:
- Casper FFG: Checkpoints every 100 blocks
- LMD-GHOST: Fork choice rule

Advantages:
- Energy efficient
- Reduced centralization risk
- Native slashing conditions
```

# Byzantine Fault Tolerance (Hyperledger)
```
╔═══════════════════════╦════════════════════╦════════════════════╦════════════════════╗
║      Algorithm        ║   Finality Time    ║   Throughput       ║   Energy/Validator ║
╠═══════════════════════╬════════════════════╬════════════════════╬════════════════════╣
║ Bitcoin PoW           ║ 60 minutes (99.9%) ║ 7 TPS              ║ 100-150 kWh/tx     ║
║ Ethereum PoS          ║ 12-15 minutes      ║ 15-45 TPS          ║ 0.0026 kWh/tx      ║
║ Solana PoH+PoS        ║ ~400 ms            ║ 65,000 TPS         ║ Negligible         ║
║ Hyperledger pBFT      ║ < 1 second         ║ 3,000 TPS          ║ Negligible         ║
╚═══════════════════════╩════════════════════╩════════════════════╩════════════════════╝
```

# 📝 Smart Contracts
# Ethereum Virtual Machine
```
Stack Machine: 1024 elements, 256-bit words
Memory: Byte-addressable, volatile
Storage: Key-value store, persistent
Gas: Computation pricing (21000 base, 4-800 per opcode)

Opcode Examples:
- ADD: 3 gas
- SHA3: 30 + 6 per word
- SSTORE: 20,000 (zero→non-zero)
- CREATE: 32,000
```

# Solidity Patterns
```solidity
// 1. Access Control
contract AccessControl {
    mapping(address => bool) private _admins;
    
    modifier onlyAdmin() {
        require(_admins[msg.sender], "Not admin");
        _;
    }
}

// 2. Reentrancy Protection
contract NonReentrant {
    bool private _locked;
    
    modifier nonReentrant() {
        require(!_locked, "Reentrant call");
        _locked = true;
        _;
        _locked = false;
    }
}

// 3. Gas Optimization
contract Optimized {
    // Pack small variables
    uint128 public var1;
    uint128 public var2;
    
    // Use immutable for constants
    address public immutable owner;
    
    // Use bytes32 instead of string for fixed data
    bytes32 public constant SYMBOL = "TOKEN";
}
```

# Token Standards
```solidity
// ERC-20 Interface
interface IERC20 {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

// ERC-721 Interface (NFTs)
interface IERC721 {
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);
    
    function balanceOf(address owner) external view returns (uint256 balance);
    function ownerOf(uint256 tokenId) external view returns (address owner);
    function safeTransferFrom(address from, address to, uint256 tokenId) external;
    function transferFrom(address from, address to, uint256 tokenId) external;
    function approve(address to, uint256 tokenId) external;
    function setApprovalForAll(address operator, bool approved) external;
    function getApproved(uint256 tokenId) external view returns (address operator);
    function isApprovedForAll(address owner, address operator) external view returns (bool);
}
```

# Layer 2 Scaling Solutions
```
Rollups:
- Optimistic: Assume validity, challenge if fraud
- ZK-Rollups: Validity proofs with zero-knowledge cryptography

Sidechains:
- Independent blockchains with two-way pegs
- Example: Polygon PoS chain

State Channels:
- Off-chain transaction channels
- On-chain settlement only for disputes
```

# Zero-Knowledge Proofs
```
zk-SNARKs:
Prover: P(statement, witness) → proof
Verifier: V(statement, proof) → true/false

Applications:
- Private transactions (Zcash)
- Scalable rollups (zkSync, StarkNet)
- Identity proofs
```

# Cross-Chain Interoperability
```
1. Atomic Swaps:
   - Hash Time-Locked Contracts (HTLCs)
   - Trustless token exchange

2. Bridges:
   - Lock-and-mint: Lock on Chain A, mint on Chain B
   - Liquidity networks: Liquidity pools on both chains

3. Oracles:
   - Chainlink: Decentralized data feeds
   - Band Protocol: Cross-chain data oracle
```

# 📊 Performance Metrics & Optimization
# Gas Optimization Techniques
```
Storage:
- Use packing: Combine multiple uints into one storage slot
- Use immutable for constants: Saves 20,000 gas per read
- Use constant for compile-time values: No storage needed

Memory:
- Use calldata for external function parameters
- Use memory for internal function arrays

Computation:
- Use != 0 instead of > 0 for unsigned integers
- Cache array length
- Use unchecked for safe arithmetic
```

# Blockchain Metrics
```
Bitcoin (2024):
- Block time: 10 minutes (target)
- Block size: 1-4 MB (actual)
- Transactions per block: 2000-4000
- Hash rate: 400-500 EH/s
- Difficulty: 80+ trillion

Ethereum (2024):
- Block time: 12 seconds
- Gas limit: 30 million per block
- Average TPS: 15-30
- Validators: 800,000+
- APR: 3-5%
```

# Tools & Frameworks

Development: Hardhat, Foundry, Brownie

Security: Slither, Mythril, Echidna

Testing: Waffle, Truffle, Chai

Monitoring: The Graph, Dune Analytics, Tenderly

# 🎯 Key Takeaways
# Technical Competencies

Cryptography: Implement SHA256, understand ECDSA, build Merkle trees

Consensus: Compare PoW, PoS, pBFT, implement mining algorithm

Smart Contracts: Write secure Solidity, understand gas optimization

Architecture: Design scalable blockchain systems

# Production Considerations

Security: Audit contracts, use established libraries, implement access control

Scalability: Consider Layer 2 solutions, sharding, sidechains

Interoperability: Plan for cross-chain compatibility

Compliance: Understand regulatory requirements
