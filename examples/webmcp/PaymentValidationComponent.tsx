/**
 * 🟢 Production Ready: WebMCP Payment Validation Component
 * 
 * This React component demonstrates real-time payment validation using WebMCP
 * integration with Qpesapay's financial system. It provides instant feedback
 * on payment validity, compliance status, and risk assessment.
 * 
 * Key Features:
 * - Real-time payment validation
 * - Live compliance checking
 * - Dynamic fee calculation
 * - Risk assessment display
 * - Mobile-responsive design
 */

import React, { useState, useEffect, useCallback } from 'react';
import { QpesapayMcpServer } from './qpesapay_mcp_server';

// Types for component state
interface PaymentForm {
  amount: string;
  fromCurrency: 'BTC' | 'USDT';
  toCurrency: 'KES' | 'USD';
  recipientAddress: string;
}

interface ValidationResult {
  isValid: boolean;
  errors: string[];
  riskScore: number;
  complianceStatus: 'approved' | 'pending' | 'rejected';
  fees?: {
    networkFee: string;
    serviceFee: string;
    totalFee: string;
  };
}

interface ComponentProps {
  mcpServer: QpesapayMcpServer;
  userId?: string;
  onValidationComplete?: (result: ValidationResult) => void;
}

/**
 * 🟢 Production Ready: Payment Validation Component with WebMCP
 * 
 * Provides real-time payment validation using browser-based MCP tools.
 * Integrates seamlessly with Qpesapay's existing authentication and
 * maintains all security and compliance requirements.
 */
