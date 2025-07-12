# QPesaPay - Kenya Market Crypto-Fiat Payment Processor

[![CI/CD](https://github.com/yourusername/qpesapay/workflows/CI/badge.svg)](https://github.com/yourusername/qpesapay/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Web-first crypto-fiat payment processor for Kenya** - Accept USDT payments with automatic KES settlement via M-Pesa

## 🚀 Overview

QPesaPay is a comprehensive dual-account payment ecosystem designed specifically for the Kenyan market. It enables merchants to accept USDT payments with automatic KES settlement, while providing personal users with crypto wallet management and M-Pesa integration.

### Key Features

- 💰 **USDT Payment Processing** - Support for Ethereum and Tron networks
- 📱 **M-Pesa Integration** - Automatic KES settlements via Daraja API
- 🏪 **Merchant Dashboard** - Business analytics and payment management
- 👤 **Customer Portal** - Personal crypto wallet management
- 🔒 **Bank-Grade Security** - Field-level encryption and compliance
- 📊 **Real-time Analytics** - Transaction monitoring and reporting

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Customer Portal│    │ Merchant Dashboard│   │   Admin Panel   │
│    (Next.js)    │    │    (Next.js)     │    │    (React)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  FastAPI Backend │
                    │   (Python 3.11) │
                    └─────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ PostgreSQL  │    │    Redis    │    │  External   │
│  Database   │    │   Cache     │    │    APIs     │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 📋 Current Status

**Phase 1 MVP - 40% Complete**

### ✅ Completed
- Backend foundation (FastAPI + SQLAlchemy)
- Database schema and models
- Authentication system structure
- API endpoints framework
- Docker development environment

### 🚧 In Progress
- Core payment processing services
- Blockchain integration (Ethereum/Tron)
- M-Pesa Daraja API integration
- Security implementation

### ❌ Upcoming
- Frontend applications (Customer Portal, Merchant Dashboard)
- Testing suite
- Production deployment
- Performance optimization

## 🛠️ Technology Stack

### Backend
- **FastAPI 0.104.1** - Modern Python web framework
- **SQLAlchemy 2.0.23** - Database ORM with async support
- **PostgreSQL 16** - Primary database
- **Redis 7** - Caching and session management
- **Alembic** - Database migrations

### Security
- **JWT Authentication** - Token-based auth with refresh tokens
- **Bcrypt** - Password hashing
- **Field-level encryption** - Sensitive data protection
- **Rate limiting** - API abuse prevention

### External Integrations
- **M-Pesa Daraja API** - Mobile money integration
- **Ethereum/Tron Networks** - USDT transaction processing
- **Exchange Rate APIs** - Real-time USD/KES conversion

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 16
- Redis 7

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/qpesapay.git
   cd qpesapay
   ```

2. **Set up environment variables**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your configuration
   ```

3. **Start development environment**
   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```

4. **Run database migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

5. **Start the backend server**
   ```bash
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 📚 Documentation

- [Phase 1 MVP Features](Phase%201%20MVP%20Core%20Features.txt) - Detailed feature specifications
- [Project Architecture](crypto-fiat-web-processor.md) - Comprehensive system design
- [Development Rules](GEMINI.md) - Coding standards and guidelines
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (when running)

## 🧪 Testing

```bash
# Run unit tests
cd backend
pytest app/tests/ -v

# Run with coverage
pytest app/tests/ -v --cov=app --cov-report=html
```

## 🔒 Security

This is a financial application with strict security requirements:

- **Never use float for monetary calculations** - Always use Decimal
- **All sensitive data is encrypted** at field level
- **Comprehensive audit logging** for all financial transactions
- **Rate limiting** on all endpoints
- **Input validation** and sanitization
- **KYC/AML compliance** from day one

### ⚠️ Security Notice

**This is open source code for educational and development purposes.**

- 🔒 **Never commit secrets** - All API keys, passwords, and private keys must be in environment variables
- 🔒 **Production deployment** - Use separate private configuration repositories for production
- 🔒 **Environment files** - `.env` files are gitignored and never committed
- 🔒 **Code review** - All changes go through pull request review process
- 🔒 **Dependency scanning** - Regular security audits of dependencies

## 🌍 Kenya Market Focus

- **M-Pesa Integration** - Native mobile money support
- **KES Currency Handling** - Proper Kenyan Shilling support
- **CBK Compliance** - Central Bank of Kenya regulations
- **Local Phone Numbers** - +254 format validation
- **EAT Timezone** - East Africa Time handling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@qpesapay.com
- 📱 WhatsApp: +254700000000
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/qpesapay/issues)

## 🗺️ Roadmap

### Phase 1: MVP (Current)
- Core payment processing
- Basic frontend applications
- M-Pesa integration
- Security implementation

### Phase 2: Enhancement
- Additional payment methods
- Advanced analytics
- Mobile applications
- API marketplace

### Phase 3: Scale
- Multi-country support
- Advanced compliance
- Enterprise features
- White-label solutions

---

**Built with ❤️ for the Kenyan fintech ecosystem**
