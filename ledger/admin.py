from django.contrib import admin
from .models import Wallet, MiningRecord

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'balance', 'created_at')
    search_fields = ('user__username', 'address')
    list_filter = ('created_at',)

@admin.register(MiningRecord)
class MiningRecordAdmin(admin.ModelAdmin):
    list_display = ('miner', 'block_index', 'block_hash', 'difficulty', 'reward', 'timestamp')
    list_filter = ('timestamp', 'difficulty')
    search_fields = ('miner__username', 'block_hash')