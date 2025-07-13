# Prompt Optimizer Quick Reference for Qpesapay Development

## 🚀 Quick Start Commands

```bash
# Windows
scripts\start_prompt_optimizer.bat

# Linux/Mac  
./scripts/start_prompt_optimizer.sh

# Manual setup (first time)
python scripts/setup_prompt_optimizer.py
```

**Access:** http://localhost:8081

## 🎯 Daily Development Workflow

### 1. Start Your Development Session
```bash
# Start Qpesapay backend
cd backend && uvicorn app.main:app --reload

# Start Prompt Optimizer (separate terminal)
scripts\start_prompt_optimizer.bat
```

### 2. Optimize WebAgent Prompts
1. **Copy current prompt** from your code
2. **Open Prompt Optimizer** → http://localhost:8081
3. **Paste prompt** in the input field
4. **Add context**: "Kenya crypto-fiat payment processor, CBK compliance"
5. **Click "Optimize"**
6. **Compare results** side-by-side
7. **Copy optimized prompt** back to your code

### 3. Test and Integrate
```python
# Before (in your WebAgent code)
prompt = "Analyze this crypto transaction"

# After optimization
prompt = """As a Kenya-focused crypto-fiat payment specialist, analyze this transaction considering:
- CBK regulatory requirements and compliance standards
- M-Pesa integration protocols and security measures
- USDT-KES conversion rates and market conditions
- KYC/AML compliance factors and risk assessment

Transaction data: {transaction_data}

Provide analysis in format:
1. Compliance Status: [Compliant/Non-Compliant/Requires Review]
2. Risk Level: [Low/Medium/High]
3. Regulatory Notes: [Specific CBK/CMA considerations]
4. Recommendations: [Action items or approvals needed]"""
```

## 🔧 Configuration

### API Keys Setup
1. **Web Interface**: Settings → Model Management → Add API keys
2. **Environment File**: Edit `development-tools/prompt-optimizer/.env`

```env
VITE_OPENAI_API_KEY=your_openai_key
VITE_GEMINI_API_KEY=your_gemini_key
VITE_DEEPSEEK_API_KEY=your_deepseek_key
ACCESS_PASSWORD=your_dev_password
```

### Recommended Models for Qpesapay
- **GPT-4**: Best for complex financial analysis
- **Gemini 1.5 Pro**: Good for compliance checking
- **DeepSeek**: Cost-effective for development testing

## 📚 Qpesapay Prompt Templates

### Financial Analysis
```
Context: "Kenya crypto-fiat payment processor, CBK compliance required"
Use for: Transaction analysis, risk assessment
```

### Compliance Checking
```
Context: "CBK and CMA regulatory compliance for Kenya financial services"
Use for: KYC/AML verification, regulatory checks
```

### M-Pesa Integration
```
Context: "Safaricom M-Pesa Daraja API integration with security requirements"
Use for: Payment processing, transaction validation
```

### Market Analysis
```
Context: "Kenya crypto market analysis with USDT-KES focus"
Use for: Market conditions, exchange rate analysis
```

## 🎯 Common Use Cases

### Optimizing Existing WebAgent Prompts
1. Find prompt in `backend/app/webagent/agents.py`
2. Copy to Prompt Optimizer
3. Add Qpesapay context
4. Optimize and test
5. Update code with improved prompt

### Creating New AI Features
1. Start with basic prompt in Optimizer
2. Add financial context and requirements
3. Iterate until satisfied
4. Save to prompt library
5. Implement in code

### A/B Testing Prompts
1. Use comparison feature in Optimizer
2. Test with real Qpesapay data
3. Measure accuracy and compliance
4. Choose best performing prompt

## 🛠️ Troubleshooting

### Prompt Optimizer Won't Start
```bash
# Check Docker is running
docker info

# Check port availability
netstat -an | findstr :8081

# Restart services
cd development-tools/prompt-optimizer
docker-compose down && docker-compose up -d
```

### API Connection Issues
1. **Check API keys** in Settings → Model Management
2. **Verify internet connection**
3. **Try different model** if one fails
4. **Check rate limits** on your API accounts

### CORS Issues
- Use **Vercel proxy** option in model settings
- Or deploy your own proxy service
- Check firewall/antivirus blocking requests

## 📊 Performance Tips

### Prompt Quality Metrics
- **Accuracy**: Does it give correct financial analysis?
- **Compliance**: Does it cover CBK/CMA requirements?
- **Specificity**: Is it tailored to Kenya market?
- **Consistency**: Does it produce reliable results?

### Development Best Practices
1. **Save successful prompts** to `backend/prompts/`
2. **Version control** your prompt templates
3. **Test with real data** before production
4. **Document** what works for different use cases
5. **Share** good prompts with your team

## 🔗 Quick Links

- **Web Interface**: http://localhost:8081
- **Chrome Extension**: [Install from Chrome Store](https://chromewebstore.google.com/detail/prompt-optimizer/cakkkhboolfnadechdlgdcnjammejlna)
- **Documentation**: `docs/prompt-optimizer-dev-guide.md`
- **Prompt Library**: `backend/prompts/`
- **Integration Examples**: `examples/prompt_optimization_workflow.py`

## 🆘 Need Help?

1. **Check logs**: `docker-compose logs` in prompt-optimizer directory
2. **Restart services**: `docker-compose restart`
3. **Reset setup**: Delete `development-tools/prompt-optimizer` and run setup again
4. **Review documentation**: `docs/prompt-optimizer-dev-guide.md`

---

**💡 Pro Tip**: Install the Chrome extension for quick access during development. You can optimize prompts without switching between windows!
