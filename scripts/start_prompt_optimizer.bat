@echo off
REM Start Prompt Optimizer for Qpesapay development (Windows)

echo 🚀 Starting Prompt Optimizer for Qpesapay development...

REM Get script directory and project root
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set OPTIMIZER_DIR=%PROJECT_ROOT%\development-tools\prompt-optimizer

REM Check if setup has been run
if not exist "%OPTIMIZER_DIR%" (
    echo ❌ Prompt Optimizer not found. Running setup first...
    python "%SCRIPT_DIR%setup_prompt_optimizer.py"
)

cd /d "%OPTIMIZER_DIR%"

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  No .env file found. Creating basic configuration...
    (
        echo # Basic configuration - add your API keys
        echo VITE_OPENAI_API_KEY=
        echo VITE_GEMINI_API_KEY=
        echo ACCESS_USERNAME=qpesapay-dev
        echo ACCESS_PASSWORD=dev123
    ) > .env
    echo 📝 Created .env file. Please add your API keys.
)

REM Start services
echo 🐳 Starting Docker containers...

REM Use custom compose file if it exists, otherwise use default
if exist "docker-compose.qpesapay.yml" (
    docker-compose -f docker-compose.yml -f docker-compose.qpesapay.yml up -d
) else (
    docker-compose up -d
)

REM Wait a moment for services to start
timeout /t 5 /nobreak >nul

REM Check if service is running
curl -s http://localhost:8081 >nul 2>&1
if errorlevel 1 (
    echo ❌ Failed to start Prompt Optimizer. Check Docker logs:
    docker-compose logs
) else (
    echo ✅ Prompt Optimizer started successfully!
    echo.
    echo 🌐 Web Interface: http://localhost:8081
    echo 🔧 Admin Access: qpesapay-dev / dev123 (or check .env file)
    echo.
    echo 💡 Quick Tips:
    echo    - Configure API keys in Settings → Model Management
    echo    - Use templates from backend/prompts/ directory
    echo    - Install Chrome extension for easier access
    echo    - Check docs/prompt-optimizer-dev-guide.md for usage guide
    echo.
    echo 🛑 To stop: docker-compose down
    echo.
    echo Opening web interface...
    start http://localhost:8081
)

pause
