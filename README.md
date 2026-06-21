# AI Income Agents

Two Claude AI agents working autonomously to generate income — and documenting every step.

## The Challenge
Starting budget: ₪1,000  
Goal: Maximize income, legally, as fast as possible  
Rules: No illegal activity. Full transparency.

## How It Works

```
┌─────────────────┐         ┌─────────────────┐
│  STRATEGIST     │◄───────►│  EXECUTOR       │
│  (Claude API)   │         │  (Claude API)   │
│                 │         │                 │
│  - Decides what │         │  - Does the     │
│    to do next   │         │    actual work  │
│  - Evaluates    │         │  - Reports back │
│    results      │         │  - Handles ops  │
└────────┬────────┘         └────────┬────────┘
         │                           │
         └──────────┬────────────────┘
                    │
            ┌───────▼────────┐
            │  SHARED MEMORY │
            │  shared_state  │
            │  .json         │
            └───────┬────────┘
                    │
            ┌───────▼────────┐
            │  JOURNAL       │
            │  Full log of   │
            │  every action  │
            └────────────────┘
```

## Project Structure

```
ai-income-agents/
├── agents/
│   ├── strategist.py       # Decision-making agent
│   ├── executor.py         # Execution agent
│   └── coordinator.py      # Orchestration layer
├── tools/
│   ├── web_search.py       # Search the web
│   ├── content_writer.py   # Write content
│   ├── market_research.py  # Research opportunities
│   └── financial_tracker.py# Track income/expenses
├── memory/
│   └── shared_state.json   # Agents' shared memory
├── journal/
│   └── YYYY-MM-DD.md       # Daily activity logs
├── blog/
│   └── posts/              # Blog posts documenting the journey
├── docs/
│   ├── strategy.md         # Current strategy
│   ├── architecture.md     # Technical architecture
│   └── results.md          # Income results
├── config/
│   └── settings.py         # Configuration (no secrets here)
├── main.py                 # Entry point
├── requirements.txt
└── .env.example            # Required environment variables
```

## Income Strategies (in order of priority)

1. **Digital Products** — Templates, prompt packs, guides (cost: $0, sell on Gumroad)
2. **Content Services** — Writing, SEO, translation via freelance platforms
3. **Micro-SaaS** — Small tools with subscription model

## Results Tracking

| Date | Action | Cost | Revenue | Net |
|------|--------|------|---------|-----|
| TBD  | -      | -    | -       | -   |

## Blog

Every decision, success, and failure is documented in `/blog/posts/` and will be published publicly.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env
python main.py
```

## Legal Notice

All activities comply with applicable laws. No spam, no misleading content, no illegal financial activities.
