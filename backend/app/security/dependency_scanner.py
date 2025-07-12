"""
OWASP-compliant Dependency Vulnerability Scanner
Implements automated dependency security scanning as per OWASP recommendations
"""

import subprocess
import json
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import pkg_resources
import re

from app.core.logging import security_logger, get_logger

logger = get_logger(__name__)


class DependencyVulnerabilityScanner:
    """
    OWASP-compliant dependency vulnerability scanner.
    Scans for known vulnerabilities in project dependencies.
    """
    
    def __init__(self):
        self.vulnerability_databases = {
            "pyup": "https://pyup.io/api/v1/safety/",
            "osv": "https://osv.dev/v1/query",
            "github": "https://api.github.com/advisories"
        }
        self.critical_packages = [
            "fastapi", "sqlalchemy", "pydantic", "cryptography", 
            "bcrypt", "pyjwt", "requests", "urllib3"
        ]
    
    def scan_dependencies(self) -> Dict[str, Any]:
        """
        Perform comprehensive dependency vulnerability scan.
        
        Returns:
            Dict: Vulnerability scan results
        """
        logger.info("Starting dependency vulnerability scan")
        
        results = {
            "scan_timestamp": datetime.now(timezone.utc).isoformat(),
            "total_packages": 0,
            "vulnerable_packages": 0,
            "critical_vulnerabilities": 0,
            "high_vulnerabilities": 0,
            "medium_vulnerabilities": 0,
            "low_vulnerabilities": 0,
            "vulnerabilities": [],
            "recommendations": [],
            "scan_status": "SUCCESS"
        }
        
        try:
            # Get installed packages
            installed_packages = self._get_installed_packages()
            results["total_packages"] = len(installed_packages)
            
            # Scan with multiple sources
            vulnerabilities = []
            
            # Scan with safety (PyUp.io database)
            safety_vulns = self._scan_with_safety()
            vulnerabilities.extend(safety_vulns)
            
            # Scan with OSV database
            osv_vulns = self._scan_with_osv(installed_packages)
            vulnerabilities.extend(osv_vulns)
            
            # Check for outdated packages
            outdated_vulns = self._check_outdated_packages(installed_packages)
            vulnerabilities.extend(outdated_vulns)
            
            # Process results
            results["vulnerabilities"] = vulnerabilities
            results["vulnerable_packages"] = len(set(v["package"] for v in vulnerabilities))
            
            # Categorize by severity
            for vuln in vulnerabilities:
                severity = vuln.get("severity", "UNKNOWN").upper()
                if severity == "CRITICAL":
                    results["critical_vulnerabilities"] += 1
                elif severity == "HIGH":
                    results["high_vulnerabilities"] += 1
                elif severity == "MEDIUM":
                    results["medium_vulnerabilities"] += 1
                elif severity == "LOW":
                    results["low_vulnerabilities"] += 1
            
            # Generate recommendations
            results["recommendations"] = self._generate_recommendations(vulnerabilities)
            
            # Log critical vulnerabilities
            if results["critical_vulnerabilities"] > 0:
                security_logger.log_suspicious_activity(
                    user_id="system",
                    activity_type="critical_vulnerabilities_found",
                    details={
                        "critical_count": results["critical_vulnerabilities"],
                        "total_vulnerabilities": len(vulnerabilities)
                    },
                    ip_address="localhost"
                )
            
        except Exception as e:
            logger.error(f"Dependency scan failed: {str(e)}")
            results["scan_status"] = "FAILED"
            results["error"] = str(e)
        
        return results
    
    def _get_installed_packages(self) -> Dict[str, str]:
        """Get list of installed packages with versions."""
        packages = {}
        for dist in pkg_resources.working_set:
            packages[dist.project_name.lower()] = dist.version
        return packages
    
    def _scan_with_safety(self) -> List[Dict[str, Any]]:
        """Scan dependencies using Safety (PyUp.io database)."""
        vulnerabilities = []
        
        try:
            # Run safety check
            result = subprocess.run(
                ["python", "-m", "safety", "check", "--json"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # No vulnerabilities found
                return vulnerabilities
            
            # Parse safety output
            if result.stdout:
                safety_data = json.loads(result.stdout)
                for vuln in safety_data:
                    vulnerabilities.append({
                        "package": vuln.get("package", "unknown"),
                        "version": vuln.get("installed_version", "unknown"),
                        "vulnerability_id": vuln.get("id", "unknown"),
                        "severity": self._map_safety_severity(vuln.get("id", "")),
                        "description": vuln.get("advisory", "No description"),
                        "fixed_version": vuln.get("fixed_version", "unknown"),
                        "source": "safety"
                    })
            
        except subprocess.TimeoutExpired:
            logger.warning("Safety scan timed out")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Safety scan failed: {e}")
        except Exception as e:
            logger.warning(f"Safety scan error: {e}")
        
        return vulnerabilities
    
    def _scan_with_osv(self, packages: Dict[str, str]) -> List[Dict[str, Any]]:
        """Scan dependencies using OSV database."""
        vulnerabilities = []
        
        # Only scan critical packages to avoid rate limiting
        critical_installed = {
            name: version for name, version in packages.items()
            if name in self.critical_packages
        }
        
        for package, version in critical_installed.items():
            try:
                # Query OSV API
                query = {
                    "package": {"name": package, "ecosystem": "PyPI"},
                    "version": version
                }
                
                response = requests.post(
                    self.vulnerability_databases["osv"],
                    json=query,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "vulns" in data:
                        for vuln in data["vulns"]:
                            vulnerabilities.append({
                                "package": package,
                                "version": version,
                                "vulnerability_id": vuln.get("id", "unknown"),
                                "severity": self._extract_osv_severity(vuln),
                                "description": vuln.get("summary", "No description"),
                                "fixed_version": self._extract_fixed_version(vuln),
                                "source": "osv"
                            })
                
            except requests.RequestException as e:
                logger.warning(f"OSV scan failed for {package}: {e}")
            except Exception as e:
                logger.warning(f"OSV scan error for {package}: {e}")
        
        return vulnerabilities
    
    def _check_outdated_packages(self, packages: Dict[str, str]) -> List[Dict[str, Any]]:
        """Check for critically outdated packages."""
        vulnerabilities = []
        
        # Define packages that are critically outdated if too old
        critical_age_limits = {
            "cryptography": "3.0.0",
            "requests": "2.25.0",
            "urllib3": "1.26.0",
            "pyjwt": "2.0.0"
        }
        
        for package, min_version in critical_age_limits.items():
            if package in packages:
                current_version = packages[package]
                if self._is_version_older(current_version, min_version):
                    vulnerabilities.append({
                        "package": package,
                        "version": current_version,
                        "vulnerability_id": f"OUTDATED_{package.upper()}",
                        "severity": "MEDIUM",
                        "description": f"Package {package} is critically outdated (current: {current_version}, minimum recommended: {min_version})",
                        "fixed_version": f">={min_version}",
                        "source": "age_check"
                    })
        
        return vulnerabilities
    
    def _map_safety_severity(self, vuln_id: str) -> str:
        """Map Safety vulnerability ID to severity level."""
        # Safety doesn't provide severity, so we estimate based on ID patterns
        if any(keyword in vuln_id.lower() for keyword in ["rce", "injection", "auth"]):
            return "CRITICAL"
        elif any(keyword in vuln_id.lower() for keyword in ["xss", "csrf", "dos"]):
            return "HIGH"
        else:
            return "MEDIUM"
    
    def _extract_osv_severity(self, vuln: Dict[str, Any]) -> str:
        """Extract severity from OSV vulnerability data."""
        # Check for CVSS score
        if "severity" in vuln:
            for severity_info in vuln["severity"]:
                if "score" in severity_info:
                    score = float(severity_info["score"])
                    if score >= 9.0:
                        return "CRITICAL"
                    elif score >= 7.0:
                        return "HIGH"
                    elif score >= 4.0:
                        return "MEDIUM"
                    else:
                        return "LOW"
        
        # Fallback to summary analysis
        summary = vuln.get("summary", "").lower()
        if any(keyword in summary for keyword in ["critical", "rce", "remote code"]):
            return "CRITICAL"
        elif any(keyword in summary for keyword in ["high", "injection", "auth"]):
            return "HIGH"
        else:
            return "MEDIUM"
    
    def _extract_fixed_version(self, vuln: Dict[str, Any]) -> str:
        """Extract fixed version from OSV vulnerability data."""
        if "affected" in vuln:
            for affected in vuln["affected"]:
                if "ranges" in affected:
                    for range_info in affected["ranges"]:
                        if "events" in range_info:
                            for event in range_info["events"]:
                                if "fixed" in event:
                                    return event["fixed"]
        return "unknown"
    
    def _is_version_older(self, current: str, minimum: str) -> bool:
        """Check if current version is older than minimum required."""
        try:
            from packaging import version
            return version.parse(current) < version.parse(minimum)
        except Exception:
            # Fallback to string comparison
            return current < minimum
    
    def _generate_recommendations(self, vulnerabilities: List[Dict[str, Any]]) -> List[str]:
        """Generate security recommendations based on vulnerabilities."""
        recommendations = []
        
        if not vulnerabilities:
            recommendations.append("✅ No known vulnerabilities found in dependencies")
            return recommendations
        
        # Critical vulnerabilities
        critical_vulns = [v for v in vulnerabilities if v.get("severity") == "CRITICAL"]
        if critical_vulns:
            recommendations.append(f"🚨 URGENT: Fix {len(critical_vulns)} critical vulnerabilities immediately")
            for vuln in critical_vulns[:3]:  # Show top 3
                recommendations.append(f"   - Update {vuln['package']} to {vuln['fixed_version']}")
        
        # High vulnerabilities
        high_vulns = [v for v in vulnerabilities if v.get("severity") == "HIGH"]
        if high_vulns:
            recommendations.append(f"⚠️ HIGH: Fix {len(high_vulns)} high-severity vulnerabilities")
        
        # General recommendations
        recommendations.extend([
            "🔄 Run dependency updates regularly (weekly)",
            "🤖 Implement automated dependency scanning in CI/CD",
            "📊 Monitor security advisories for critical packages",
            "🔒 Consider using dependency pinning for production"
        ])
        
        return recommendations


def run_dependency_scan():
    """Run dependency vulnerability scan."""
    scanner = DependencyVulnerabilityScanner()
    return scanner.scan_dependencies()


if __name__ == "__main__":
    import json
    results = run_dependency_scan()
    print(json.dumps(results, indent=2))
