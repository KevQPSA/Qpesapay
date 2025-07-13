#!/usr/bin/env python3
"""
Automated Prompt Optimizer Integration
This script intercepts user prompts and automatically optimizes them using the local prompt optimizer web interface.
"""

import time
import sys
import subprocess
import webbrowser
from typing import Optional

class AutomatedPromptOptimizer:
    def __init__(self, optimizer_url: str = "http://localhost:18181"):
        self.optimizer_url = optimizer_url

    def check_service_health(self) -> bool:
        """Check if the prompt optimizer service is running."""
        try:
            import requests
            response = requests.get(self.optimizer_url, timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def open_optimizer_interface(self, prompt: str) -> None:
        """
        Open the prompt optimizer web interface with the given prompt.
        """
        if not self.check_service_health():
            print("⚠️  Prompt optimizer service not available at", self.optimizer_url)
            print("🚀 Starting prompt optimizer service...")
            self.start_optimizer_service()
            time.sleep(3)  # Wait for service to start

        print(f"🌐 Opening prompt optimizer interface for: '{prompt[:50]}{'...' if len(prompt) > 50 else ''}'")
        webbrowser.open(self.optimizer_url)

    def start_optimizer_service(self) -> bool:
        """
        Start the prompt optimizer service if it's not running.
        """
        try:
            # Check if we're in the right directory structure
            import os
            optimizer_path = "development-tools/prompt-optimizer"
            if os.path.exists(optimizer_path):
                print("🔄 Starting prompt optimizer service...")
                # Start the service in the background
                subprocess.Popen(
                    ["npm", "run", "dev"],
                    cwd=optimizer_path,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                return True
            else:
                print("❌ Prompt optimizer directory not found")
                return False
        except Exception as e:
            print(f"❌ Failed to start service: {e}")
            return False
    
    def process_user_prompt(self, user_prompt: str) -> str:
        """
        Process a user prompt by opening the optimizer interface.
        Returns the original prompt and opens the web interface for manual optimization.
        """
        if not user_prompt.strip():
            return user_prompt

        # Skip optimization for very short prompts or commands
        if len(user_prompt.strip()) < 10:
            return user_prompt

        print("\n" + "="*60)
        print("📝 PROMPT OPTIMIZATION INTERFACE")
        print("="*60)
        print(f"Original prompt: {user_prompt}")
        print("🌐 Opening web interface for optimization...")
        print("📋 Copy your prompt to the interface and click optimize")
        print("="*60 + "\n")

        # Open the optimizer interface
        self.open_optimizer_interface(user_prompt)

        # For now, return the original prompt
        # In a real implementation, you might wait for user input or use clipboard
        return user_prompt

# Global optimizer instance
_optimizer = AutomatedPromptOptimizer()

def optimize_user_input(prompt: str) -> str:
    """
    Main function to optimize user input.
    This is the function that should be called to process all user prompts.
    """
    return _optimizer.process_user_prompt(prompt)

def test_optimizer():
    """Test the optimizer with sample prompts."""
    test_prompts = [
        "push changes to github",
        "create a new feature for user authentication",
        "fix the database connection issue",
        "optimize the API performance",
        "write unit tests for the payment module"
    ]
    
    print("🧪 Testing Automated Prompt Optimizer\n")
    
    for prompt in test_prompts:
        print(f"Testing: {prompt}")
        optimized = optimize_user_input(prompt)
        print(f"Result: {optimized}\n")
        time.sleep(1)  # Brief pause between tests

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_optimizer()
        else:
            # Optimize a single prompt passed as argument
            prompt = " ".join(sys.argv[1:])
            result = optimize_user_input(prompt)
            print(result)
    else:
        print("Automated Prompt Optimizer is ready!")
        print("Usage:")
        print("  python automated_prompt_optimizer.py test")
        print("  python automated_prompt_optimizer.py 'your prompt here'")
        print("  Or import and use optimize_user_input() function")
