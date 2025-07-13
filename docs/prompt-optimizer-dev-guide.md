# Prompt Optimizer Development Integration Guide

## 🚀 Quick Setup for Qpesapay Development

### 1. Clone and Setup Prompt Optimizer

```bash
# Navigate to your development tools directory
cd ~/development-tools/  # or wherever you keep dev tools

# Clone the prompt optimizer
git clone https://github.com/linshenkx/prompt-optimizer.git
cd prompt-optimizer

# Quick start with Docker (recommended for development)
docker-compose up -d

# Access at http://localhost:3000
```

### 2. Alternative: Local Development Setup

```bash
# If you prefer local development
cd prompt-optimizer

# Install dependencies
pnpm install

# Start development server
pnpm dev

# Access at http://localhost:5173
```

### 3. Chrome Extension Installation (Recommended for Dev)

1. Download the latest release from GitHub releases
2. Or install from Chrome Web Store: [Prompt Optimizer Extension](https://chromewebstore.google.com/detail/prompt-optimizer/cakkkhboolfnadechdlgdcnjammejlna)
3. Pin the extension to your toolbar for easy access

## 🎯 Development Workflow Integration

### Step 1: Configure API Keys

**Via Web Interface:**
1. Open the prompt optimizer (web or extension)
2. Click "⚙️ Settings" → "Model Management"
3. Configure your development API keys:
   - OpenAI API Key
   - Gemini API Key (if using)
   - DeepSeek API Key (if using)
   - Any custom APIs

**Via Environment Variables (Docker):**
```bash
# Create .env file in prompt-optimizer directory
cat > .env << EOF
VITE_OPENAI_API_KEY=your_openai_api_key
VITE_GEMINI_API_KEY=your_gemini_api_key
VITE_DEEPSEEK_API_KEY=your_deepseek_api_key
ACCESS_PASSWORD=your_dev_password
EOF

# Restart with environment
docker-compose down && docker-compose up -d
```

### Step 2: Create Qpesapay-Specific Prompt Templates

Create a development prompt library for common Qpesapay use cases:

**Financial Analysis Prompts:**
```
Original: "Analyze this crypto transaction"

Optimized: "As a Kenya-focused crypto-fiat payment specialist, analyze this transaction considering CBK regulatory requirements, M-Pesa integration standards, USDT-KES conversion rates, and KYC/AML compliance factors."
```

**Compliance Checking Prompts:**
```
Original: "Check if this transaction is compliant"

Optimized: "Perform comprehensive regulatory compliance analysis for Kenya financial services: 1) Verify against CBK guidelines, 2) Check CMA requirements, 3) Validate KYC/AML procedures, 4) Assess transaction risk factors, 5) Ensure data protection compliance."
```

**Market Analysis Prompts:**
```
Original: "What are the current market conditions?"

Optimized: "Analyze crypto-fiat market conditions for Kenya focusing on: USDT/KES exchange rate trends, M-Pesa transaction volume patterns, regulatory impact on market sentiment, cross-border payment flows, and economic indicators affecting crypto adoption."
```

## 🛠️ Daily Development Usage

### Scenario 1: Optimizing WebAgent Prompts

1. **Open your WebAgent code:**
```python
# backend/app/webagent/agents.py
class FinancialSearchAgent:
    def __init__(self):
        self.base_prompt = "Analyze financial data..."  # Your current prompt
```

2. **Use Prompt Optimizer:**
   - Copy your current prompt
   - Paste into Prompt Optimizer
   - Add context: "Financial analysis for Kenya crypto-fiat payments"
   - Click "Optimize"
   - Compare results side-by-side

3. **Test and Iterate:**
   - Test optimized prompt with real data
   - Use the comparison feature to A/B test
   - Refine based on results

### Scenario 2: Creating New AI Features

When developing new AI-powered features:

1. **Start with basic prompt in Prompt Optimizer**
2. **Add Qpesapay context:**
   - "This is for a Kenya crypto-fiat payment processor"
   - "Must comply with CBK and CMA regulations"
   - "Integrates with M-Pesa payments"

3. **Iterate and optimize:**
   - Use multi-round optimization
   - Test with different models
   - Save successful prompts for reuse

### Scenario 3: Testing Different AI Models

```python
# Test the same prompt across different models
models_to_test = [
    "gpt-4",
    "gpt-3.5-turbo", 
    "gemini-1.5-pro",
    "deepseek-chat"
]

# Use Prompt Optimizer to compare responses
# Document which models work best for different use cases
```

## 📝 Development Best Practices

### 1. Prompt Version Control

Create a prompt library in your project:

```bash
# Create prompt library directory
mkdir -p backend/prompts/
```

```yaml
# backend/prompts/financial_analysis.yaml
name: "Financial Analysis"
version: "1.2"
original: "Analyze this crypto transaction"
optimized: "As a Kenya-focused crypto-fiat payment specialist..."
context: "Used by FinancialSearchAgent for transaction analysis"
models_tested: ["gpt-4", "gemini-1.5-pro"]
performance_notes: "gpt-4 shows 23% better accuracy"
```

### 2. Integration with WebAgent Development

```python
# backend/app/webagent/prompt_templates.py
class QpesapayPromptTemplates:
    """Centralized prompt templates optimized for Qpesapay use cases"""
    
    FINANCIAL_ANALYSIS = """
    As a Kenya-focused crypto-fiat payment specialist, analyze this transaction considering:
    - CBK regulatory requirements
    - M-Pesa integration standards  
    - USDT-KES conversion rates
    - KYC/AML compliance factors
    - Transaction security patterns
    
    Transaction data: {transaction_data}
    """
    
    COMPLIANCE_CHECK = """
    Perform comprehensive regulatory compliance analysis for Kenya financial services:
    1. Verify against CBK guidelines
    2. Check CMA requirements
    3. Validate KYC/AML procedures
    4. Assess transaction risk factors
    5. Ensure data protection compliance
    
    Data to analyze: {compliance_data}
    """
```

### 3. A/B Testing Workflow

```python
# backend/app/services/prompt_testing.py
class PromptTester:
    """A/B test prompts during development"""
    
    async def compare_prompts(self, original: str, optimized: str, test_data: dict):
        """Compare prompt performance"""
        original_result = await self.test_prompt(original, test_data)
        optimized_result = await self.test_prompt(optimized, test_data)
        
        return {
            "original_accuracy": original_result.accuracy,
            "optimized_accuracy": optimized_result.accuracy,
            "improvement": optimized_result.accuracy - original_result.accuracy
        }
```

## 🔧 Advanced Development Techniques

### 1. Automated Prompt Optimization

```python
# backend/scripts/optimize_prompts.py
"""
Script to automatically optimize prompts during development
"""
import requests
import json

class AutoPromptOptimizer:
    def __init__(self, optimizer_url="http://localhost:3000"):
        self.optimizer_url = optimizer_url
    
    def optimize_prompt(self, prompt: str, context: str = "financial"):
        """Automatically optimize prompts via API"""
        # Implementation would call prompt optimizer API
        pass
    
    def batch_optimize_prompts(self, prompt_file: str):
        """Optimize all prompts in a file"""
        # Batch process prompts for efficiency
        pass
```

### 2. Integration with Testing

```python
# backend/app/tests/test_prompt_optimization.py
import pytest
from app.services.prompt_testing import PromptTester

class TestPromptOptimization:
    """Test optimized prompts against original ones"""
    
    @pytest.mark.asyncio
    async def test_financial_analysis_prompt_improvement(self):
        """Test that optimized prompts perform better"""
        tester = PromptTester()
        
        original = "Analyze this crypto transaction"
        optimized = QpesapayPromptTemplates.FINANCIAL_ANALYSIS
        
        result = await tester.compare_prompts(original, optimized, test_data)
        assert result["improvement"] > 0.1  # 10% improvement threshold
```

## 📊 Measuring Prompt Performance

### Key Metrics to Track:

1. **Accuracy**: How often the AI gives correct responses
2. **Relevance**: How well responses match Qpesapay's needs
3. **Compliance**: How well responses adhere to regulations
4. **Speed**: Response time with different prompts
5. **Cost**: Token usage and API costs

### Development Dashboard

Create a simple dashboard to track prompt performance:

```python
# backend/app/utils/prompt_metrics.py
class PromptMetrics:
    """Track prompt performance during development"""
    
    def log_prompt_performance(self, prompt_id: str, metrics: dict):
        """Log performance metrics"""
        pass
    
    def get_best_performing_prompts(self, category: str):
        """Get top performing prompts by category"""
        pass
```

## 🚀 Automated Setup (Recommended)

For the fastest setup, use our automated setup script:

```bash
# Run the automated setup
python3 scripts/setup_prompt_optimizer.py

# Start the prompt optimizer
./scripts/start_prompt_optimizer.sh

# Access at http://localhost:8081
```

This will:
- Clone the prompt optimizer repository
- Create development environment configuration
- Set up Qpesapay-specific prompt templates
- Create helper scripts for daily use

## 🎯 Real-World Development Example

Let's optimize an actual WebAgent prompt from your codebase:

### Before Optimization:
```python
# backend/app/webagent/agents.py - Current code
class FinancialSearchAgent:
    def analyze_transaction(self, transaction_data):
        prompt = f"Analyze this crypto transaction: {transaction_data}"
        return self.llm.generate(prompt)
```

### Development Workflow:

1. **Copy the current prompt** to Prompt Optimizer
2. **Add Qpesapay context**: "This is for a Kenya crypto-fiat payment processor that must comply with CBK regulations"
3. **Click "Optimize"** and review suggestions
4. **Test with real data** using the comparison feature
5. **Update your code** with the optimized prompt

### After Optimization:
```python
# backend/app/webagent/agents.py - Optimized version
class FinancialSearchAgent:
    def analyze_transaction(self, transaction_data):
        prompt = f"""As a Kenya-focused crypto-fiat payment specialist, analyze this transaction considering:
        - CBK regulatory requirements and compliance standards
        - M-Pesa integration protocols and security measures
        - USDT-KES conversion rates and market conditions
        - KYC/AML compliance factors and risk assessment
        - Transaction security patterns and fraud detection

        Transaction data: {transaction_data}

        Provide analysis in format:
        1. Compliance Status: [Compliant/Non-Compliant/Requires Review]
        2. Risk Level: [Low/Medium/High]
        3. Regulatory Notes: [Specific CBK/CMA considerations]
        4. Recommendations: [Action items or approvals needed]"""

        return self.llm.generate(prompt)
```

## 📊 Measuring Improvement

Track the improvement in your development:

```python
# backend/app/utils/prompt_metrics.py
class PromptPerformanceTracker:
    def compare_prompts(self, original_response, optimized_response):
        """Compare prompt performance metrics"""
        return {
            "accuracy_improvement": self.calculate_accuracy_improvement(original_response, optimized_response),
            "compliance_score": self.check_compliance_coverage(optimized_response),
            "specificity_score": self.measure_kenya_market_specificity(optimized_response)
        }
```

## 🎯 Next Steps

1. **Run the automated setup**: `python3 scripts/setup_prompt_optimizer.py`
2. **Start optimizing existing prompts** in your WebAgent code
3. **Create new prompts** using the Qpesapay templates
4. **Integrate into your daily workflow** using the helper scripts
5. **Measure and iterate** on prompt performance

This development integration will significantly improve the quality of your AI features while maintaining the high standards required for financial applications.
