from django.test import TestCase
from django.contrib.auth.models import User
from ledger.models import Wallet, MiningRecord

class WalletModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_wallet_creation(self):
        wallet = Wallet.objects.create(
            user=self.user,
            address='test_address_123',
            public_key='test_public_key',
            private_key='test_private_key',
            balance=100.0
        )
        
        self.assertEqual(wallet.user.username, 'testuser')
        self.assertEqual(wallet.address, 'test_address_123')
        self.assertEqual(float(wallet.balance), 100.0)
        self.assertTrue(wallet.created_at)
    
    def test_wallet_string_representation(self):
        wallet = Wallet.objects.create(
            user=self.user,
            address='test_address_123'
        )
        
        self.assertIn('test_address', str(wallet))
        self.assertIn('testuser', str(wallet))

class MiningRecordModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='miner',
            password='minerpass123'
        )
    
    def test_mining_record_creation(self):
        record = MiningRecord.objects.create(
            miner=self.user,
            block_index=1,
            block_hash='0' * 64,
            difficulty=2,
            nonce=12345,
            reward=6.25
        )
        
        self.assertEqual(record.miner.username, 'miner')
        self.assertEqual(record.block_index, 1)
        self.assertEqual(record.difficulty, 2)
        self.assertEqual(float(record.reward), 6.25)
        self.assertTrue(record.timestamp)
    
    def test_mining_record_ordering(self):
        record1 = MiningRecord.objects.create(
            miner=self.user,
            block_index=1,
            block_hash='hash1',
            difficulty=2,
            nonce=100
        )
        
        record2 = MiningRecord.objects.create(
            miner=self.user,
            block_index=2,
            block_hash='hash2',
            difficulty=2,
            nonce=200
        )
        
        records = MiningRecord.objects.all()
        self.assertEqual(records[0].block_index, 2)  # Should be latest first
        self.assertEqual(records[1].block_index, 1)