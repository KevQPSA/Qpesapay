#!/usr/bin/env python3
"""
Local WebAgent Development Assistant Demo (No API Keys Required)

This script demonstrates WebAgent-style development assistance using only
local code analysis and pattern matching - no external API keys needed!
"""

import ast
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime

# Add the backend directory to the path
sys.path.append(str(Path(__file__).parent.parent))


class LocalWebAgentAnalyzer:
    """Local code analyzer that mimics WebAgent capabilities without API keys"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        
    def analyze_payment_tests(self, file_path: str = "examples/tests/payment_tests.py") -> Dict[str, Any]:
        """Analyze payment tests and identify incomplete functions"""
        print(f"🔍 Analyzing {file_path}...")
        
        if not Path(file_path).exists():
            return {"error": f"File {file_path} not found"}
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Parse AST to find incomplete functions
        tree = ast.parse(content)
        
        analysis = {
            "file_path": file_path,
            "total_functions": 0,
            "incomplete_functions": [],
            "complete_functions": [],
            "test_patterns": [],
            "security_gaps": [],
            "recommendations": []
        }
        
        # Find all test functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                analysis["total_functions"] += 1
                
                # Check if function is incomplete (just has 'pass')
                if (len(node.body) == 1 and 
                    isinstance(node.body[0], ast.Pass)):
                    
                    analysis["incomplete_functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "docstring": ast.get_docstring(node) or "No description",
                        "priority": self._calculate_priority(node.name),
                        "estimated_effort": self._estimate_effort(node.name),
                        "test_type": self._classify_test_type(node.name)
                    })
                else:
                    analysis["complete_functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "complexity": self._estimate_complexity(node)
                    })
        
        # Analyze test patterns and gaps
        analysis["test_patterns"] = self._analyze_test_patterns(content)
        analysis["security_gaps"] = self._identify_security_gaps(content)
        analysis["recommendations"] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _calculate_priority(self, function_name: str) -> int:
        """Calculate priority score for test completion"""
        priority = 0
        name_lower = function_name.lower()
        
        # High priority for security and audit
        if any(keyword in name_lower for keyword in ["security", "audit", "validation"]):
            priority += 50
        
        # High priority for financial operations
        if any(keyword in name_lower for keyword in ["payment", "transaction", "money"]):
            priority += 40
        
        # Medium priority for compliance
        if any(keyword in name_lower for keyword in ["compliance", "rate_limiting"]):
            priority += 35
        
        # Medium priority for error handling
        if any(keyword in name_lower for keyword in ["error", "exception", "failure"]):
            priority += 30
        
        return priority
    
    def _estimate_effort(self, function_name: str) -> str:
        """Estimate effort required to complete test"""
        name_lower = function_name.lower()
        
        if any(keyword in name_lower for keyword in ["integration", "end_to_end", "comprehensive"]):
            return "high"
        elif any(keyword in name_lower for keyword in ["security", "audit", "compliance"]):
            return "medium"
        else:
            return "low"
    
    def _classify_test_type(self, function_name: str) -> str:
        """Classify the type of test"""
        name_lower = function_name.lower()
        
        if "audit" in name_lower:
            return "audit_trail"
        elif "rate_limiting" in name_lower:
            return "rate_limiting"
        elif "security" in name_lower:
            return "security_validation"
        elif "compliance" in name_lower:
            return "compliance_check"
        else:
            return "general"
    
    def _estimate_complexity(self, node: ast.FunctionDef) -> str:
        """Estimate complexity of existing function"""
        line_count = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 10
        
        if line_count > 50:
            return "high"
        elif line_count > 20:
            return "medium"
        else:
            return "low"
    
    def _analyze_test_patterns(self, content: str) -> List[str]:
        """Analyze existing test patterns"""
        patterns = []
        
        if "Mock(" in content:
            patterns.append("✅ Uses mocking for external dependencies")
        
        if "pytest.raises" in content:
            patterns.append("✅ Tests exception handling")
        
        if "Decimal(" in content:
            patterns.append("✅ Uses Decimal for financial calculations")
        
        if "@pytest.fixture" in content:
            patterns.append("✅ Uses pytest fixtures for test setup")
        
        if "assert" in content:
            patterns.append("✅ Has assertion-based validation")
        
        return patterns
    
    def _identify_security_gaps(self, content: str) -> List[str]:
        """Identify security testing gaps"""
        gaps = []
        
        if "malicious_input" not in content.lower():
            gaps.append("⚠️ Limited malicious input testing")
        
        if "sql injection" not in content.lower():
            gaps.append("⚠️ No SQL injection prevention tests")
        
        if "rate limit" not in content.lower():
            gaps.append("⚠️ Missing rate limiting tests")
        
        if "audit" not in content.lower():
            gaps.append("⚠️ Incomplete audit trail testing")
        
        return gaps
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        incomplete_count = len(analysis["incomplete_functions"])
        if incomplete_count > 0:
            recommendations.append(f"🎯 Complete {incomplete_count} incomplete test functions")
        
        # Priority-based recommendations
        high_priority = [f for f in analysis["incomplete_functions"] if f["priority"] >= 40]
        if high_priority:
            recommendations.append(f"🔥 Focus on {len(high_priority)} high-priority tests first")
        
        # Security recommendations
        if analysis["security_gaps"]:
            recommendations.append("🔒 Address security testing gaps")
        
        recommendations.extend([
            "🧪 Add more edge case testing",
            "📊 Implement test coverage measurement",
            "⚡ Add performance testing for critical paths",
            "🔄 Implement idempotency testing patterns"
        ])
        
        return recommendations
    
    def generate_test_implementation(self, function_name: str, test_type: str) -> str:
        """Generate test implementation based on function name and type"""
        
        if test_type == "audit_trail":
            return self._generate_audit_trail_test()
        elif test_type == "rate_limiting":
            return self._generate_rate_limiting_test()
        elif test_type == "security_validation":
            return self._generate_security_test()
        else:
            return self._generate_generic_test(function_name)
    
    def _generate_audit_trail_test(self) -> str:
        """Generate audit trail test implementation"""
        return '''        """Test that all payment operations are properly audited."""
        # Arrange
        payment_request = PaymentRequest(
            user_id="test-user-123",
            amount=Money(Decimal("100.00"), Currency.USDT),
            recipient_address="0x742d35Cc6634C0532925a3b8D4C9db4C4C4b4C4C",
            currency=Currency.USDT,
            network="ethereum",
            priority="standard"
        )
        
        # Mock audit logger to track all calls
        audit_logger = Mock()
        payment_processor.audit_logger = audit_logger
        
        # Mock successful validation and processing
        mock_dependencies['validator'].validate_payment.return_value = Mock(
            is_valid=True, errors=[]
        )
        mock_dependencies['validator'].validate_balance.return_value = True
        mock_dependencies['fee_estimator'].estimate_fee.return_value = Decimal("2.50")
        mock_dependencies['blockchain_service'].send_transaction.return_value = Mock(
            hash="0xtest123", status="pending"
        )
        
        # Act
        with patch.object(payment_processor, '_is_duplicate_request', return_value=False):
            result = payment_processor.process_payment(
                payment_request=payment_request,
                idempotency_key="test-audit-key"
            )
        
        # Assert - Verify all required audit events were logged
        required_audit_calls = [
            'log_payment_initiated',
            'log_validation_completed',
            'log_fee_calculated',
            'log_blockchain_transaction_started',
            'log_payment_completed'
        ]
        
        for call_name in required_audit_calls:
            assert hasattr(audit_logger, call_name), f"Missing audit method: {call_name}"
            getattr(audit_logger, call_name).assert_called_once()
        
        # Verify audit data contains required fields
        for call in audit_logger.method_calls:
            if len(call) > 2 and 'audit_data' in call[2]:
                audit_data = call[2]['audit_data']
                required_fields = ['timestamp', 'user_id', 'transaction_id', 'amount', 'status']
                
                for field in required_fields:
                    assert field in audit_data, f"Missing audit field: {field} in {call[0]}"
                
                # Verify timestamp format
                assert isinstance(audit_data['timestamp'], (str, datetime))
                
                # Verify amount precision
                if 'amount' in audit_data:
                    assert isinstance(audit_data['amount'], (Decimal, str))'''
    
    def _generate_rate_limiting_test(self) -> str:
        """Generate rate limiting test implementation"""
        return '''        """Test that payment processing respects rate limits."""
        from app.core.rate_limiter import RateLimiter
        from app.core.exceptions import RateLimitExceededError
        
        # Arrange
        rate_limiter = RateLimiter(max_requests=3, time_window=60)  # 3 requests per minute
        payment_processor.rate_limiter = rate_limiter
        
        payment_request = PaymentRequest(
            user_id="test-user-rate-limit",
            amount=Money(Decimal("50.00"), Currency.USDT),
            recipient_address="0x742d35Cc6634C0532925a3b8D4C9db4C4C4b4C4C",
            currency=Currency.USDT,
            network="ethereum",
            priority="standard"
        )
        
        # Mock successful validation for all requests
        with patch.object(payment_processor, '_validate_payment', return_value=True):
            with patch.object(payment_processor, '_process_blockchain_transaction'):
                
                # Act & Assert - First 3 requests should succeed
                for i in range(3):
                    try:
                        result = payment_processor.process_payment(
                            payment_request=payment_request,
                            idempotency_key=f"rate-limit-key-{i}"
                        )
                        assert result is not None, f"Request {i+1} should succeed"
                    except RateLimitExceededError:
                        pytest.fail(f"Request {i+1} should not be rate limited")
                
                # 4th request should be rate limited
                with pytest.raises(RateLimitExceededError) as exc_info:
                    payment_processor.process_payment(
                        payment_request=payment_request,
                        idempotency_key="rate-limit-key-4"
                    )
                
                # Verify error message contains rate limit information
                error_message = str(exc_info.value)
                assert "rate limit" in error_message.lower()
                assert "3 requests" in error_message
                assert "minute" in error_message.lower()
                
                # Verify rate limit headers/metadata if available
                if hasattr(exc_info.value, 'retry_after'):
                    assert exc_info.value.retry_after > 0
                    assert exc_info.value.retry_after <= 60'''
    
    def _generate_security_test(self) -> str:
        """Generate security validation test implementation"""
        return '''        """Test comprehensive security validations and input sanitization."""
        # Test SQL injection prevention
        sql_injection_inputs = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'/*",
            "' UNION SELECT * FROM payments --",
            "user'; DELETE FROM transactions; --"
        ]
        
        for malicious_input in sql_injection_inputs:
            with pytest.raises(ValidationError) as exc_info:
                PaymentRequest(
                    user_id=malicious_input,
                    amount=Money(Decimal("100"), Currency.USDT),
                    recipient_address="0x742d35Cc6634C0532925a3b8D4C9db4C4C4b4C4C",
                    currency=Currency.USDT,
                    network="ethereum",
                    priority="standard"
                )
            
            assert "invalid input" in str(exc_info.value).lower()
        
        # Test XSS prevention
        xss_inputs = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "';alert('xss');//",
            "<iframe src='javascript:alert(1)'></iframe>"
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
            "C:\\\\Windows\\\\System32\\\\drivers\\\\etc\\\\hosts",
            "../../../root/.ssh/id_rsa"
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
        
        # Test cryptocurrency address validation
        invalid_addresses = [
            "invalid_address",
            "0x123",  # Too short
            "0xGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",  # Invalid hex
            "",  # Empty
            "1234567890" * 10,  # Too long
            "0x" + "0" * 39,  # Wrong length
        ]
        
        for invalid_address in invalid_addresses:
            with pytest.raises(ValidationError) as exc_info:
                PaymentRequest(
                    user_id="test-user",
                    amount=Money(Decimal("100"), Currency.USDT),
                    recipient_address=invalid_address,
                    currency=Currency.USDT,
                    network="ethereum",
                    priority="standard"
                )
            
            assert "invalid address" in str(exc_info.value).lower()'''
    
    def _generate_generic_test(self, function_name: str) -> str:
        """Generate generic test implementation"""
        return f'''        """Test implementation for {function_name}."""
        # Arrange
        # TODO: Set up test data and mocks based on function purpose
        
        # Act
        # TODO: Execute the functionality being tested
        
        # Assert
        # TODO: Verify expected behavior and outcomes
        assert True  # Replace with actual assertions
        
        # Additional test cases to consider:
        # - Edge cases and boundary conditions
        # - Error handling scenarios
        # - Performance requirements
        # - Security validations'''


def main():
    """Run the local WebAgent development demo"""
    print("🤖 Local WebAgent Development Assistant")
    print("AI-style development assistance without API keys!")
    print("=" * 60)
    
    analyzer = LocalWebAgentAnalyzer()
    
    # Analyze payment tests
    analysis = analyzer.analyze_payment_tests()
    
    if "error" in analysis:
        print(f"❌ {analysis['error']}")
        return
    
    # Display analysis results
    print(f"\n📊 Analysis Results:")
    print(f"   📁 File: {analysis['file_path']}")
    print(f"   🔢 Total functions: {analysis['total_functions']}")
    print(f"   ✅ Complete: {len(analysis['complete_functions'])}")
    print(f"   🔧 Incomplete: {len(analysis['incomplete_functions'])}")
    
    # Show incomplete functions with priorities
    if analysis['incomplete_functions']:
        print(f"\n🎯 Incomplete Functions (Priority Order):")
        sorted_functions = sorted(analysis['incomplete_functions'], 
                                key=lambda x: x['priority'], reverse=True)
        
        for i, func in enumerate(sorted_functions, 1):
            print(f"   {i}. {func['name']}")
            print(f"      Priority: {func['priority']} | Effort: {func['estimated_effort']} | Type: {func['test_type']}")
            print(f"      Description: {func['docstring'][:80]}...")
            print()
    
    # Show test patterns
    if analysis['test_patterns']:
        print(f"🧪 Test Patterns Found:")
        for pattern in analysis['test_patterns']:
            print(f"   {pattern}")
    
    # Show security gaps
    if analysis['security_gaps']:
        print(f"\n🔒 Security Gaps:")
        for gap in analysis['security_gaps']:
            print(f"   {gap}")
    
    # Show recommendations
    print(f"\n💡 Recommendations:")
    for rec in analysis['recommendations']:
        print(f"   {rec}")
    
    # Generate sample implementations
    print(f"\n🛠️ Sample Implementations:")
    print("=" * 40)
    
    # Generate implementation for highest priority incomplete function
    if analysis['incomplete_functions']:
        top_function = sorted(analysis['incomplete_functions'], 
                            key=lambda x: x['priority'], reverse=True)[0]
        
        print(f"\n📝 Implementation for '{top_function['name']}':")
        print("-" * 50)
        
        implementation = analyzer.generate_test_implementation(
            top_function['name'], 
            top_function['test_type']
        )
        
        print(f"    def {top_function['name']}(self, payment_processor, mock_dependencies):")
        print(implementation)
        print("-" * 50)
        
        # Save implementation to file
        output_dir = Path("examples/generated")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / f"{top_function['name']}_implementation.py"
        with open(output_file, 'w') as f:
            f.write(f"""# Generated by Local WebAgent - {top_function['name']}
# Priority: {top_function['priority']}
# Effort: {top_function['estimated_effort']}
# Type: {top_function['test_type']}
# Generated: {datetime.now().isoformat()}

def {top_function['name']}(self, payment_processor, mock_dependencies):
{implementation}
""")
        
        print(f"💾 Implementation saved to: {output_file}")
    
    print(f"\n🎉 Local WebAgent Analysis Complete!")
    print("\nNext Steps:")
    print("1. 📝 Review the generated implementations")
    print("2. 🧪 Copy implementations to your test file")
    print("3. 🔧 Customize for your specific needs")
    print("4. ✅ Run tests to verify they work")
    print("5. 🚀 Integrate into your development workflow")


if __name__ == "__main__":
    # Check if we're in the right directory
    if not Path("examples/tests/payment_tests.py").exists():
        print("❌ Error: payment_tests.py not found!")
        print("   Please run this script from the backend directory")
        sys.exit(1)
    
    main()
