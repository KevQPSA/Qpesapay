CRUCIAL!!!

Start with Martin Fowler - His "Patterns of Enterprise Application Architecture" is crucial for payment systems. You'll need patterns like Transaction Script, Domain Model, and Gateway patterns for handling financial transactions and external integrations.
Eric Evans' Domain-Driven Design is essential because payment processing involves complex business rules around currencies, exchange rates, compliance, and settlement. DDD helps you model these financial domains accurately and handle the intricate business logic.
Robert C. Martin's "Clean Architecture" becomes critical for payment systems because you need clear separation between your core business logic and external dependencies (blockchain networks, banking APIs, regulatory systems). The dependency inversion principle is vital when dealing with multiple external services.
Add Vaughn Vernon's "Implementing Domain-Driven Design" - This builds on Evans with practical implementation guidance, especially around event sourcing and CQRS, which are valuable for financial audit trails and handling high transaction volumes.
Michael Nygard's "Release It!" - This focuses on production-ready systems, fault tolerance, and resilience patterns. Payment processors can't afford downtime, so you need circuit breakers, timeouts, and graceful degradation.
Security-focused reading would include resources on cryptographic implementations and secure coding practices, though these might be more specialized texts than general software engineering books.
The financial domain demands extreme reliability, auditability, and regulatory compliance - so architecture and domain modeling become more critical than in typical applications.
-  Embody Sandi Metz principles and all of the above like your life depends on it. ALWAYS!!!


### 🔄 Project Awareness & Context & Research
-  
- **Always read `PLANNING.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `TASK.md`** before starting a new task. If the task isn’t listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `PLANNING.md`.
- **Use Docker commands** whenever executing Python commands, including for unit tests.
- **Set up Docker** Setup a docker instance for development and be aware of the output of Docker so that you can self improve your code and testing.
- **Create a homepage** - The first task after setting up the docker environment is to create a homepage for the project. This should be a clean system with var variables, a theme, and should also be mobile friendly. This will include human relay - where we will create a homepage together until I'm happy with the result. You can create any SVGs, animations, anything you deem fit, just ensure that it looks good, clean, modern, and follows the design system.
- **LLM Models** - Always look for the models page from the documentation links mentioned below and find the model that is mentioned in the initial.md - do not change models, find the exact model name to use in the code.
- **Always scrape around 30-100 pages in total when doing research**
- **Take my tech as sacred truth, for example if I say a model name then research that model name for LLM usage - don't assume from your own knowledge at any point** 
- **For Maximum efficiency, whenever you need to perform multiple independent operations, such as research, invole all relevant tools simultaneously, rather that sequentially.**

### 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **When creating AI prompts do not hardcode examples but make everything dynamic or based off the context of what the prompt is for**
- **Agents should be designed as intelligent human beings** by giving them decision making, ability to do detailed research using Jina, and not just your basic propmts that generate absolute shit. This is absolutely vital.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
  For agents this looks like:
    - `agent.py` - Main agent definition and execution logic 
    - `tools.py` - Tool functions used by the agent 
    - `prompts.py` - System prompts
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use python_dotenv and load_env()** for environment variables.

### 🧪 Testing & Reliability
- **Always create Pytest unit tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
  - Include at least:
    - 1 test for expected use
    - 1 edge case
    - 1 failure case

### ✅ Task Completion
- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a “Discovered During Work” section.

### 📎 Style & Conventions
- **Use Python** as the primary language.
- **Follow PEP8**, use type hints, and format with `black`.
- **Use `pydantic` for data validation**.
- Use `FastAPI` for APIs and `SQLAlchemy` or `SQLModel` for ORM if applicable.
- Write **docstrings for every function** using the Google style:
  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.
      """
  ```

### 📚 Documentation & Explainability
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

### 🧠 AI Behavior Rules
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.

### Design

- Stick to the design system inside designsystem.md Designsystem.md - must be adhered to at all times for building any new features.

### 🏦 Financial System Specific Rules

#### Security & Compliance
- **NEVER hardcode private keys, API keys, or sensitive credentials** - always use environment variables
- **Implement proper encryption** for all sensitive data at rest and in transit
- **Use multi-signature wallets** for business accounts and large transactions
- **Implement proper audit logging** - every financial transaction must be logged with immutable records
- **Follow PCI DSS compliance** guidelines for handling payment data
- **Implement KYC/AML checks** from day one - never skip compliance requirements
- **Use rate limiting** aggressively to prevent abuse and attacks
- **Implement proper input validation** and sanitization for all financial data

#### Financial Data Handling
- **Use Decimal type** for all currency calculations - NEVER use float for money
- **Implement proper rounding** using banker's rounding for financial calculations
- **Handle currency precision** correctly (USDT: 6 decimals, KES: 2 decimals)
- **Implement idempotency** for all payment operations using unique transaction IDs
- **Use database transactions** for multi-step financial operations
- **Implement proper rollback mechanisms** for failed transactions
- **Validate all amounts** are positive and within acceptable ranges

#### Kenyan Market Specific
- **M-Pesa integration** - follow Daraja API patterns exactly
- **Pesapal/Pesalink** - implement proper webhook handling
- **CBK compliance** - ensure all operations comply with Central Bank regulations
- **Time zones** - handle EAT (East Africa Time) properly
- **Phone number format** - validate Kenyan phone numbers (+254 format)
- **KES currency** - handle Kenyan Shilling properly (no cents in practice)

#### Blockchain/Crypto Specific
- **Gas fee estimation** - always estimate and handle gas fees properly
- **Transaction confirmation** - wait for proper confirmations before processing
- **Network selection** - support both Ethereum and Tron networks for USDT
- **Wallet security** - use HD wallets and proper key derivation
- **Block reorganization** - handle blockchain reorgs gracefully
- **Transaction monitoring** - implement proper blockchain monitoring

#### Testing Financial Systems
- **Use testnet** for all blockchain testing - NEVER use mainnet in tests
- **Mock external APIs** in unit tests but have integration tests with real APIs
- **Test failure scenarios** extensively - network failures, API timeouts, etc.
- **Implement chaos engineering** for financial systems
- **Test currency conversion** edge cases and rate fluctuations
- **Load testing** - test with realistic transaction volumes

#### Monitoring & Alerting
- **Real-time monitoring** for all financial transactions
- **Alert on suspicious activities** - unusual amounts, frequency, patterns
- **Monitor exchange rates** and alert on significant fluctuations
- **Track settlement times** and alert on delays
- **Monitor wallet balances** and alert on low funds
- **System health monitoring** - database, API health, etc.
