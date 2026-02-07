from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ledger.models import Wallet

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Blockchain Dashboard')
    
    def test_block_explorer_view(self):
        response = self.client.get(reverse('block_explorer'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blocks.html')
    
    def test_login_required_views(self):
        # Test views that require login
        protected_urls = [
            reverse('create_transaction'),
            reverse('mine_block'),
            reverse('wallet'),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)
            self.assertRedirects(response, f'/login/?next={url}')
    
    def test_authenticated_views(self):
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('create_transaction'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('wallet'))
        self.assertEqual(response.status_code, 200)
        # Wallet should be auto-created
        self.assertTrue(Wallet.objects.filter(user=self.user).exists())
    
    def test_api_endpoints(self):
        response = self.client.get(reverse('api_blockchain'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        data = response.json()
        self.assertIn('chain', data)
        self.assertIn('length', data)
        self.assertIn('valid', data)