export const PaymentValidationComponent: React.FC<ComponentProps> = ({
  mcpServer,
  userId,
  onValidationComplete
}) => {
  // Component state
  const [paymentForm, setPaymentForm] = useState<PaymentForm>({
    amount: '',
    fromCurrency: 'USDT',
    toCurrency: 'KES',
    recipientAddress: ''
  });
  
  const [validationResult, setValidationResult] = useState<ValidationResult | null>(null);
  const [isValidating, setIsValidating] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [fees, setFees] = useState<any>(null);
  const [isCalculatingFees, setIsCalculatingFees] = useState(false);
  
  /**
   * Real-time payment validation using WebMCP
   */
  const validatePayment = useCallback(async () => {
    if (!paymentForm.amount || !paymentForm.recipientAddress) {
      return;
    }
    
    setIsValidating(true);
    setValidationError(null);
    
    try {
      // Use WebMCP tool for real-time validation
      const result = await mcpServer.server.callTool('validatePayment', {
        amount: paymentForm.amount,
        fromCurrency: paymentForm.fromCurrency,
        toCurrency: paymentForm.toCurrency,
        recipientAddress: paymentForm.recipientAddress,
        userId
      });
      
      if (result.content && result.content[0]) {
        const validationData = JSON.parse(result.content[0].text);
        const validation = validationData.validation;
        
        setValidationResult(validation);
        onValidationComplete?.(validation);
      }
    } catch (error) {
      setValidationError(`Validation failed: ${error.message}`);
    } finally {
      setIsValidating(false);
    }
  }, [paymentForm, mcpServer, userId, onValidationComplete]);
  
  /**
   * Real-time fee calculation using WebMCP
   */
  const calculateFees = useCallback(async () => {
    if (!paymentForm.amount) {
      return;
    }
    
    setIsCalculatingFees(true);
    
    try {
      const result = await mcpServer.server.callTool('calculateFees', {
        amount: paymentForm.amount,
        fromCurrency: paymentForm.fromCurrency,
        toCurrency: paymentForm.toCurrency,
        priority: 'standard'
      });
      
      if (result.content && result.content[0]) {
        const feeData = JSON.parse(result.content[0].text);
        setFees(feeData);
      }
    } catch (error) {
      console.error('Fee calculation failed:', error);
    } finally {
      setIsCalculatingFees(false);
    }
  }, [paymentForm, mcpServer]);
  
  /**
   * Handle form input changes with real-time validation
   */
  const handleInputChange = (field: keyof PaymentForm, value: string) => {
    setPaymentForm(prev => ({
      ...prev,
      [field]: value
    }));
    
    // Clear previous results
    setValidationResult(null);
    setValidationError(null);
  };
  
  /**
   * Debounced validation effect
   */
  useEffect(() => {
    const timer = setTimeout(() => {
      if (paymentForm.amount && paymentForm.recipientAddress) {
        validatePayment();
        calculateFees();
      }
    }, 500); // 500ms debounce
    
    return () => clearTimeout(timer);
  }, [paymentForm, validatePayment, calculateFees]);
  
  /**
   * Render validation status indicator
   */
  const renderValidationStatus = () => {
    if (isValidating) {
      return (
        <div className="validation-status validating">
          <div className="spinner"></div>
          <span>Validating payment...</span>
        </div>
      );
    }
    
    if (validationError) {
      return (
        <div className="validation-status error">
          <span className="icon">❌</span>
          <span>{validationError}</span>
        </div>
      );
    }
    
    if (validationResult) {
      return (
        <div className={`validation-status ${validationResult.isValid ? 'valid' : 'invalid'}`}>
          <span className="icon">{validationResult.isValid ? '✅' : '❌'}</span>
          <div className="validation-details">
            <div className="status">
              {validationResult.isValid ? 'Payment Valid' : 'Payment Invalid'}
            </div>
            <div className="risk-score">
              Risk Score: {validationResult.riskScore}/100
            </div>
            <div className="compliance-status">
              Compliance: {validationResult.complianceStatus}
            </div>
            {validationResult.errors.length > 0 && (
              <div className="errors">
                {validationResult.errors.map((error, index) => (
                  <div key={index} className="error-item">{error}</div>
                ))}
              </div>
            )}
          </div>
        </div>
      );
    }
    
    return null;
  };
  
  /**
   * Render fee information
   */
  const renderFeeInformation = () => {
    if (isCalculatingFees) {
      return (
        <div className="fee-info calculating">
          <div className="spinner"></div>
          <span>Calculating fees...</span>
        </div>
      );
    }
    
    if (fees) {
      return (
        <div className="fee-info">
          <h4>Transaction Fees</h4>
          <div className="fee-breakdown">
            <div className="fee-item">
              <span>Network Fee:</span>
              <span>{fees.breakdown.networkFee} {paymentForm.fromCurrency}</span>
            </div>
            <div className="fee-item">
              <span>Service Fee:</span>
              <span>{fees.breakdown.serviceFee} {paymentForm.fromCurrency}</span>
            </div>
            <div className="fee-item total">
              <span>Total Fee:</span>
              <span>{fees.breakdown.totalFee} {paymentForm.fromCurrency}</span>
            </div>
          </div>
          <div className="estimated-time">
            Estimated Time: {fees.estimatedTime}
          </div>
        </div>
      );
    }
    
    return null;
  };
  
  return (
    <div className="payment-validation-component">
      <div className="form-section">
        <h3>Payment Details</h3>
        
        <div className="form-group">
          <label htmlFor="amount">Amount</label>
          <input
            id="amount"
            type="number"
            step="0.000001"
            value={paymentForm.amount}
            onChange={(e) => handleInputChange('amount', e.target.value)}
            placeholder="Enter amount"
            className="form-input"
          />
        </div>
        
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="fromCurrency">From</label>
            <select
              id="fromCurrency"
              value={paymentForm.fromCurrency}
              onChange={(e) => handleInputChange('fromCurrency', e.target.value as 'BTC' | 'USDT')}
              className="form-select"
            >
              <option value="USDT">USDT</option>
              <option value="BTC">Bitcoin</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="toCurrency">To</label>
            <select
              id="toCurrency"
              value={paymentForm.toCurrency}
              onChange={(e) => handleInputChange('toCurrency', e.target.value as 'KES' | 'USD')}
              className="form-select"
            >
              <option value="KES">Kenyan Shilling</option>
              <option value="USD">US Dollar</option>
            </select>
          </div>
        </div>
        
        <div className="form-group">
          <label htmlFor="recipientAddress">
            {paymentForm.toCurrency === 'KES' ? 'Phone Number' : 'Wallet Address'}
          </label>
          <input
            id="recipientAddress"
            type="text"
            value={paymentForm.recipientAddress}
            onChange={(e) => handleInputChange('recipientAddress', e.target.value)}
            placeholder={
              paymentForm.toCurrency === 'KES' 
                ? '+254712345678' 
                : '0x742d35Cc6634C0532925a3b8D4C9db4C4C4b4C4C'
            }
            className="form-input"
          />
        </div>
      </div>
      
      <div className="validation-section">
        {renderValidationStatus()}
        {renderFeeInformation()}
      </div>
      
      <style jsx>{`
        .payment-validation-component {
          max-width: 600px;
          margin: 0 auto;
          padding: 20px;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .form-section {
          background: #f8f9fa;
          padding: 20px;
          border-radius: 8px;
          margin-bottom: 20px;
        }
        
        .form-section h3 {
          margin: 0 0 20px 0;
          color: #333;
        }
        
        .form-group {
          margin-bottom: 15px;
        }
        
        .form-row {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 15px;
        }
        
        .form-group label {
          display: block;
          margin-bottom: 5px;
          font-weight: 500;
          color: #555;
        }
        
        .form-input, .form-select {
          width: 100%;
          padding: 10px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 14px;
        }
        
        .form-input:focus, .form-select:focus {
          outline: none;
          border-color: #007bff;
          box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
        }
        
        .validation-section {
          background: white;
          border: 1px solid #e9ecef;
          border-radius: 8px;
          padding: 20px;
        }
        
        .validation-status {
          display: flex;
          align-items: flex-start;
          gap: 10px;
          margin-bottom: 20px;
        }
        
        .validation-status.validating {
          color: #6c757d;
        }
        
        .validation-status.valid {
          color: #28a745;
        }
        
        .validation-status.invalid {
          color: #dc3545;
        }
        
        .validation-status.error {
          color: #dc3545;
        }
        
        .validation-details {
          flex: 1;
        }
        
        .validation-details .status {
          font-weight: 600;
          margin-bottom: 5px;
        }
        
        .validation-details .risk-score,
        .validation-details .compliance-status {
          font-size: 14px;
          margin-bottom: 3px;
        }
        
        .errors {
          margin-top: 10px;
        }
        
        .error-item {
          background: #f8d7da;
          color: #721c24;
          padding: 5px 10px;
          border-radius: 4px;
          margin-bottom: 5px;
          font-size: 14px;
        }
        
        .fee-info {
          border-top: 1px solid #e9ecef;
          padding-top: 20px;
        }
        
        .fee-info h4 {
          margin: 0 0 15px 0;
          color: #333;
        }
        
        .fee-breakdown {
          margin-bottom: 15px;
        }
        
        .fee-item {
          display: flex;
          justify-content: space-between;
          margin-bottom: 8px;
          font-size: 14px;
        }
        
        .fee-item.total {
          font-weight: 600;
          border-top: 1px solid #e9ecef;
          padding-top: 8px;
          margin-top: 8px;
        }
        
        .estimated-time {
          font-size: 14px;
          color: #6c757d;
        }
        
        .spinner {
          width: 16px;
          height: 16px;
          border: 2px solid #f3f3f3;
          border-top: 2px solid #007bff;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
          .payment-validation-component {
            padding: 15px;
          }
          
          .form-row {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default PaymentValidationComponent;
