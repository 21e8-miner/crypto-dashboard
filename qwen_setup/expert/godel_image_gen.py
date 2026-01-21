#!/usr/bin/env python3
"""Generate Gödel Machine visualization as images using matplotlib"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Arc
import numpy as np
import random
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import time

# Style settings
plt.style.use('dark_background')

@dataclass
class MarketState:
    price: float
    change_pct: float
    volume: float
    rsi: float
    macd: float

@dataclass
class GodelState:
    decision: str
    confidence: float
    meta_confidence: float
    godel_number: str
    strange_loop_active: bool
    incompleteness: Optional[str]
    incompleteness_desc: Optional[str]
    meta_level: int
    total_decisions: int
    total_abstentions: int
    total_paradoxes: int
    cognitive_state: str

def generate_godel_number():
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    components = []
    for i in range(random.randint(3, 5)):
        prime = primes[i]
        exp = random.randint(1, 8)
        components.append(f"{prime}^{exp}")
    return " × ".join(components)

INCOMPLETENESS_TYPES = [
    ("REGIME_SUPERPOSITION", "Market is both bull and bear until observed"),
    ("INFORMATION_GAP", "Critical data missing for complete analysis"),
    ("SELF_REFERENCE_PARADOX", "Prediction predicts its own failure"),
    ("HALTING_UNCERTAINTY", "Cannot determine if analysis will terminate"),
]

COGNITIVE_STATES = ["ANALYZING", "INTROSPECTING", "META-COMPUTING", "SELF-MODIFYING"]

def simulate_market() -> MarketState:
    return MarketState(
        price=45000 + random.uniform(-2000, 3000),
        change_pct=random.uniform(-3, 3),
        volume=random.uniform(0.5, 2.0),
        rsi=random.uniform(20, 80),
        macd=random.uniform(-1, 1)
    )

def simulate_godel(market: MarketState, prev_decisions: int, prev_abstentions: int) -> GodelState:
    # 30% chance of incompleteness
    if random.random() < 0.3:
        inc = random.choice(INCOMPLETENESS_TYPES)
        return GodelState(
            decision="ABSTAIN",
            confidence=0,
            meta_confidence=random.uniform(75, 100),
            godel_number="---",
            strange_loop_active=False,
            incompleteness=inc[0],
            incompleteness_desc=inc[1],
            meta_level=random.randint(0, 2),
            total_decisions=prev_decisions + 1,
            total_abstentions=prev_abstentions + 1,
            total_paradoxes=random.randint(0, 2),
            cognitive_state=random.choice(COGNITIVE_STATES)
        )

    # Make decision based on RSI
    if market.rsi < 35:
        decision = "BUY"
    elif market.rsi > 65:
        decision = "SELL"
    else:
        decision = "HOLD"

    strange_loop = random.random() < 0.4

    return GodelState(
        decision=decision,
        confidence=random.uniform(30, 70),
        meta_confidence=random.uniform(10, 50) if strange_loop else random.uniform(40, 70),
        godel_number=generate_godel_number(),
        strange_loop_active=strange_loop,
        incompleteness=None,
        incompleteness_desc=None,
        meta_level=random.randint(0, 3),
        total_decisions=prev_decisions + 1,
        total_abstentions=prev_abstentions,
        total_paradoxes=random.randint(0, 2),
        cognitive_state=random.choice(COGNITIVE_STATES)
    )

def draw_godel_visualization(market: MarketState, godel: GodelState, frame_num: int, price_history: List[float]) -> plt.Figure:
    fig = plt.figure(figsize=(16, 12), facecolor='#0a0a0f')

    # Colors
    cyan = '#00ffff'
    magenta = '#ff00ff'
    green = '#00ff88'
    red = '#ff4444'
    yellow = '#ffff00'
    white = '#ffffff'
    gray = '#888888'
    dark_bg = '#1a1a2e'

    # Title
    fig.text(0.5, 0.96, '⟨ THE GÖDEL MACHINE ⟩', fontsize=28, ha='center',
             color=cyan, fontweight='bold', fontfamily='monospace')
    fig.text(0.5, 0.93, '"I am the strange loop that trades itself"', fontsize=12,
             ha='center', color=gray, style='italic', fontfamily='monospace')

    # Draw strange loop symbol in top right
    ax_loop = fig.add_axes([0.88, 0.90, 0.08, 0.08])
    ax_loop.set_xlim(-1.5, 1.5)
    ax_loop.set_ylim(-1.5, 1.5)
    ax_loop.set_aspect('equal')
    ax_loop.axis('off')

    theta = np.linspace(0, 2*np.pi, 100)
    r1 = 1.0
    r2 = 0.6
    ax_loop.plot(r1*np.cos(theta), r1*np.sin(theta), color=magenta, linewidth=2)
    ax_loop.plot(r2*np.cos(theta), r2*np.sin(theta), color=cyan, linewidth=1.5)
    if godel.strange_loop_active:
        ax_loop.text(0, 0, '∞', fontsize=20, ha='center', va='center', color=magenta, fontweight='bold')

    # === MARKET STATE PANEL ===
    ax_market = fig.add_axes([0.05, 0.60, 0.42, 0.28])
    ax_market.set_facecolor(dark_bg)
    ax_market.set_xlim(0, 10)
    ax_market.set_ylim(0, 10)
    ax_market.axis('off')

    # Panel border
    rect = FancyBboxPatch((0.1, 0.1), 9.8, 9.8, boxstyle="round,pad=0.05",
                          facecolor=dark_bg, edgecolor='#333333', linewidth=2)
    ax_market.add_patch(rect)

    # Title bar
    ax_market.fill_between([0.1, 9.9], [9.9, 9.9], [9.5, 9.5], color=cyan, alpha=0.3)
    ax_market.text(0.5, 9.7, '📊 MARKET STATE', fontsize=11, color=cyan, fontweight='bold', fontfamily='monospace')

    # Price
    change_color = green if market.change_pct >= 0 else red
    change_sign = '+' if market.change_pct >= 0 else ''
    ax_market.text(0.5, 8.0, f'${market.price:,.0f}', fontsize=32, color=white, fontweight='bold', fontfamily='monospace')
    ax_market.text(6.5, 8.0, f'{change_sign}{market.change_pct:.2f}%', fontsize=16, color=change_color, fontfamily='monospace')

    # Mini chart
    if len(price_history) > 1:
        chart_x = np.linspace(0.5, 9.5, len(price_history))
        chart_y = np.array(price_history)
        chart_y_norm = 4.5 + 2.5 * (chart_y - chart_y.min()) / (chart_y.max() - chart_y.min() + 1)
        ax_market.plot(chart_x, chart_y_norm, color=cyan, linewidth=2)
        ax_market.fill_between(chart_x, 4.5, chart_y_norm, alpha=0.2, color=cyan)

    # Stats
    ax_market.text(1.5, 2.0, 'VOLUME', fontsize=9, color=gray, ha='center', fontfamily='monospace')
    ax_market.text(1.5, 1.2, f'{market.volume:.2f}M', fontsize=12, color=white, ha='center', fontfamily='monospace')
    ax_market.text(5.0, 2.0, 'RSI', fontsize=9, color=gray, ha='center', fontfamily='monospace')
    ax_market.text(5.0, 1.2, f'{market.rsi:.1f}', fontsize=12, color=white, ha='center', fontfamily='monospace')
    ax_market.text(8.5, 2.0, 'MACD', fontsize=9, color=gray, ha='center', fontfamily='monospace')
    macd_sign = '+' if market.macd >= 0 else ''
    ax_market.text(8.5, 1.2, f'{macd_sign}{market.macd:.2f}', fontsize=12, color=white, ha='center', fontfamily='monospace')

    # === DECISION PANEL ===
    ax_decision = fig.add_axes([0.53, 0.60, 0.42, 0.28])
    ax_decision.set_facecolor(dark_bg)
    ax_decision.set_xlim(0, 10)
    ax_decision.set_ylim(0, 10)
    ax_decision.axis('off')

    rect = FancyBboxPatch((0.1, 0.1), 9.8, 9.8, boxstyle="round,pad=0.05",
                          facecolor=dark_bg, edgecolor='#333333', linewidth=2)
    ax_decision.add_patch(rect)

    ax_decision.fill_between([0.1, 9.9], [9.9, 9.9], [9.5, 9.5], color=cyan, alpha=0.3)
    ax_decision.text(0.5, 9.7, '🎯 DECISION', fontsize=11, color=cyan, fontweight='bold', fontfamily='monospace')

    # Decision box
    decision_colors = {
        'BUY': ('#004d00', green),
        'SELL': ('#4d0000', red),
        'HOLD': ('#4d4d00', yellow),
        'ABSTAIN': ('#2d004d', magenta)
    }
    bg_col, text_col = decision_colors.get(godel.decision, ('#333333', white))

    decision_box = FancyBboxPatch((2.5, 6.5), 5, 2, boxstyle="round,pad=0.1",
                                   facecolor=bg_col, edgecolor=text_col, linewidth=3)
    ax_decision.add_patch(decision_box)
    ax_decision.text(5, 7.5, godel.decision, fontsize=24, color=text_col,
                     ha='center', va='center', fontweight='bold', fontfamily='monospace')

    # Confidence bars
    ax_decision.text(1, 5.3, 'Confidence', fontsize=9, color=gray, fontfamily='monospace')
    ax_decision.text(9, 5.3, f'{godel.confidence:.0f}%', fontsize=9, color=white, ha='right', fontfamily='monospace')
    conf_bg = FancyBboxPatch((1, 4.5), 8, 0.6, boxstyle="round,pad=0.02", facecolor='#222222', edgecolor='none')
    ax_decision.add_patch(conf_bg)
    conf_fill = FancyBboxPatch((1, 4.5), 8 * godel.confidence / 100, 0.6, boxstyle="round,pad=0.02", facecolor=cyan, edgecolor='none')
    ax_decision.add_patch(conf_fill)

    ax_decision.text(1, 3.5, 'Meta-Confidence', fontsize=9, color=gray, fontfamily='monospace')
    ax_decision.text(9, 3.5, f'{godel.meta_confidence:.0f}%', fontsize=9, color=white, ha='right', fontfamily='monospace')
    meta_bg = FancyBboxPatch((1, 2.7), 8, 0.6, boxstyle="round,pad=0.02", facecolor='#222222', edgecolor='none')
    ax_decision.add_patch(meta_bg)
    meta_fill = FancyBboxPatch((1, 2.7), 8 * godel.meta_confidence / 100, 0.6, boxstyle="round,pad=0.02", facecolor=magenta, edgecolor='none')
    ax_decision.add_patch(meta_fill)

    # Gödel number
    ax_decision.text(1, 1.5, 'Gödel Number:', fontsize=9, color=gray, fontfamily='monospace')
    ax_decision.text(1, 0.7, godel.godel_number, fontsize=10, color=cyan, fontfamily='monospace')

    # === GÖDELIAN STATE PANEL ===
    ax_godel = fig.add_axes([0.05, 0.28, 0.42, 0.28])
    ax_godel.set_facecolor(dark_bg)
    ax_godel.set_xlim(0, 10)
    ax_godel.set_ylim(0, 10)
    ax_godel.axis('off')

    rect = FancyBboxPatch((0.1, 0.1), 9.8, 9.8, boxstyle="round,pad=0.05",
                          facecolor=dark_bg, edgecolor='#333333', linewidth=2)
    ax_godel.add_patch(rect)

    ax_godel.fill_between([0.1, 9.9], [9.9, 9.9], [9.5, 9.5], color=cyan, alpha=0.3)
    ax_godel.text(0.5, 9.7, '∞ GÖDELIAN STATE', fontsize=11, color=cyan, fontweight='bold', fontfamily='monospace')

    # Strange loop status
    loop_status = "ACTIVE ∞" if godel.strange_loop_active else "inactive"
    loop_color = magenta if godel.strange_loop_active else gray
    ax_godel.text(1, 8.2, 'Strange Loop:', fontsize=10, color=gray, fontfamily='monospace')
    ax_godel.text(5, 8.2, loop_status, fontsize=12, color=loop_color, fontweight='bold', fontfamily='monospace')

    # Incompleteness status
    if godel.incompleteness:
        inc_box = FancyBboxPatch((0.5, 4.5), 9, 3, boxstyle="round,pad=0.05",
                                  facecolor='#2d004d', edgecolor=magenta, linewidth=2, alpha=0.5)
        ax_godel.add_patch(inc_box)
        ax_godel.text(1, 6.8, '⚠', fontsize=20, color=magenta, fontfamily='monospace')
        ax_godel.text(2, 6.8, godel.incompleteness, fontsize=11, color=magenta, fontweight='bold', fontfamily='monospace')
        ax_godel.text(1, 5.5, godel.incompleteness_desc, fontsize=9, color=white, fontfamily='monospace', style='italic')
    else:
        inc_box = FancyBboxPatch((0.5, 4.5), 9, 3, boxstyle="round,pad=0.05",
                                  facecolor='#004d00', edgecolor=green, linewidth=2, alpha=0.3)
        ax_godel.add_patch(inc_box)
        ax_godel.text(1, 6.5, '✓', fontsize=20, color=green, fontfamily='monospace')
        ax_godel.text(2, 6.5, 'CLEAR', fontsize=11, color=green, fontweight='bold', fontfamily='monospace')
        ax_godel.text(1, 5.5, 'System can make decisions', fontsize=9, color=white, fontfamily='monospace')

    # Cognitive state
    ax_godel.text(1, 2.5, 'Cognitive State:', fontsize=10, color=gray, fontfamily='monospace')
    ax_godel.text(5, 2.5, godel.cognitive_state, fontsize=11, color=cyan, fontfamily='monospace')

    # Meta depth
    ax_godel.text(1, 1.2, 'Meta-Depth Reached:', fontsize=10, color=gray, fontfamily='monospace')
    ax_godel.text(6.5, 1.2, str(godel.meta_level), fontsize=11, color=white, fontfamily='monospace')

    # === META-PREDICTION TOWER ===
    ax_tower = fig.add_axes([0.53, 0.28, 0.42, 0.28])
    ax_tower.set_facecolor(dark_bg)
    ax_tower.set_xlim(0, 10)
    ax_tower.set_ylim(0, 10)
    ax_tower.axis('off')

    rect = FancyBboxPatch((0.1, 0.1), 9.8, 9.8, boxstyle="round,pad=0.05",
                          facecolor=dark_bg, edgecolor='#333333', linewidth=2)
    ax_tower.add_patch(rect)

    ax_tower.fill_between([0.1, 9.9], [9.9, 9.9], [9.5, 9.5], color=cyan, alpha=0.3)
    ax_tower.text(0.5, 9.7, '🗼 META-PREDICTION TOWER', fontsize=11, color=cyan, fontweight='bold', fontfamily='monospace')

    levels = [
        ("L0", "Base Prediction"),
        ("L1", "Prediction about prediction"),
        ("L2", "Meta-meta analysis"),
        ("L3", "Self-referential loop")
    ]

    for i, (label, desc) in enumerate(levels):
        y = 7.5 - i * 1.8
        active = i <= godel.meta_level

        if active:
            level_box = FancyBboxPatch((0.5, y - 0.5), 9, 1.2, boxstyle="round,pad=0.05",
                                        facecolor=(0, 1, 1, 0.2), edgecolor=cyan, linewidth=2)
            ax_tower.add_patch(level_box)
            # Add left border
            ax_tower.plot([0.5, 0.5], [y - 0.5, y + 0.7], color=cyan, linewidth=4)

        circle_color = cyan if active else '#333333'
        text_color = '#000000' if active else gray
        circle = Circle((1.5, y + 0.1), 0.5, facecolor=circle_color, edgecolor='none')
        ax_tower.add_patch(circle)
        ax_tower.text(1.5, y + 0.1, label, fontsize=9, color=text_color, ha='center', va='center', fontweight='bold', fontfamily='monospace')
        ax_tower.text(3, y + 0.1, desc, fontsize=10, color=white if active else gray, fontfamily='monospace')

    # === STATISTICS PANEL ===
    ax_stats = fig.add_axes([0.05, 0.04, 0.90, 0.18])
    ax_stats.set_facecolor(dark_bg)
    ax_stats.set_xlim(0, 10)
    ax_stats.set_ylim(0, 3)
    ax_stats.axis('off')

    rect = FancyBboxPatch((0.05, 0.1), 9.9, 2.8, boxstyle="round,pad=0.05",
                          facecolor=dark_bg, edgecolor='#333333', linewidth=2)
    ax_stats.add_patch(rect)

    # Stats boxes
    stats = [
        ("Total Decisions", str(godel.total_decisions), cyan),
        ("Abstentions", str(godel.total_abstentions), magenta),
        ("Paradoxes", str(godel.total_paradoxes), red),
        ("Frame", str(frame_num), green)
    ]

    for i, (label, value, color) in enumerate(stats):
        x = 1.25 + i * 2.5
        stat_box = FancyBboxPatch((x - 0.8, 0.3), 2, 2.3, boxstyle="round,pad=0.05",
                                   facecolor='#111111', edgecolor='#333333', linewidth=1)
        ax_stats.add_patch(stat_box)
        ax_stats.text(x + 0.2, 1.8, value, fontsize=28, color=color, ha='center', fontweight='bold', fontfamily='monospace')
        ax_stats.text(x + 0.2, 0.7, label, fontsize=9, color=gray, ha='center', fontfamily='monospace')

    return fig


def generate_visualization_frames(num_frames: int = 5) -> List[str]:
    """Generate multiple frames of the visualization"""
    output_dir = Path(__file__).parent / "godel_captures"
    output_dir.mkdir(exist_ok=True)

    print("=" * 60)
    print("   GÖDEL MACHINE VISUALIZATION GENERATOR")
    print("=" * 60)

    price_history = [45000 + random.uniform(-1000, 1000) for _ in range(10)]
    total_decisions = 0
    total_abstentions = 0

    saved_files = []

    for i in range(num_frames):
        print(f"\nGenerating frame {i+1}/{num_frames}...")

        market = simulate_market()
        price_history.append(market.price)
        if len(price_history) > 20:
            price_history.pop(0)

        godel = simulate_godel(market, total_decisions, total_abstentions)
        total_decisions = godel.total_decisions
        total_abstentions = godel.total_abstentions

        fig = draw_godel_visualization(market, godel, i + 1, price_history)

        filepath = output_dir / f"godel_frame_{i+1:02d}.png"
        fig.savefig(filepath, dpi=120, facecolor='#0a0a0f', edgecolor='none',
                    bbox_inches='tight', pad_inches=0.2)
        plt.close(fig)

        saved_files.append(str(filepath))
        print(f"  ✓ Saved: {filepath}")
        print(f"    Decision: {godel.decision} | Confidence: {godel.confidence:.0f}%")
        if godel.incompleteness:
            print(f"    Incompleteness: {godel.incompleteness}")
        if godel.strange_loop_active:
            print(f"    Strange Loop: ACTIVE ∞")

    print("\n" + "=" * 60)
    print(f"Generated {num_frames} frames in {output_dir}")
    print("=" * 60)

    return saved_files


if __name__ == "__main__":
    files = generate_visualization_frames(5)
    print(f"\nLatest frame: {files[-1]}")
