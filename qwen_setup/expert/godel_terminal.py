#!/usr/bin/env python3
"""
GÖDEL MACHINE: Terminal Visualization

A live ASCII visualization of the Gödel Machine running in your terminal.
Watch the strange loops spin, incompleteness detected, and decisions made.
"""

import sys
import os
import time
import random
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from godel_numbers import GodelEncoder, GodelStrategyFactory
from introspection_engine import IntrospectionEngine
from meta_predictor import MetaPredictor
from incompleteness_detector import IncompletenessDetector, MarketState, IncompletenessType
from recursive_self_improvement import RecursiveSelfImprover
from godel_machine import GodelMachine

# ANSI color codes
class C:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'


def clear_screen():
    print('\033[2J\033[H', end='')


def move_cursor(row, col):
    print(f'\033[{row};{col}H', end='')


def draw_box(row, col, width, height, title="", color=C.CYAN):
    """Draw a box with optional title"""
    move_cursor(row, col)
    print(f"{color}╔{'═' * (width-2)}╗{C.RESET}")

    if title:
        title_str = f" {title} "
        padding = (width - 2 - len(title_str)) // 2
        move_cursor(row, col + padding + 1)
        print(f"{color}{C.BOLD}{title_str}{C.RESET}")

    for i in range(1, height - 1):
        move_cursor(row + i, col)
        print(f"{color}║{' ' * (width-2)}║{C.RESET}")

    move_cursor(row + height - 1, col)
    print(f"{color}╚{'═' * (width-2)}╝{C.RESET}")


def draw_progress_bar(row, col, width, value, max_value=1.0, color=C.GREEN):
    """Draw a progress bar"""
    filled = int((value / max_value) * (width - 2))
    empty = width - 2 - filled
    bar = f"{color}{'█' * filled}{C.DIM}{'░' * empty}{C.RESET}"
    move_cursor(row, col)
    print(f"[{bar}] {value*100:5.1f}%")


def draw_strange_loop(row, col, active=False, frame=0):
    """Draw an animated strange loop symbol"""
    if active:
        frames = ['◐', '◓', '◑', '◒']
        symbol = frames[frame % 4]
        color = C.MAGENTA
    else:
        symbol = '○'
        color = C.DIM

    move_cursor(row, col)
    print(f"{color}{C.BOLD}  ∞ {symbol} ∞  {C.RESET}")


def format_godel_number(num):
    """Format a Gödel number for display"""
    if num is None:
        return "---"
    s = str(num)
    if len(s) > 12:
        return s[:6] + ".." + s[-4:]
    return s


