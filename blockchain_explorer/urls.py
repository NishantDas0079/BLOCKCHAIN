"""blockchain_explorer URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from ledger import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('blocks/', views.block_explorer, name='block_explorer'),
    path('blocks/<int:block_index>/', views.block_detail, name='block_detail'),
    path('create-transaction/', views.create_transaction, name='create_transaction'),
    path('mine/', views.mine_block, name='mine_block'),
    path('wallet/', views.wallet_view, name='wallet'),
    path('api/blockchain/', views.api_blockchain, name='api_blockchain'),
    path('api/create-transaction/', views.api_create_transaction, name='api_create_transaction'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.register, name='register'),
]