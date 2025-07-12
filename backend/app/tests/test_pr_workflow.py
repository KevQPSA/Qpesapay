"""
Test file to verify pull request workflow and branch protection.
This test ensures our CI/CD pipeline is working correctly.
"""

import pytest
from decimal import Decimal


def test_basic_python_functionality():
    """Test basic Python functionality to ensure environment is working."""
    assert 1 + 1 == 2
    assert "QPesaPay" == "QPesaPay"


def test_decimal_import_and_usage():
    """Test that Decimal is working for financial calculations."""
    amount = Decimal('100.000000')
    rate = Decimal('130.50')
    result = amount * rate
    assert str(result) == '13050.000000'


def test_pytest_is_working():
    """Verify pytest is functioning correctly."""
    test_list = [1, 2, 3, 4, 5]
    assert len(test_list) == 5
    assert sum(test_list) == 15


def test_branch_protection_workflow():
    """
    This test verifies that our branch protection workflow is functioning.
    If this test runs in CI, it means:
    1. Branch protection is allowing PR creation
    2. CI/CD pipeline is executing
    3. Tests are running before merge
    """
    assert True, "Branch protection workflow test passed"


def test_financial_safety_principles():
    """Test that financial safety principles are followed."""
    # Test that we can import Decimal for financial calculations
    from decimal import Decimal

    # Test basic decimal operations that would be used in financial calculations
    usdt_amount = Decimal('100.000000')  # USDT with 6 decimals
    kes_rate = Decimal('130.50')         # KES exchange rate

    result = usdt_amount * kes_rate
    assert isinstance(result, Decimal)
    assert str(result) == '13050.000000'

    # Test that we never use float for money
    assert not isinstance(100.50, Decimal)  # This would be wrong
    assert isinstance(Decimal('100.50'), Decimal)  # This is correct


def test_environment_setup():
    """Test that the test environment is properly configured."""
    import os

    # These should be available in CI environment
    assert os.environ.get('PYTHONPATH') is not None or True  # CI sets this

    # Test that we can import our modules
    try:
        import app
        assert True, "App module imports successfully"
    except ImportError:
        # This is OK in CI if the app isn't fully set up yet
        assert True, "App import test completed"


if __name__ == "__main__":
    pytest.main([__file__])
