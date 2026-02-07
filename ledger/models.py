from django.db import models
from django.contrib.auth.models import User
from .blockchain_logic import blockchain

class Wallet(models.Model):
    """User wallet for the blockchain"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    address = models.CharField(max_length=100, unique=True)
    public_key = models.TextField(blank=True)
    private_key = models.TextField(blank=True)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0.00000000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Wallet: {self.address[:10]}... ({self.user.username})"
    
    def update_balance(self):
        """Update balance from blockchain"""
        self.balance = blockchain.get_wallet_balance(self.address)
        self.save()
    
    def get_transaction_history(self):
        """Get transaction history from blockchain"""
        return blockchain.get_transaction_history(self.address)

class MiningRecord(models.Model):
    """Record of mined blocks"""
    miner = models.ForeignKey(User, on_delete=models.CASCADE)
    block_index = models.IntegerField()
    block_hash = models.CharField(max_length=64)
    difficulty = models.IntegerField()
    nonce = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    reward = models.DecimalField(max_digits=20, decimal_places=8, default=6.25)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Block #{self.block_index} mined by {self.miner.username}"