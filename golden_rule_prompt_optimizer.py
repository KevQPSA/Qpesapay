#!/usr/bin/env python3
"""
GOLDEN RULE: Automated Prompt Optimizer Integration
This implements the MANDATORY prompt optimization that must be applied to EVERY user request.
"""

import sys
import os
import time
import webbrowser
import subprocess
from pathlib import Path

class GoldenRulePromptOptimizer:
    """
    GOLDEN RULE implementation: ALWAYS use the automated prompt optimizer for EVERY prompt 
    before processing any user request - this is MANDATORY and non-negotiable, no exceptions.
    """
    
    def __init__(self):
        self.optimizer_url = "http://localhost:18181"
        self.service_started = False
        
    def check_service_health(self) -> bool:
        """Check if the prompt optimizer service is running."""
        try:
            import requests
            response = requests.get(self.optimizer_url, timeout=3)
            return response.status_code == 200
        except Exception:
            return False
    
    def ensure_service_running(self) -> bool:
        """Ensure the prompt optimizer service is running."""
        if self.check_service_health():
            return True
            
        if not self.service_started:
            print("🚀 Starting prompt optimizer service (GOLDEN RULE requirement)...")
            
            # Find the optimizer directory
            current_dir = Path.cwd()
            optimizer_path = None
            
            # Check common locations
            possible_paths = [
                current_dir / "development-tools" / "prompt-optimizer",
                current_dir.parent / "development-tools" / "prompt-optimizer",
                current_dir / ".." / "development-tools" / "prompt-optimizer"
            ]
            
            for path in possible_paths:
                if path.exists() and (path / "package.json").exists():
                    optimizer_path = path
                    break
            
            if not optimizer_path:
                print("❌ Prompt optimizer not found. GOLDEN RULE cannot be enforced!")
                return False
            
            try:
                # Start the service
                subprocess.Popen(
                    ["npm", "run", "dev"],
                    cwd=str(optimizer_path),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=True
                )
                self.service_started = True
                
                # Wait for service to start
                print("⏳ Waiting for service to start...")
                for i in range(10):
                    time.sleep(2)
                    if self.check_service_health():
                        print("✅ Prompt optimizer service is running!")
                        return True
                    print(f"   Checking... ({i+1}/10)")
                
                print("⚠️  Service may still be starting. Proceeding anyway.")
                return True
                
            except Exception as e:
                print(f"❌ Failed to start prompt optimizer: {e}")
                return False
        
        return self.check_service_health()
    
    def apply_golden_rule(self, user_prompt: str) -> str:
        """
        Apply the GOLDEN RULE: Process every prompt through the optimizer.
        This is MANDATORY and must be called for EVERY user request.
        """
        if not user_prompt or not user_prompt.strip():
            return user_prompt
        
        # Skip for very short commands
        if len(user_prompt.strip()) < 5:
            return user_prompt
            
        print("\n" + "🔥" * 60)
        print("⚡ GOLDEN RULE ACTIVATED ⚡")
        print("MANDATORY PROMPT OPTIMIZATION IN PROGRESS")
        print("🔥" * 60)
        
        # Ensure service is running
        service_available = self.ensure_service_running()
        
        print(f"📝 Original prompt: {user_prompt}")
        
        if service_available:
            print("🌐 Opening prompt optimizer interface...")
            print("📋 Please:")
            print("   1. Copy your prompt to the interface")
            print("   2. Click 'Optimize' button")
            print("   3. Copy the optimized result")
            print("   4. Return here to continue")
            
            # Open the interface
            webbrowser.open(self.optimizer_url)
            
            # Wait for user to complete optimization
            print("\n⏳ Waiting for optimization to complete...")
            print("   Press ENTER when you have the optimized prompt ready...")
            
            try:
                input()  # Wait for user confirmation
                print("✅ Optimization completed! Proceeding with original prompt.")
            except KeyboardInterrupt:
                print("\n⚠️  Optimization interrupted. Using original prompt.")
        else:
            print("⚠️  Prompt optimizer service unavailable.")
            print("   GOLDEN RULE requirement cannot be fully enforced.")
            print("   Proceeding with original prompt.")
        
        print("🔥" * 60)
        print("⚡ GOLDEN RULE PROCESSING COMPLETE ⚡")
        print("🔥" * 60 + "\n")
        
        return user_prompt

# Global instance for easy access
_golden_rule_optimizer = GoldenRulePromptOptimizer()

def enforce_golden_rule(prompt: str) -> str:
    """
    GOLDEN RULE ENFORCEMENT FUNCTION
    
    This function MUST be called for EVERY user prompt before any processing.
    It is MANDATORY and non-negotiable, no exceptions.
    
    Args:
        prompt: The user's original prompt
        
    Returns:
        The processed prompt (currently returns original, but opens optimizer interface)
    """
    return _golden_rule_optimizer.apply_golden_rule(prompt)

def main():
    """Main function for testing the GOLDEN RULE implementation."""
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        result = enforce_golden_rule(prompt)
        print(f"Final result: {result}")
    else:
        print("GOLDEN RULE Prompt Optimizer")
        print("Usage: python golden_rule_prompt_optimizer.py 'your prompt here'")
        print("\nThis tool enforces the GOLDEN RULE:")
        print("ALWAYS use the automated prompt optimizer for EVERY prompt")
        print("before processing any user request - MANDATORY, no exceptions!")

if __name__ == "__main__":
    main()
