// Blockchain Explorer JavaScript

// Auto-update blockchain stats every 30 seconds
function updateBlockchainStats() {
    fetch('/api/blockchain/')
        .then(response => response.json())
        .then(data => {
            // Update stats if elements exist
            const totalBlocks = document.getElementById('total-blocks');
            const totalTransactions = document.getElementById('total-transactions');
            const pendingTransactions = document.getElementById('pending-transactions');
            
            if (totalBlocks) totalBlocks.textContent = data.length;
            if (totalTransactions) {
                let txCount = 0;
                data.chain.forEach(block => {
                    txCount += block.transaction_count;
                });
                totalTransactions.textContent = txCount;
            }
            if (pendingTransactions) pendingTransactions.textContent = data.pending_transactions;
        })
        .catch(error => console.error('Error updating stats:', error));
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Start auto-update if on dashboard
    if (window.location.pathname === '/') {
        setInterval(updateBlockchainStats, 30000); // Update every 30 seconds
    }
    
    // Add copy functionality to all code blocks
    document.querySelectorAll('code').forEach(codeBlock => {
        codeBlock.addEventListener('click', function() {
            const text = this.textContent;
            navigator.clipboard.writeText(text).then(() => {
                // Show temporary notification
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                this.style.backgroundColor = '#d4edda';
                
                setTimeout(() => {
                    this.textContent = originalText;
                    this.style.backgroundColor = '';
                }, 1500);
            });
        });
    });
    
    // Mining simulation (for mine page)
    const mineButton = document.querySelector('button[type="submit"]');
    if (mineButton && mineButton.textContent.includes('Mining')) {
        mineButton.addEventListener('click', function(e) {
            // Add mining animation
            this.innerHTML = '<span class="mining-spinner"></span> Mining...';
            this.disabled = true;
            
            // Simulate mining delay
            setTimeout(() => {
                this.innerHTML = '⛏️ Start Mining';
                this.disabled = false;
            }, 3000);
        });
    }
    
    // Transaction form validation
    const transactionForm = document.querySelector('form[action*="create-transaction"]');
    if (transactionForm) {
        transactionForm.addEventListener('submit', function(e) {
            const amount = parseFloat(this.querySelector('input[name="amount"]').value);
            if (amount <= 0) {
                e.preventDefault();
                alert('Amount must be greater than 0');
            }
        });
    }
    
    // Wallet address QR code generation (placeholder)
    const walletAddress = document.querySelector('.wallet-address');
    if (walletAddress) {
        // In a real app, you would generate a QR code here
        console.log('Wallet address:', walletAddress.textContent);
    }
});

// Utility function to format Bitcoin amounts
function formatBTC(amount) {
    return parseFloat(amount).toFixed(8) + ' BTC';
}

// Utility function to format dates
function formatDate(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

// Export for use in console
window.BlockchainUtils = {
    formatBTC,
    formatDate,
    updateBlockchainStats
};