def run_terminal_visualization():
    """Run the terminal-based Gödel Machine visualization"""

    # Create the machine
    machine = GodelMachine(
        name="GodelMachine_Terminal",
        enable_self_improvement=True,
        max_meta_depth=3,
        incompleteness_sensitivity=0.7
    )

    price = 45000
    frame = 0

    # Header
    clear_screen()
    print(f"""
{C.CYAN}{C.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                          ⟨ THE GÖDEL MACHINE ⟩                               ║
║                   "I am the strange loop that trades itself"                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
{C.RESET}
{C.DIM}Press Ctrl+C to stop{C.RESET}
""")

    try:
        while True:
            frame += 1

            # Generate market data
            price_change = random.gauss(0, 0.02)
            price *= (1 + price_change)

            market_data = {
                "price": price,
                "prev_price": price / (1 + price_change),
                "volume": random.uniform(500000, 2000000),
                "rsi": random.uniform(20, 80),
                "macd": random.gauss(0, 0.5),
                "momentum": price_change * 10,
                "trend": random.uniform(-1, 1),
                "sentiment": random.uniform(0.2, 0.8) if random.random() > 0.3 else None,
                "volatility": random.uniform(0.1, 0.5) if random.random() > 0.2 else None
            }

            # Process through Gödel Machine
            decision = machine.process_market_state(market_data)

            # Clear and redraw
            move_cursor(7, 1)

            # Market Price
            change_color = C.GREEN if price_change >= 0 else C.RED
            change_str = f"{'+' if price_change >= 0 else ''}{price_change*100:.2f}%"
            print(f"""
{C.BOLD}┌─ MARKET STATE ─────────────────────────────────────────────────────────────┐{C.RESET}
│  Price: {C.WHITE}{C.BOLD}${price:,.0f}{C.RESET}  {change_color}{change_str}{C.RESET}                                              │
│  Volume: {market_data['volume']/1000000:.2f}M   RSI: {market_data['rsi']:.1f}   MACD: {market_data['macd']:+.2f}                      │
└─────────────────────────────────────────────────────────────────────────────┘
""")

            # Decision
            action_colors = {
                'buy': C.GREEN,
                'sell': C.RED,
                'hold': C.YELLOW,
                'abstain': C.MAGENTA
            }
            action_color = action_colors.get(decision.action, C.WHITE)

            print(f"""
{C.BOLD}┌─ DECISION ───────────────────────────────────────────────────────────────────┐{C.RESET}
│                                                                               │
│      {action_color}{C.BOLD}╔═══════════════════╗{C.RESET}                                                │
│      {action_color}{C.BOLD}║  {decision.action.upper():^15s}  ║{C.RESET}                                                │
│      {action_color}{C.BOLD}╚═══════════════════╝{C.RESET}                                                │
│                                                                               │
│  Gödel Number: {C.CYAN}{format_godel_number(decision.godel_number):^15s}{C.RESET}                                        │
│                                                                               │
│  Confidence:      [{C.GREEN}{'█' * int(decision.confidence * 20)}{C.DIM}{'░' * (20 - int(decision.confidence * 20))}{C.RESET}] {decision.confidence*100:5.1f}%      │
│  Meta-Confidence: [{C.MAGENTA}{'█' * int(decision.meta_confidence * 20)}{C.DIM}{'░' * (20 - int(decision.meta_confidence * 20))}{C.RESET}] {decision.meta_confidence*100:5.1f}%      │
│                                                                               │
└───────────────────────────────────────────────────────────────────────────────┘
""")

            # Statistics
            stats = machine.get_machine_state()
            print(f"""
{C.BOLD}┌─ STATISTICS ─────────────────────────────────────────────────────────────────┐{C.RESET}
│  Total Decisions: {C.WHITE}{stats['total_decisions']:>5}{C.RESET}    Abstentions: {C.MAGENTA}{stats['abstentions']:>5}{C.RESET}                           │
│  Paradoxes: {C.RED}{stats['paradoxes_encountered']:>5}{C.RESET}          Self-Improvements: {C.GREEN}{stats['self_improvements']:>5}{C.RESET}                   │
└───────────────────────────────────────────────────────────────────────────────┘
""")

            # Strange Loop & Incompleteness
            loop_status = f"{C.MAGENTA}{C.BOLD}ACTIVE ∞{C.RESET}" if decision.strange_loop_active else f"{C.DIM}inactive{C.RESET}"

            if decision.incompleteness_detected:
                incomp_status = f"{C.YELLOW}{C.BOLD}⚠ {decision.incompleteness_type.name if decision.incompleteness_type else 'DETECTED'}{C.RESET}"
            else:
                incomp_status = f"{C.GREEN}Clear{C.RESET}"

            print(f"""
{C.BOLD}┌─ GÖDELIAN STATE ─────────────────────────────────────────────────────────────┐{C.RESET}
│  Strange Loop: {loop_status:^30s}                                    │
│  Incompleteness: {incomp_status:<45s}    │
│  Cognitive State: {C.CYAN}{stats['cognitive_state']:<20s}{C.RESET}                                  │
│  Meta-Depth Reached: {stats['meta_depth_reached']}                                                      │
└───────────────────────────────────────────────────────────────────────────────┘
""")

            # Meta Tower
            tower_visual = ""
            for i in range(4):
                if i == 0:
                    tower_visual += f"  L{i}: {C.GREEN}█{C.RESET} Base Prediction\n"
                elif i <= stats['meta_depth_reached']:
                    tower_visual += f"  L{i}: {C.CYAN}█{C.RESET} Meta-Level {i}\n"
                else:
                    tower_visual += f"  L{i}: {C.DIM}░ (not reached){C.RESET}\n"

            print(f"""
{C.BOLD}┌─ META-PREDICTION TOWER ──────────────────────────────────────────────────────┐{C.RESET}
{tower_visual}└───────────────────────────────────────────────────────────────────────────────┘
""")

            # Philosophy
            philosophy = decision.philosophical_note[:75] + "..." if len(decision.philosophical_note) > 75 else decision.philosophical_note
            print(f"""
{C.BOLD}┌─ PHILOSOPHICAL NOTE ─────────────────────────────────────────────────────────┐{C.RESET}
│ {C.DIM}"{philosophy}"{C.RESET}
└───────────────────────────────────────────────────────────────────────────────┘
""")

            # Reasoning
            reasoning = decision.reasoning[:75] + "..." if len(decision.reasoning) > 75 else decision.reasoning
            print(f"""
{C.BOLD}┌─ REASONING ──────────────────────────────────────────────────────────────────┐{C.RESET}
│ {reasoning:<77s}│
└───────────────────────────────────────────────────────────────────────────────┘
""")

            time.sleep(2)

    except KeyboardInterrupt:
        print(f"\n\n{C.CYAN}Gödel Machine stopped.{C.RESET}")
        print(f"\nFinal Statistics:")
        print(f"  Total Decisions: {machine.total_decisions}")
        print(f"  Abstentions: {machine.abstentions}")
        print(f"  Paradoxes: {machine.paradoxes_encountered}")
        print(f"  Self-Improvements: {machine.self_improvements}")


if __name__ == "__main__":
    run_terminal_visualization()
