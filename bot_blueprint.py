"""
AI-Agent Trader - Public Blueprint
A multi-AI synergy trading bot for Solana tokens.
- Smart API Management with Automatic Switching
- AI-Agent Web Browser (Intelligent Browsing)
- Multi-AI Synergy System (Grok, Gemini, Helius, GLM-4.6, DeepSeek, GPT)
- Auto Buy/Sell with Jupiter Integration
- Local DCA Scheduler
- On-chain Monitoring
- DCA, StopLoss, Profit Targets

DISCLAIMER: This is an educational blueprint. Use at your own risk.
The developers are not responsible for any financial losses.
"""

import aiohttp
import asyncio
import json
import time
import logging
import base64
import os
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from solders.keypair import Keypair
from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair as SolKeypair
from solana.transaction import Transaction
from typing import Dict, List, Optional, Tuple, Any
from bs4 import BeautifulSoup
from dataclasses import dataclass

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_agent_trader.log'),
        logging.StreamHandler()
    ]
)

def safe_float(v, default=0.0):
    try:
        return float(v) if v is not None else default
    except Exception:
        return default

@dataclass
class APIConfig:
    name: str
    key: str
    daily_limit: int
    monthly_limit: int
    cost_per_request: float
    strengths: List[str]
    used_today: int = 0
    used_monthly: int = 0
    last_reset_day: int = datetime.now().day

class SmartAPIManager:
    """Smart API Manager - Automatically switches APIs and analyzes costs"""
    
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
        self.apis = self._load_and_encrypt_apis()
        self.usage_log = []

    def _load_and_encrypt_apis(self) -> Dict[str, APIConfig]:
        """Load and encrypt API keys from environment variables"""
        raw_keys = {
            'grok': os.getenv('GROK_API_KEY'),
            'gemini': os.getenv('GEMINI_API_KEY'),
            'helius': os.getenv('HELIUS_API_KEY'),
            'glm': os.getenv('GLM_API_KEY'),
            'deepseek': os.getenv('DEEPSEEK_API_KEY'),
            'gpt': os.getenv('GPT_API_KEY'),
        }
        
        configs = {
            'grok': APIConfig('grok', self._encrypt_key(raw_keys['grok']) if raw_keys['grok'] else '', 100, 3000, 0.002, ['sentiment', 'news_impact', 'social_trends']),
            'gemini': APIConfig('gemini', self._encrypt_key(raw_keys['gemini']) if raw_keys['gemini'] else '', 60, 1800, 0.0015, ['technical_analysis', 'pattern_recognition', 'price_prediction']),
            'helius': APIConfig('helius', self._encrypt_key(raw_keys['helius']) if raw_keys['helius'] else '', 100000, 3000000, 0.0, ['onchain_data', 'holder_analysis', 'transaction_monitoring']),
            'glm': APIConfig('glm', self._encrypt_key(raw_keys['glm']) if raw_keys['glm'] else '', 20000, 600000, 0.0, ['primary_signal', 'risk_assessment', 'final_decision']),
            'deepseek': APIConfig('deepseek', self._encrypt_key(raw_keys['deepseek']) if raw_keys['deepseek'] else '', 50, 1500, 0.001, ['main_signal', 'strategy_optimization', 'decision_making']),
            'gpt': APIConfig('gpt', self._encrypt_key(raw_keys['gpt']) if raw_keys['gpt'] else '', 100, 3000, 0.003, ['market_analysis', 'comprehensive_evaluation', 'strategy_development']),
        }
        return configs

    def _encrypt_key(self, key: str) -> str:
        """Encrypt API key"""
        if not key: return ""
        return self.fernet.encrypt(key.encode()).decode()

    def _decrypt_key(self, encrypted_key: str) -> str:
        """Decrypt API key"""
        if not encrypted_key: return ""
        return self.fernet.decrypt(encrypted_key.encode()).decode()

    def _check_and_reset_limits(self):
        """Check and reset daily/monthly limits"""
        today = datetime.now().day
        for api in self.apis.values():
            if today != api.last_reset_day:
                api.used_today = 0
                api.last_reset_day = today
                logging.info(f"🔄 Daily usage reset for {api.name}")

    def get_best_api_for_task(self, task_type: str, complexity: str = 'medium') -> Optional[str]:
        """Select the best API for a task with cost-benefit analysis"""
        self._check_and_reset_limits()
        
        candidates = []
        for name, config in self.apis.items():
            if task_type in config.strengths and config.used_today < config.daily_limit and config.key:
                strength_score = 10
                usage_score = (config.daily_limit - config.used_today) / config.daily_limit * 10
                cost_score = max(0, 10 - (config.cost_per_request * 1000))
                total_score = strength_score + usage_score + cost_score
                candidates.append((name, total_score))
        
        if not candidates:
            logging.warning(f"⚠️ No available API for task: {task_type}")
            return None
            
        candidates.sort(key=lambda x: x[1], reverse=True)
        best_api_name = candidates[0][0]
        
        self.apis[best_api_name].used_today += 1
        self.apis[best_api_name].used_monthly += 1
        
        logging.info(f"🧠 Using {best_api_name} for task '{task_type}'. Daily usage: {self.apis[best_api_name].used_today}/{self.apis[best_api_name].daily_limit}")
        return best_api_name

    def get_api_key(self, api_name: str) -> str:
        """Get decrypted API key"""
        if api_name in self.apis:
            return self._decrypt_key(self.apis[api_name].key)
        return ""

# ... (The rest of the classes: WebBrowserTool, TradingExecutor, AIAgent, PublicAIAgentTraderBot remain the same as your original code)
# For brevity, I'm not including them all here, but you would copy them from your original script.
# Make sure to rename the main class to PublicAIAgentTraderBot.

class PublicAIAgentTraderBot:
    """Main Public AI-Agent Trader Bot Class"""
    
    def __init__(self, secret_key: bytes, investment_sol: float = 0.1, fee_budget_sol: float = 0.01):
        # ... (All the __init__ code from your original bot)
        # ...
        logging.info(f"🤖 Public AI-Agent Trader Initialized - Wallet: {self.wallet_pubkey}")
        logging.info(f"💰 Investment per trade: {investment_sol} SOL")

    # ... (All other methods like discover_new_tokens, fetch_token_data, run_phoenix_pro remain the same)
    # ...

# Example usage
if __name__ == "__main__":
    # Check if private key is set
    private_key_b64 = os.getenv('PRIVATE_KEY_BASE64')
    if not private_key_b64:
        logging.error("❌ PRIVATE_KEY_BASE64 not found in .env file. Please configure it.")
    else:
        try:
            private_key = base64.b64decode(private_key_b64)
            bot = PublicAIAgentTraderBot(
                secret_key=private_key,
                investment_sol=float(os.getenv('INVESTMENT_SOL', 0.1)),
                fee_budget_sol=float(os.getenv('FEE_BUDGET_SOL', 0.01))
            )
            asyncio.run(bot.run_phoenix_pro())
        except Exception as e:
            logging.error(f"❌ Failed to start bot: {e}")
