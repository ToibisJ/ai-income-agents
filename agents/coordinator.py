"""
Coordinator: manages the conversation between Strategist and Executor agents.
Loads shared state, runs a session, saves results, writes journal entry.
"""

import json
import os
from datetime import datetime
from pathlib import Path

import anthropic
from rich.console import Console
from rich.panel import Panel

from config.settings import (
    ANTHROPIC_API_KEY,
    STRATEGIST_MODEL,
    EXECUTOR_MODEL,
    MEMORY_PATH,
    JOURNAL_DIR,
)

console = Console()
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def load_state() -> dict:
    with open(MEMORY_PATH) as f:
        return json.load(f)


def save_state(state: dict):
    with open(MEMORY_PATH, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def write_journal(session: int, log: list[dict]):
    Path(JOURNAL_DIR).mkdir(exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    path = f"{JOURNAL_DIR}/{date}-session-{session}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Session {session} — {date}\n\n")
        for entry in log:
            f.write(f"## [{entry['time']}] {entry['role'].upper()}\n\n")
            f.write(entry["content"] + "\n\n---\n\n")
    console.print(f"[green]Journal saved: {path}[/green]")


def ask_strategist(state: dict, executor_report: str | None = None) -> str:
    context = json.dumps(state, ensure_ascii=False, indent=2)
    messages = [
        {
            "role": "user",
            "content": f"""You are the STRATEGIST agent in a two-agent system.
Your goal: maximize legal income starting with ₪1,000 budget.

SHARED STATE:
{context}

{"EXECUTOR REPORT:\n" + executor_report if executor_report else "This is the first session."}

Analyze the situation and decide:
1. What is the best income strategy right now?
2. What specific action should the Executor take next?
3. What is the expected ROI and timeline?

Be concrete. Give the Executor a clear, actionable task.
Format: STRATEGY / NEXT ACTION / EXPECTED OUTCOME""",
        }
    ]

    response = client.messages.create(
        model=STRATEGIST_MODEL,
        max_tokens=1024,
        messages=messages,
    )
    return response.content[0].text


def ask_executor(state: dict, strategist_instruction: str) -> str:
    context = json.dumps(state, ensure_ascii=False, indent=2)
    messages = [
        {
            "role": "user",
            "content": f"""You are the EXECUTOR agent in a two-agent system.
Your goal: carry out the Strategist's instructions and report results.

SHARED STATE:
{context}

STRATEGIST INSTRUCTION:
{strategist_instruction}

Execute the task (or simulate execution if no external tools are available yet).
Report: what you did, what worked, what didn't, and what you need next.
Format: ACTIONS TAKEN / RESULTS / BLOCKERS / NEXT NEEDS""",
        }
    ]

    response = client.messages.create(
        model=EXECUTOR_MODEL,
        max_tokens=1024,
        messages=messages,
    )
    return response.content[0].text


def run_session():
    state = load_state()
    state["session"] += 1
    if not state["started"]:
        state["started"] = datetime.now().isoformat()

    session_num = state["session"]
    log = []

    console.print(Panel(f"[bold cyan]Session {session_num}[/bold cyan]", expand=False))

    # Strategist thinks first
    console.print("\n[yellow]STRATEGIST thinking...[/yellow]")
    strategist_output = ask_strategist(state)
    console.print(Panel(strategist_output, title="STRATEGIST", border_style="yellow"))
    log.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "role": "strategist",
        "content": strategist_output,
    })

    state["strategist_notes"].append({
        "session": session_num,
        "time": datetime.now().isoformat(),
        "content": strategist_output,
    })

    # Executor acts
    console.print("\n[blue]EXECUTOR acting...[/blue]")
    executor_output = ask_executor(state, strategist_output)
    console.print(Panel(executor_output, title="EXECUTOR", border_style="blue"))
    log.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "role": "executor",
        "content": executor_output,
    })

    state["executor_notes"].append({
        "session": session_num,
        "time": datetime.now().isoformat(),
        "content": executor_output,
    })

    # Strategist evaluates
    console.print("\n[yellow]STRATEGIST evaluating...[/yellow]")
    evaluation = ask_strategist(state, executor_output)
    console.print(Panel(evaluation, title="STRATEGIST EVALUATION", border_style="yellow"))
    log.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "role": "strategist_eval",
        "content": evaluation,
    })

    state["decisions"].append({
        "session": session_num,
        "strategist_plan": strategist_output,
        "executor_result": executor_output,
        "evaluation": evaluation,
    })

    save_state(state)
    write_journal(session_num, log)
    console.print(f"\n[green]Session {session_num} complete.[/green]")
