# Blockchain Engineering Fundamentals

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Solidity](https://img.shields.io/badge/solidity-0.8+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/coverage-95%25-green.svg)

> Production-grade blockchain implementation with cryptographic primitives, consensus algorithms, and smart contract development.

## 🏗️ Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│ Application Layer │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Smart Contracts │ │
│ └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Consensus Layer │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ PoW │ │ PoS │ │ pBFT │ │ PoET │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Blockchain Layer │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Distributed Ledger │ │
│ │ (Blocks + Transactions + State) │ │
│ └─────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Cryptography Layer │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│ │ SHA256 │ │ ECDSA │ │ Merkle │ │ ZK-SNARK │ │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
└─────────────────────────────────────────────────────────────┘

```

# Requirements
```

## 📦 Quick Start

### Prerequisites
```bash
# System Requirements
- Python 3.9+
- Node.js 16+
- Docker (optional)
- Git

# Install Foundational Tools
pip install poetry          # Modern Python dependency management
npm install -g hardhat      # Ethereum development environment
npm install -g ganache-cli  # Local blockchain
```

# Installation
```
# Clone repository
git clone https://github.com/yourusername/blockchain-engineering-fundamentals.git
cd blockchain-engineering-fundamentals

# Install Python dependencies
poetry install

# Install Node.js dependencies
npm install

# Setup development environment
scripts/setup_environment.sh
```

# Run Core Implementations
```
# 1. SHA256 Cryptographic Engine
poetry run python src/cryptography/sha256_engine.py

# 2. Blockchain Implementation with Proof-of-Work
poetry run python src/blockchain/chain.py

# 3. Deploy SimpleToken Contract
npx hardhat run scripts/deploy.js --network localhost
```

# 🧪 Test Suite
```
# Run all tests with coverage
poetry run pytest tests/ --cov=src --cov-report=html

# Run specific test suites
poetry run pytest tests/test_cryptography.py -v
poetry run pytest tests/test_blockchain.py -v

# Test smart contracts
npx hardhat test
```


