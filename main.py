"""
AI Income Agents — entry point.
Run: python main.py
"""

from agents.coordinator import run_session
from config.settings import ANTHROPIC_API_KEY

if __name__ == "__main__":
    if not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY missing. Copy .env.example to .env and add your key.")
        exit(1)
    run_session()
