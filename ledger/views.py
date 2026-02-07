from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .blockchain_logic import blockchain
from .models import Wallet, MiningRecord
import json

def index(request):
    """Home page with blockchain overview"""
    chain_data = blockchain.get_chain_data()
    total_blocks = len(chain_data)
    total_transactions = blockchain.get_total_transactions()
    pending_transactions = len(blockchain.pending_transactions)
    
    context = {
        'total_blocks': total_blocks,
        'total_transactions': total_transactions,
        'pending_transactions': pending_transactions,
        'difficulty': blockchain.difficulty,
        'latest_block': chain_data[-1] if chain_data else None,
        'chain_valid': blockchain.is_chain_valid(),
    }
    
    if request.user.is_authenticated:
        try:
            wallet = request.user.wallet
            wallet.update_balance()
            context['wallet'] = wallet
            context['wallet_balance'] = wallet.balance
        except:
            context['wallet'] = None
    
    return render(request, 'index.html', context)

def block_explorer(request):
    """Display all blocks in the blockchain"""
    chain_data = blockchain.get_chain_data()
    
    context = {
        'blocks': chain_data,
        'total_blocks': len(chain_data),
    }
    return render(request, 'blocks.html', context)

def block_detail(request, block_index):
    """Display details of a specific block"""
    try:
        block = blockchain.chain[block_index]
        context = {
            'block': block.to_dict(),
            'transactions': block.transactions,
        }
        return render(request, 'block_detail.html', context)
    except IndexError:
        messages.error(request, f"Block #{block_index} not found")
        return redirect('block_explorer')

@login_required
def create_transaction(request):
    """Create a new transaction"""
    if request.method == 'POST':
        try:
            sender = request.POST.get('sender')
            receiver = request.POST.get('receiver')
            amount = float(request.POST.get('amount'))
            
            if not sender or not receiver:
                messages.error(request, "Sender and receiver are required")
                return redirect('create_transaction')
            
            if amount <= 0:
                messages.error(request, "Amount must be positive")
                return redirect('create_transaction')
            
            tx_id = blockchain.add_transaction(sender, receiver, amount)
            
            messages.success(request, f"Transaction created! TX ID: {tx_id}")
            return redirect('index')
            
        except ValueError as e:
            messages.error(request, f"Invalid input: {str(e)}")
        except Exception as e:
            messages.error(request, f"Error creating transaction: {str(e)}")
    
    user_wallet = None
    if hasattr(request.user, 'wallet'):
        user_wallet = request.user.wallet
    
    context = {
        'user_wallet': user_wallet,
    }
    return render(request, 'create_transaction.html', context)

@login_required
def mine_block(request):
    """Mine a new block"""
    if request.method == 'POST':
        try:
            miner_address = "Anonymous"
            if hasattr(request.user, 'wallet'):
                miner_address = request.user.wallet.address
            else:
                miner_address = request.user.username
            
            new_block = blockchain.mine_pending_transactions(miner_address)
            
            if new_block:
                MiningRecord.objects.create(
                    miner=request.user,
                    block_index=new_block.index,
                    block_hash=new_block.hash,
                    difficulty=blockchain.difficulty,
                    nonce=new_block.nonce
                )
                
                messages.success(request, 
                    f"Block #{new_block.index} mined successfully! "
                    f"Reward: 6.25 coins"
                )
            else:
                messages.warning(request, "No pending transactions to mine")
                
            return redirect('index')
            
        except Exception as e:
            messages.error(request, f"Mining failed: {str(e)}")
    
    pending_tx_count = len(blockchain.pending_transactions)
    
    context = {
        'pending_tx_count': pending_tx_count,
        'difficulty': blockchain.difficulty,
        'block_reward': 6.25,
    }
    return render(request, 'mine_block.html', context)

@login_required
def wallet_view(request):
    """Display user wallet"""
    try:
        wallet = request.user.wallet
        wallet.update_balance()
        
        tx_history = wallet.get_transaction_history()
        
        context = {
            'wallet': wallet,
            'balance': wallet.balance,
            'transaction_history': tx_history,
            'total_transactions': len(tx_history),
        }
        
    except Wallet.DoesNotExist:
        messages.info(request, "You don't have a wallet yet. One will be created for you.")
        wallet = Wallet.objects.create(
            user=request.user,
            address=f"user_{request.user.id}_{request.user.username}",
            public_key=f"pubkey_{request.user.id}",
            private_key=f"privkey_{request.user.id}",
        )
        wallet.update_balance()
        return redirect('wallet')
    
    return render(request, 'wallet.html', context)

def api_blockchain(request):
    """API endpoint for blockchain data"""
    chain_data = blockchain.get_chain_data()
    
    data = {
        'chain': chain_data,
        'length': len(chain_data),
        'pending_transactions': len(blockchain.pending_transactions),
        'difficulty': blockchain.difficulty,
        'valid': blockchain.is_chain_valid(),
    }
    
    return JsonResponse(data)

def api_create_transaction(request):
    """API endpoint to create transaction"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sender = data.get('sender')
            receiver = data.get('receiver')
            amount = float(data.get('amount'))
            
            tx_id = blockchain.add_transaction(sender, receiver, amount)
            
            return JsonResponse({
                'success': True,
                'transaction_id': tx_id,
                'message': 'Transaction added to pending pool'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('index')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})