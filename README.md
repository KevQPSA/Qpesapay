# Qpesapay

Web-first crypto-fiat payment processor for the Kenya market.

## Overview

Qpesapay enables seamless conversion between cryptocurrency (USDT) and Kenyan Shillings through M-Pesa integration, providing a secure and efficient payment gateway for businesses and individuals.

## Technology Stack

- **Backend**: FastAPI, PostgreSQL, Redis
- **Authentication**: JWT with bcrypt
- **Payments**: M-Pesa Daraja API
- **Blockchain**: Ethereum, Tron, Bitcoin
- **Infrastructure**: Docker, Nginx

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/KevQPSA/Qpesapay.git
   cd Qpesapay
   ```

2. **Set up environment**
   ```bash
   cp backend/.env.example backend/.env
   # Configure your environment variables
   ```

3. **Start services**
   ```bash
   docker-compose -f docker/docker-compose.yml up -d
   ```

4. **Run migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

5. **Access the application**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## Development

**Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

**Run tests:**
```bash
pytest app/tests/ -v --cov=app
```

**Code quality:**
```bash
ruff check app/ --fix
mypy app/
black app/
```

## License

MIT
