"""
Development Assistant Tool - WebAgent for Development Workflows
"""

import asyncio
import ast
import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class DevelopmentAssistantTool:
    """
    Development Assistant Tool using WebAgent capabilities
    
    Provides intelligent assistance for:
    - Test completion and generation
    - Code analysis and suggestions
    - Bug detection and fixes
    - Documentation generation
    - API testing and validation
    """
    
    def __init__(self, config: Any):
        self.config = config
        self.name = "dev_assistant"
        self.project_root = Path.cwd()
        
    async def analyze_test_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze test file and identify incomplete implementations"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            analysis = {
                "file_path": file_path,
                "incomplete_tests": [],
                "missing_implementations": [],
                "suggestions": [],
                "test_coverage_gaps": []
            }
            
            # Parse AST to find incomplete functions
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check for functions with just 'pass'
                    if (len(node.body) == 1 and 
                        isinstance(node.body[0], ast.Pass)):
                        analysis["incomplete_tests"].append({
                            "function_name": node.name,
                            "line_number": node.lineno,
                            "docstring": ast.get_docstring(node),
                            "suggested_implementation": await self._suggest_test_implementation(node, content)
                        })
                    
                    # Check for TODO comments
                    if any("TODO" in line or "FIXME" in line 
                          for line in content.split('\n')[node.lineno-1:node.end_lineno]):
                        analysis["missing_implementations"].append({
                            "function_name": node.name,
                            "line_number": node.lineno,
                            "type": "todo_comment"
                        })
            
            # Analyze test coverage gaps
            analysis["test_coverage_gaps"] = await self._analyze_coverage_gaps(content)
            
            # Generate suggestions
            analysis["suggestions"] = await self._generate_test_suggestions(content, analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze test file {file_path}: {e}")
            return {"error": str(e)}
    
    async def _suggest_test_implementation(self, node: ast.FunctionDef, content: str) -> str:
        """Suggest implementation for incomplete test function"""
        function_name = node.name
        docstring = ast.get_docstring(node) or ""
        
        # Analyze function name and docstring to suggest implementation
        if "audit_trail" in function_name.lower():
            return self._generate_audit_trail_test()
        elif "rate_limiting" in function_name.lower():
            return self._generate_rate_limiting_test()
        elif "security" in function_name.lower():
            return self._generate_security_test()
        elif "validation" in function_name.lower():
            return self._generate_validation_test()
        else:
            return self._generate_generic_test(function_name, docstring)
    
    def _generate_audit_trail_test(self) -> str:
        """Generate audit trail test implementation"""
        return '''
        """Test that all payment operations are properly audited."""
        # Arrange
        payment_request = PaymentRequest(
            user_id="test-user-123",
            amount=Money(Decimal("100.00"), Currency.USDT),
            recipient_address="0x742d35Cc6634C0532925a3b8D4C9db4C4C4b4C4C",
            currency=Currency.USDT,
            network="ethereum",
            priority="standard"
        )
        
        # Mock audit logger
        audit_logger = Mock()
        payment_processor = CryptoPaymentProcessor(audit_logger=audit_logger)
        
        # Act
        with patch.object(payment_processor, '_validate_payment', return_value=True):
            with patch.object(payment_processor, '_process_blockchain_transaction'):
                payment_processor.process_payment(payment_request, "test-key")
        
        # Assert - Verify all required audit events
        required_audit_calls = [
            'log_payment_initiated',
            'log_validation_completed', 
            'log_blockchain_transaction_started',
            'log_payment_completed'
        ]
        
        for call_name in required_audit_calls:
            assert hasattr(audit_logger, call_name), f"Missing audit method: {call_name}"
            getattr(audit_logger, call_name).assert_called()
        
        # Verify audit log contains required fields
        audit_calls = audit_logger.method_calls
        for call in audit_calls:
            call_args = call[1] if len(call) > 1 else []
            call_kwargs = call[2] if len(call) > 2 else {}
            
            # Check required audit fields
            required_fields = ['timestamp', 'user_id', 'transaction_id', 'amount', 'status']
            audit_data = call_kwargs.get('audit_data', {})
            
            for field in required_fields:
                assert field in audit_data, f"Missing audit field: {field}"
        '''
    
    def _generate_rate_limiting_test(self) -> str:
        """Generate rate limiting test implementation"""
        return '''
        """Test that payment processing respects rate limits."""
        from app.core.rate_limiter import RateLimiter
        from app.core.exceptions import RateLimitExceededError
        
        # Arrange
        rate_limiter = RateLimiter(max_requests=5, time_window=60)  # 5 requests per minute
        payment_processor = CryptoPaymentProcessor(rate_limiter=rate_limiter)
        
        payment_request = PaymentRequest(
            user_id="test-user-123",
            amount=Money(Decimal("100.00"), Currency.USDT),
            recipient_address="0x742d35Cc6634C0532925a3b8D4C9db4C4C4b4C4C",
            currency=Currency.USDT,
            network="ethereum",
            priority="standard"
        )
        
        # Act & Assert - Test rate limit enforcement
        with patch.object(payment_processor, '_validate_payment', return_value=True):
            with patch.object(payment_processor, '_process_blockchain_transaction'):
                
                # Should succeed for first 5 requests
                for i in range(5):
                    result = payment_processor.process_payment(
                        payment_request, f"test-key-{i}"
                    )
                    assert result is not None
                
                # 6th request should be rate limited
                with pytest.raises(RateLimitExceededError) as exc_info:
                    payment_processor.process_payment(payment_request, "test-key-6")
                
                assert "Rate limit exceeded" in str(exc_info.value)
                assert "5 requests per minute" in str(exc_info.value)
        
        # Test rate limit reset after time window
        with patch('time.time', return_value=time.time() + 61):  # Advance time by 61 seconds
            result = payment_processor.process_payment(payment_request, "test-key-7")
            assert result is not None  # Should succeed after reset
        '''
    
    def _generate_security_test(self) -> str:
        """Generate security test implementation"""
        return '''
        """Test security validations and input sanitization."""
        # Test SQL injection prevention
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'/*",
            "' UNION SELECT * FROM users --"
        ]
        
        for malicious_input in malicious_inputs:
            with pytest.raises(ValidationError) as exc_info:
                PaymentRequest(
                    user_id=malicious_input,
                    amount=Money(Decimal("100"), Currency.USDT),
                    recipient_address="0x742d35Cc6634C0532925a3b8D4C9db4C4C4b4C4C",
                    currency=Currency.USDT,
                    network="ethereum",
                    priority="standard"
                )
            assert "Invalid input detected" in str(exc_info.value)
        
        # Test XSS prevention
        xss_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "';alert('xss');//"
        ]
        
        for xss_input in xss_inputs:
            with pytest.raises(ValidationError):
                PaymentRequest(
                    user_id=f"user-{xss_input}",
                    amount=Money(Decimal("100"), Currency.USDT),
                    recipient_address="0x742d35Cc6634C0532925a3b8D4C9db4C4C4b4C4C",
                    currency=Currency.USDT,
                    network="ethereum",
                    priority="standard"
                )
        
        # Test path traversal prevention
        path_traversal_inputs = [
            "../../etc/passwd",
            "..\\\\windows\\\\system32\\\\config\\\\sam",
            "/etc/shadow",
            "C:\\\\Windows\\\\System32\\\\drivers\\\\etc\\\\hosts"
        ]
        
        for path_input in path_traversal_inputs:
            with pytest.raises(ValidationError):
                PaymentRequest(
                    user_id=f"user-{path_input}",
                    amount=Money(Decimal("100"), Currency.USDT),
                    recipient_address="0x742d35Cc6634C0532925a3b8D4C9db4C4C4b4C4C",
                    currency=Currency.USDT,
                    network="ethereum",
                    priority="standard"
                )
        '''
    
    def _generate_validation_test(self) -> str:
        """Generate validation test implementation"""
        return '''
        """Test comprehensive input validation."""
        # Test amount validation
        invalid_amounts = [
            Decimal("-100"),      # Negative amount
            Decimal("0"),         # Zero amount
            Decimal("0.0000001"), # Too small for currency precision
            Decimal("999999999999999999999"), # Too large
        ]
        
        for invalid_amount in invalid_amounts:
            with pytest.raises(ValidationError) as exc_info:
                PaymentRequest(
                    user_id="test-user",
                    amount=Money(invalid_amount, Currency.USDT),
                    recipient_address="0x742d35Cc6634C0532925a3b8D4C9db4C4C4b4C4C",
                    currency=Currency.USDT,
                    network="ethereum",
                    priority="standard"
                )
            assert "Invalid amount" in str(exc_info.value)
        
        # Test address validation
        invalid_addresses = [
            "invalid_address",
            "0x123",  # Too short
            "0xGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",  # Invalid hex
            "",  # Empty
            None,  # None
        ]
        
        for invalid_address in invalid_addresses:
            with pytest.raises(ValidationError):
                PaymentRequest(
                    user_id="test-user",
                    amount=Money(Decimal("100"), Currency.USDT),
                    recipient_address=invalid_address,
                    currency=Currency.USDT,
                    network="ethereum",
                    priority="standard"
                )
        
        # Test currency validation
        with pytest.raises(ValidationError):
            PaymentRequest(
                user_id="test-user",
                amount=Money(Decimal("100"), Currency.USDT),
                recipient_address="0x742d35Cc6634C0532925a3b8D4C9db4C4C4b4C4C",
                currency="INVALID_CURRENCY",
                network="ethereum",
                priority="standard"
            )
        '''
    
    def _generate_generic_test(self, function_name: str, docstring: str) -> str:
        """Generate generic test implementation"""
        return f'''
        """
        {docstring or f"Test implementation for {function_name}"}
        """
        # Arrange
        # TODO: Set up test data and mocks
        
        # Act
        # TODO: Execute the functionality being tested
        
        # Assert
        # TODO: Verify expected behavior
        assert True  # Replace with actual assertions
        '''
    
    async def _analyze_coverage_gaps(self, content: str) -> List[Dict[str, Any]]:
        """Analyze test coverage gaps"""
        gaps = []
        
        # Look for missing test scenarios
        if "test_edge_cases" not in content:
            gaps.append({
                "type": "missing_edge_case_tests",
                "description": "No edge case tests found",
                "suggestion": "Add tests for boundary conditions and edge cases"
            })
        
        if "test_error_handling" not in content:
            gaps.append({
                "type": "missing_error_tests",
                "description": "No error handling tests found",
                "suggestion": "Add tests for error conditions and exception handling"
            })
        
        if "test_performance" not in content:
            gaps.append({
                "type": "missing_performance_tests",
                "description": "No performance tests found",
                "suggestion": "Add performance and load tests"
            })
        
        return gaps
    
    async def _generate_test_suggestions(self, content: str, analysis: Dict[str, Any]) -> List[str]:
        """Generate test improvement suggestions"""
        suggestions = []
        
        if analysis["incomplete_tests"]:
            suggestions.append(
                f"Complete {len(analysis['incomplete_tests'])} incomplete test functions"
            )
        
        if "mock" not in content.lower():
            suggestions.append(
                "Consider adding more mocking for external dependencies"
            )
        
        if "parametrize" not in content:
            suggestions.append(
                "Use pytest.mark.parametrize for testing multiple scenarios"
            )
        
        if "fixture" not in content:
            suggestions.append(
                "Add more pytest fixtures for better test organization"
            )
        
        return suggestions
    
    async def generate_test_completion(self, file_path: str, function_name: str) -> str:
        """Generate complete test implementation for specific function"""
        try:
            analysis = await self.analyze_test_file(file_path)
            
            # Find the specific incomplete test
            target_test = None
            for test in analysis.get("incomplete_tests", []):
                if test["function_name"] == function_name:
                    target_test = test
                    break
            
            if not target_test:
                return f"Function {function_name} not found or already implemented"
            
            return target_test["suggested_implementation"]
            
        except Exception as e:
            logger.error(f"Failed to generate test completion: {e}")
            return f"Error generating test: {e}"
    
    async def analyze_payment_tests(self) -> Dict[str, Any]:
        """Analyze the payment tests specifically"""
        file_path = "examples/tests/payment_tests.py"
        
        analysis = await self.analyze_test_file(file_path)
        
        # Add payment-specific analysis
        payment_analysis = {
            **analysis,
            "payment_specific_gaps": [],
            "security_recommendations": [],
            "financial_test_patterns": []
        }
        
        # Check for payment-specific test patterns
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check for decimal precision tests
        if "decimal" not in content.lower():
            payment_analysis["payment_specific_gaps"].append({
                "type": "missing_decimal_precision_tests",
                "description": "Insufficient decimal precision testing for financial calculations"
            })
        
        # Check for idempotency tests
        if "idempotency" not in content.lower():
            payment_analysis["payment_specific_gaps"].append({
                "type": "missing_idempotency_tests", 
                "description": "Missing idempotency tests for payment operations"
            })
        
        # Security recommendations
        payment_analysis["security_recommendations"] = [
            "Add tests for transaction replay attacks",
            "Test for amount manipulation attempts",
            "Verify proper authentication on all payment endpoints",
            "Test rate limiting on payment operations",
            "Verify audit logging for all financial operations"
        ]
        
        return payment_analysis
    
    def is_relevant(self, query: str) -> bool:
        """Check if this tool is relevant for the query"""
        dev_keywords = [
            "test", "testing", "implementation", "code", "function",
            "bug", "error", "debug", "analyze", "complete", "generate"
        ]
        
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in dev_keywords)
    
    async def execute(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute development assistant based on query"""
        if "payment test" in query.lower() or "payment_tests.py" in query:
            return await self.analyze_payment_tests()
        elif "analyze test" in query.lower():
            file_path = context.get("file_path", "examples/tests/payment_tests.py")
            return await self.analyze_test_file(file_path)
        elif "complete test" in query.lower():
            file_path = context.get("file_path", "examples/tests/payment_tests.py")
            function_name = context.get("function_name", "")
            implementation = await self.generate_test_completion(file_path, function_name)
            return {"implementation": implementation}
        else:
            return {"error": "Query not understood. Try 'analyze payment tests' or 'complete test function_name'"}
    
    async def cleanup(self):
        """Cleanup resources"""
        pass
