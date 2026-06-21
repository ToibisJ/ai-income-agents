import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

STRATEGIST_MODEL = "claude-opus-4-8"
EXECUTOR_MODEL = "claude-sonnet-4-6"

BUDGET_ILS = 1000
BUDGET_USD = BUDGET_ILS / 3.7  # approximate

MAX_SPEND_PER_ACTION_USD = 20

MEMORY_PATH = "memory/shared_state.json"
JOURNAL_DIR = "journal"
BLOG_DIR = "blog/posts"
