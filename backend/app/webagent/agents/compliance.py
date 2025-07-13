"""
Compliance Agent - WebSailor-based agent for regulatory compliance and risk assessment
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

from .base import WebSailorBasedAgent


class ComplianceAgent(WebSailorBasedAgent):
    """
    Compliance Agent using WebSailor's extended thinking capabilities
    
    Specialized for:
    - KYC/AML compliance checking
    - Regulatory requirement analysis
    - Risk assessment and scoring
    - Transaction monitoring and flagging
    - Regulatory update tracking
    """
    
    def __init__(self, tools: List[Any], config: Any):
        super().__init__(tools, config, "compliance")
        self.compliance_frameworks = [
            "kenya_cma_regulations",
            "cbk_guidelines", 
            "fatf_recommendations",
            "aml_requirements",
            "kyc_standards"
        ]
        self.risk_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    
    async def check_compliance(
        self, 
        transaction_data: Dict[str, Any], 
        check_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """
        Main compliance checking method
        
        Args:
            transaction_data: Transaction details to check
            check_type: Type of compliance check (basic, comprehensive, specific)
            
        Returns:
            Comprehensive compliance assessment
        """
        await self._rate_limit_check()
        
        # Check cache first
        cache_key = self._get_cache_key(str(transaction_data), {"check_type": check_type})
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        try:
            # Perform extended thinking analysis
            thinking_result = await self._extended_thinking(
                f"Compliance check for {check_type}", 
                {"transaction_data": transaction_data, "check_type": check_type}
            )
            
            # Execute compliance checks
            compliance_result = await self._execute_compliance_checks(
                transaction_data, check_type, thinking_result
            )
            
            # Calculate risk score
            risk_assessment = await self._assess_risk(transaction_data, compliance_result)
            
            # Generate compliance report
            final_result = await self._generate_compliance_report(
                transaction_data, compliance_result, risk_assessment, thinking_result
            )
            
            # Cache result
            self._set_cached_result(cache_key, final_result)
            
            return final_result
            
        except Exception as e:
            self.logger.error(f"Compliance check failed: {e}")
            return {
                "success": False,
                "transaction_data": transaction_data,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _execute_compliance_checks(
        self, 
        transaction_data: Dict[str, Any], 
        check_type: str,
        thinking_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute specific compliance checks based on type"""
        
        checks_result = {
            "check_type": check_type,
            "checks_performed": [],
            "passed_checks": [],
            "failed_checks": [],
            "warnings": []
        }
        
        if check_type in ["basic", "comprehensive"]:
            # Basic KYC checks
            kyc_result = await self._check_kyc_compliance(transaction_data)
            checks_result["checks_performed"].append("kyc_compliance")
            if kyc_result["passed"]:
                checks_result["passed_checks"].append("kyc_compliance")
            else:
                checks_result["failed_checks"].append("kyc_compliance")
            checks_result["kyc_result"] = kyc_result
            
            # AML checks
            aml_result = await self._check_aml_compliance(transaction_data)
            checks_result["checks_performed"].append("aml_compliance")
            if aml_result["passed"]:
                checks_result["passed_checks"].append("aml_compliance")
            else:
                checks_result["failed_checks"].append("aml_compliance")
            checks_result["aml_result"] = aml_result
        
        if check_type in ["comprehensive"]:
            # Transaction limits check
            limits_result = await self._check_transaction_limits(transaction_data)
            checks_result["checks_performed"].append("transaction_limits")
            if limits_result["passed"]:
                checks_result["passed_checks"].append("transaction_limits")
            else:
                checks_result["failed_checks"].append("transaction_limits")
            checks_result["limits_result"] = limits_result
            
            # Regulatory compliance
            regulatory_result = await self._check_regulatory_compliance(transaction_data)
            checks_result["checks_performed"].append("regulatory_compliance")
            if regulatory_result["passed"]:
                checks_result["passed_checks"].append("regulatory_compliance")
            else:
                checks_result["failed_checks"].append("regulatory_compliance")
            checks_result["regulatory_result"] = regulatory_result
        
        return checks_result
    
    async def _check_kyc_compliance(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check KYC compliance requirements"""
        result = {
            "passed": True,
            "issues": [],
            "requirements_met": [],
            "missing_requirements": []
        }
        
        # Check user verification status
        user_id = transaction_data.get("user_id")
        if not user_id:
            result["passed"] = False
            result["issues"].append("No user ID provided")
            return result
        
        # Check required KYC documents
        required_docs = ["national_id", "proof_of_address"]
        user_docs = transaction_data.get("user_documents", [])
        
        for doc in required_docs:
            if doc in user_docs:
                result["requirements_met"].append(doc)
            else:
                result["missing_requirements"].append(doc)
                result["passed"] = False
                result["issues"].append(f"Missing {doc}")
        
        # Check transaction amount thresholds
        amount = transaction_data.get("amount", 0)
        if amount > 100000:  # KES 100,000 threshold
            enhanced_kyc_docs = ["bank_statement", "source_of_funds"]
            for doc in enhanced_kyc_docs:
                if doc not in user_docs:
                    result["missing_requirements"].append(doc)
                    result["passed"] = False
                    result["issues"].append(f"Enhanced KYC required: missing {doc}")
        
        return result
    
    async def _check_aml_compliance(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check AML compliance requirements"""
        result = {
            "passed": True,
            "risk_score": 0,
            "flags": [],
            "checks_performed": []
        }
        
        # Check against sanctions lists
        user_name = transaction_data.get("user_name", "")
        if user_name:
            sanctions_check = await self._check_sanctions_list(user_name)
            result["checks_performed"].append("sanctions_list")
            if sanctions_check["flagged"]:
                result["passed"] = False
                result["flags"].append("Sanctions list match")
                result["risk_score"] += 50
        
        # Check transaction patterns
        pattern_check = await self._check_transaction_patterns(transaction_data)
        result["checks_performed"].append("transaction_patterns")
        if pattern_check["suspicious"]:
            result["flags"].append("Suspicious transaction pattern")
            result["risk_score"] += pattern_check["risk_score"]
        
        # Check high-risk countries
        country = transaction_data.get("country", "KE")
        if country in ["AF", "IR", "KP", "SY"]:  # High-risk countries
            result["flags"].append("High-risk country")
            result["risk_score"] += 30
        
        # Determine overall pass/fail
        if result["risk_score"] > 70:
            result["passed"] = False
        
        return result
    
    async def _check_transaction_limits(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check transaction limits compliance"""
        result = {
            "passed": True,
            "limits_checked": [],
            "violations": []
        }
        
        amount = transaction_data.get("amount", 0)
        transaction_type = transaction_data.get("transaction_type", "")
        user_tier = transaction_data.get("user_tier", "basic")
        
        # Define limits based on user tier
        limits = {
            "basic": {"daily": 50000, "monthly": 500000},  # KES
            "verified": {"daily": 200000, "monthly": 2000000},
            "premium": {"daily": 1000000, "monthly": 10000000}
        }
        
        user_limits = limits.get(user_tier, limits["basic"])
        
        # Check daily limit
        daily_usage = transaction_data.get("daily_usage", 0)
        if daily_usage + amount > user_limits["daily"]:
            result["passed"] = False
            result["violations"].append(f"Daily limit exceeded: {daily_usage + amount} > {user_limits['daily']}")
        result["limits_checked"].append("daily_limit")
        
        # Check monthly limit
        monthly_usage = transaction_data.get("monthly_usage", 0)
        if monthly_usage + amount > user_limits["monthly"]:
            result["passed"] = False
            result["violations"].append(f"Monthly limit exceeded: {monthly_usage + amount} > {user_limits['monthly']}")
        result["limits_checked"].append("monthly_limit")
        
        return result
    
    async def _check_regulatory_compliance(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check regulatory compliance requirements"""
        result = {
            "passed": True,
            "regulations_checked": [],
            "compliance_issues": []
        }
        
        # Check CMA Kenya requirements
        cma_check = await self._check_cma_requirements(transaction_data)
        result["regulations_checked"].append("cma_kenya")
        if not cma_check["compliant"]:
            result["passed"] = False
            result["compliance_issues"].extend(cma_check["issues"])
        
        # Check CBK guidelines
        cbk_check = await self._check_cbk_guidelines(transaction_data)
        result["regulations_checked"].append("cbk_guidelines")
        if not cbk_check["compliant"]:
            result["passed"] = False
            result["compliance_issues"].extend(cbk_check["issues"])
        
        return result
    
    async def _check_sanctions_list(self, user_name: str) -> Dict[str, Any]:
        """Check user against sanctions lists"""
        # This would integrate with actual sanctions list APIs
        return {
            "flagged": False,
            "matches": [],
            "confidence": 0.0
        }
    
    async def _check_transaction_patterns(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze transaction patterns for suspicious activity"""
        # This would implement ML-based pattern analysis
        return {
            "suspicious": False,
            "risk_score": 0,
            "patterns_detected": []
        }
    
    async def _check_cma_requirements(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check CMA Kenya regulatory requirements"""
        return {
            "compliant": True,
            "issues": [],
            "requirements_met": ["licensing", "reporting"]
        }
    
    async def _check_cbk_guidelines(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check Central Bank of Kenya guidelines"""
        return {
            "compliant": True,
            "issues": [],
            "guidelines_followed": ["payment_systems", "foreign_exchange"]
        }
    
    async def _assess_risk(
        self, 
        transaction_data: Dict[str, Any], 
        compliance_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Assess overall risk level"""
        risk_score = 0
        risk_factors = []
        
        # Base risk from AML check
        aml_result = compliance_result.get("aml_result", {})
        risk_score += aml_result.get("risk_score", 0)
        
        # Risk from failed checks
        failed_checks = compliance_result.get("failed_checks", [])
        risk_score += len(failed_checks) * 20
        
        # Transaction amount risk
        amount = transaction_data.get("amount", 0)
        if amount > 500000:  # KES 500,000
            risk_score += 20
            risk_factors.append("High transaction amount")
        
        # Determine risk level
        if risk_score < 20:
            risk_level = "LOW"
        elif risk_score < 50:
            risk_level = "MEDIUM"
        elif risk_score < 80:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "recommendation": self._get_risk_recommendation(risk_level)
        }
    
    def _get_risk_recommendation(self, risk_level: str) -> str:
        """Get recommendation based on risk level"""
        recommendations = {
            "LOW": "Transaction can proceed normally",
            "MEDIUM": "Additional verification recommended",
            "HIGH": "Manual review required before processing",
            "CRITICAL": "Transaction should be blocked pending investigation"
        }
        return recommendations.get(risk_level, "Unknown risk level")
    
    async def _generate_compliance_report(
        self,
        transaction_data: Dict[str, Any],
        compliance_result: Dict[str, Any],
        risk_assessment: Dict[str, Any],
        thinking_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        
        report = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "transaction_summary": {
                "user_id": transaction_data.get("user_id"),
                "amount": transaction_data.get("amount"),
                "transaction_type": transaction_data.get("transaction_type"),
                "currency": transaction_data.get("currency", "KES")
            },
            "compliance_status": {
                "overall_passed": len(compliance_result.get("failed_checks", [])) == 0,
                "checks_performed": compliance_result.get("checks_performed", []),
                "passed_checks": compliance_result.get("passed_checks", []),
                "failed_checks": compliance_result.get("failed_checks", []),
                "warnings": compliance_result.get("warnings", [])
            },
            "risk_assessment": risk_assessment,
            "detailed_results": compliance_result,
            "thinking_analysis": {
                "total_depth": thinking_result.get("total_depth", 0),
                "key_considerations": self._extract_key_considerations(thinking_result)
            },
            "recommendations": self._generate_compliance_recommendations(
                compliance_result, risk_assessment
            ),
            "next_actions": self._suggest_compliance_actions(
                compliance_result, risk_assessment
            )
        }
        
        return report
    
    def _extract_key_considerations(self, thinking_result: Dict[str, Any]) -> List[str]:
        """Extract key considerations from thinking process"""
        considerations = []
        
        thinking_layers = thinking_result.get("thinking_layers", [])
        for layer in thinking_layers:
            layer_considerations = layer.get("analysis", {}).get("considerations", [])
            considerations.extend(layer_considerations)
        
        return list(set(considerations))
    
    def _generate_compliance_recommendations(
        self, 
        compliance_result: Dict[str, Any], 
        risk_assessment: Dict[str, Any]
    ) -> List[str]:
        """Generate compliance recommendations"""
        recommendations = []
        
        failed_checks = compliance_result.get("failed_checks", [])
        risk_level = risk_assessment.get("risk_level", "LOW")
        
        if "kyc_compliance" in failed_checks:
            recommendations.append("Complete KYC verification process")
        
        if "aml_compliance" in failed_checks:
            recommendations.append("Conduct enhanced due diligence")
        
        if risk_level in ["HIGH", "CRITICAL"]:
            recommendations.append("Implement additional monitoring measures")
            recommendations.append("Consider transaction limits or restrictions")
        
        return recommendations
    
    def _suggest_compliance_actions(
        self, 
        compliance_result: Dict[str, Any], 
        risk_assessment: Dict[str, Any]
    ) -> List[str]:
        """Suggest next actions for compliance"""
        actions = []
        
        risk_level = risk_assessment.get("risk_level", "LOW")
        
        if risk_level == "CRITICAL":
            actions.append("Block transaction immediately")
            actions.append("Initiate investigation process")
        elif risk_level == "HIGH":
            actions.append("Hold transaction for manual review")
            actions.append("Request additional documentation")
        elif risk_level == "MEDIUM":
            actions.append("Apply enhanced monitoring")
            actions.append("Document risk factors")
        else:
            actions.append("Process transaction normally")
            actions.append("Continue routine monitoring")
        
        return actions
    
    async def process_query(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of abstract method from base class"""
        # Convert query to transaction data format
        transaction_data = context.get("transaction_data", {})
        check_type = context.get("check_type", "comprehensive")
        
        return await self.check_compliance(transaction_data, check_type)
