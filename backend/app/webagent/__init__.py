"""
WebAgent Integration Module for Qpesapay

This module integrates Alibaba's WebAgent capabilities into the Qpesapay platform,
providing autonomous information seeking and advanced reasoning for financial operations.

Components:
- WebDancer: Multi-turn reasoning agent for complex financial analysis
- WebSailor: Extended thinking agent for regulatory compliance and market research
- Financial Tools: Specialized tools for crypto/fiat market analysis
- Compliance Tools: Automated regulatory monitoring and verification
"""

from .core import WebAgentManager
from .agents import FinancialSearchAgent, ComplianceAgent, MarketAnalysisAgent, DevelopmentAssistantAgent
from .tools import CryptoMarketTool, FiatRatesTool, ComplianceCheckTool, TransactionVerificationTool, DevelopmentAssistantTool
from .config import WebAgentConfig

__all__ = [
    'WebAgentManager',
    'FinancialSearchAgent',
    'ComplianceAgent',
    'MarketAnalysisAgent',
    'DevelopmentAssistantAgent',
    'CryptoMarketTool',
    'FiatRatesTool',
    'ComplianceCheckTool',
    'TransactionVerificationTool',
    'DevelopmentAssistantTool',
    'WebAgentConfig'
]

__version__ = '1.0.0'
