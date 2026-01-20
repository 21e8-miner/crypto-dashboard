"""
GÖDEL MACHINE FRONTEND: Visualizing Self-Reference

A web interface to observe the Gödel Machine in action.
Watch as it thinks about thinking, predicts its predictions,
and encounters the limits of self-knowledge.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template_string, jsonify, Response
import json
import time
import random
from datetime import datetime
from threading import Thread, Lock
import queue

# Import Gödel components
from godel_numbers import GodelEncoder, GodelStrategyFactory, StrategyPrimitive
from introspection_engine import IntrospectionEngine, CognitiveState
from meta_predictor import MetaPredictor, StrangeLoopGenerator
from incompleteness_detector import IncompletenessDetector, MarketState, IncompletenessType
from recursive_self_improvement import RecursiveSelfImprover, ImprovementOutcome
from godel_machine import GodelMachine, GodelMachineState

app = Flask(__name__)

# Global state
machine = None
event_queue = queue.Queue()
state_lock = Lock()
running = False

# HTML Template with full visualization
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Gödel Machine</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #0a0a0f;
            color: #e0e0e0;
            font-family: 'Courier New', monospace;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            text-align: center;
            padding: 30px 0;
            border-bottom: 1px solid #333;
            margin-bottom: 30px;
        }

        h1 {
            font-size: 2.5em;
            background: linear-gradient(135deg, #00ff88, #00aaff, #ff00aa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #888;
            font-style: italic;
        }

        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }

        .panel {
            background: #12121a;
            border: 1px solid #2a2a3a;
            border-radius: 10px;
            padding: 20px;
            position: relative;
            overflow: hidden;
        }

        .panel::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #00ff88, #00aaff);
        }

        .panel.warning::before {
            background: linear-gradient(90deg, #ffaa00, #ff5500);
        }

        .panel.paradox::before {
            background: linear-gradient(90deg, #ff0055, #ff00aa);
            animation: pulse 1s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .panel-title {
            font-size: 1.2em;
            color: #00ff88;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .panel-title .icon {
            font-size: 1.5em;
        }

        .full-width {
            grid-column: 1 / -1;
        }

        .stat-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
        }

        .stat-box {
            background: #1a1a2a;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #00aaff;
        }

        .stat-label {
            font-size: 0.8em;
            color: #888;
            margin-top: 5px;
        }

        .decision-display {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 30px;
            padding: 20px;
        }

        .action-badge {
            font-size: 3em;
            font-weight: bold;
            padding: 20px 40px;
            border-radius: 10px;
            text-transform: uppercase;
        }

        .action-badge.buy {
            background: linear-gradient(135deg, #00ff88, #00aa55);
            color: #000;
        }

        .action-badge.sell {
            background: linear-gradient(135deg, #ff5555, #aa0000);
            color: #fff;
        }

        .action-badge.hold {
            background: linear-gradient(135deg, #ffaa00, #aa7700);
            color: #000;
        }

        .action-badge.abstain {
            background: linear-gradient(135deg, #8855ff, #5500aa);
            color: #fff;
            animation: glow 2s infinite;
        }

        @keyframes glow {
            0%, 100% { box-shadow: 0 0 20px rgba(136, 85, 255, 0.5); }
            50% { box-shadow: 0 0 40px rgba(136, 85, 255, 0.8); }
        }

        .confidence-bar {
            width: 100%;
            height: 30px;
            background: #1a1a2a;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }

        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #00ff88, #00aaff);
            transition: width 0.5s ease;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            font-weight: bold;
            color: #000;
        }

        .meta-tower {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .meta-level {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 12px;
            background: #1a1a2a;
            border-radius: 5px;
            font-size: 0.9em;
        }

        .meta-level.active {
            border-left: 3px solid #00ff88;
        }

        .meta-level .level-num {
            color: #00aaff;
            font-weight: bold;
            min-width: 30px;
        }

        .strange-loop {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .loop-visual {
            width: 150px;
            height: 150px;
            border: 3px solid #ff00aa;
            border-radius: 50%;
            position: relative;
            animation: rotate 4s linear infinite;
        }

        .loop-visual.inactive {
            border-color: #333;
            animation: none;
        }

        .loop-visual::before {
            content: '∞';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 4em;
            color: #ff00aa;
        }

        .loop-visual.inactive::before {
            color: #333;
        }

        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }

        .incompleteness-indicator {
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }

        .incompleteness-indicator.detected {
            background: rgba(255, 85, 0, 0.2);
            border: 1px solid #ff5500;
        }

        .incompleteness-indicator.clear {
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid #00ff88;
        }

        .godel-number {
            font-family: 'Courier New', monospace;
            font-size: 1.5em;
            color: #00aaff;
            background: #1a1a2a;
            padding: 10px 20px;
            border-radius: 5px;
            display: inline-block;
            margin: 10px 0;
        }

        .thought-stream {
            max-height: 300px;
            overflow-y: auto;
            background: #0a0a0f;
            border-radius: 5px;
            padding: 10px;
        }

        .thought {
            padding: 8px;
            border-bottom: 1px solid #222;
            font-size: 0.85em;
        }

        .thought:last-child {
            border-bottom: none;
        }

        .thought-time {
            color: #666;
        }

        .thought-type {
            color: #00aaff;
            font-weight: bold;
        }

        .philosophy-box {
            background: linear-gradient(135deg, #1a1a2a, #2a1a3a);
            padding: 20px;
            border-radius: 8px;
            font-style: italic;
            color: #aaa;
            line-height: 1.6;
        }

        .philosophy-box::before {
            content: '"';
            font-size: 3em;
            color: #ff00aa;
            float: left;
            margin-right: 10px;
            line-height: 0.8;
        }

        .controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin: 20px 0;
        }

        button {
            padding: 15px 30px;
            font-size: 1.1em;
            font-family: 'Courier New', monospace;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }

        button.primary {
            background: linear-gradient(135deg, #00ff88, #00aa55);
            color: #000;
        }

        button.secondary {
            background: #2a2a3a;
            color: #fff;
            border: 1px solid #444;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 255, 136, 0.3);
        }

        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        .price-display {
            font-size: 2.5em;
            font-weight: bold;
            color: #fff;
        }

        .price-change {
            font-size: 1.2em;
            margin-left: 10px;
        }

        .price-change.up { color: #00ff88; }
        .price-change.down { color: #ff5555; }

        .cognitive-state {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }

        .cognitive-state.MONITORING { background: #00aaff; color: #000; }
        .cognitive-state.ANALYZING { background: #00ff88; color: #000; }
        .cognitive-state.META_ANALYZING { background: #ffaa00; color: #000; }
        .cognitive-state.PARADOX { background: #ff0055; color: #fff; animation: pulse 0.5s infinite; }
        .cognitive-state.BOUNDED { background: #8855ff; color: #fff; }

        footer {
            text-align: center;
            padding: 30px;
            color: #555;
            border-top: 1px solid #222;
            margin-top: 30px;
        }

        .manifesto {
            max-width: 800px;
            margin: 0 auto;
            text-align: left;
            white-space: pre-line;
            font-size: 0.85em;
            line-height: 1.8;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⟨ THE GÖDEL MACHINE ⟩</h1>
            <p class="subtitle">"I am the strange loop that trades itself."</p>
        </header>

        <div class="controls">
            <button class="primary" id="startBtn" onclick="startMachine()">▶ START MACHINE</button>
            <button class="secondary" id="stopBtn" onclick="stopMachine()" disabled>◼ STOP</button>
            <button class="secondary" onclick="createGodelTrade()">∞ GÖDEL SENTENCE TRADE</button>
        </div>

        <div class="grid">
            <!-- Current Decision -->
            <div class="panel full-width" id="decisionPanel">
                <div class="panel-title"><span class="icon">🎯</span> CURRENT DECISION</div>
                <div class="decision-display">
                    <div>
                        <div class="price-display">
                            $<span id="currentPrice">45,000</span>
                            <span class="price-change" id="priceChange"></span>
                        </div>
                        <div style="margin-top: 10px; color: #888;">Market Price</div>
                    </div>
                    <div class="action-badge hold" id="actionBadge">HOLD</div>
                    <div style="text-align: center;">
                        <div style="color: #888; margin-bottom: 5px;">Gödel Number</div>
                        <div class="godel-number" id="godelNumber">---</div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                    <div>
                        <div style="color: #888; margin-bottom: 5px;">Confidence</div>
                        <div class="confidence-bar">
                            <div class="confidence-fill" id="confidenceBar" style="width: 50%;">50%</div>
                        </div>
                    </div>
                    <div>
                        <div style="color: #888; margin-bottom: 5px;">Meta-Confidence (confidence about confidence)</div>
                        <div class="confidence-bar">
                            <div class="confidence-fill" id="metaConfidenceBar" style="width: 50%; background: linear-gradient(90deg, #ff00aa, #aa00ff);">50%</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Statistics -->
            <div class="panel full-width">
                <div class="panel-title"><span class="icon">📊</span> MACHINE STATISTICS</div>
                <div class="stat-grid">
                    <div class="stat-box">
                        <div class="stat-value" id="totalDecisions">0</div>
                        <div class="stat-label">Total Decisions</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" id="abstentions">0</div>
                        <div class="stat-label">Abstentions</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" id="paradoxes">0</div>
                        <div class="stat-label">Paradoxes</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" id="improvements">0</div>
                        <div class="stat-label">Self-Improvements</div>
                    </div>
                </div>
            </div>

            <!-- Meta-Prediction Tower -->
            <div class="panel">
                <div class="panel-title"><span class="icon">🗼</span> META-PREDICTION TOWER</div>
                <div class="meta-tower" id="metaTower">
                    <div class="meta-level"><span class="level-num">L0</span> Base prediction awaiting...</div>
                </div>
            </div>

            <!-- Strange Loop Detector -->
            <div class="panel" id="loopPanel">
                <div class="panel-title"><span class="icon">🔄</span> STRANGE LOOP DETECTOR</div>
                <div class="strange-loop">
                    <div class="loop-visual inactive" id="loopVisual"></div>
                </div>
                <div style="text-align: center; color: #888;" id="loopStatus">
                    No strange loops detected
                </div>
            </div>

            <!-- Incompleteness Detection -->
            <div class="panel" id="incompletenessPanel">
                <div class="panel-title"><span class="icon">❓</span> INCOMPLETENESS DETECTION</div>
                <div class="incompleteness-indicator clear" id="incompletenessIndicator">
                    <strong>Status:</strong> <span id="incompletenessStatus">Market state appears complete</span>
                </div>
                <div style="margin-top: 15px;">
                    <strong>Cognitive State:</strong>
                    <span class="cognitive-state MONITORING" id="cognitiveState">MONITORING</span>
                </div>
            </div>

            <!-- Introspection -->
            <div class="panel">
                <div class="panel-title"><span class="icon">🪞</span> INTROSPECTION ENGINE</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <div class="stat-box">
                        <div class="stat-value" id="metaDepth">0</div>
                        <div class="stat-label">Meta-Depth Reached</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" id="thoughtCount">0</div>
                        <div class="stat-label">Thoughts Recorded</div>
                    </div>
                </div>
                <div style="margin-top: 15px;">
                    <div style="color: #888; margin-bottom: 5px;">Recent Thoughts</div>
                    <div class="thought-stream" id="thoughtStream">
                        <div class="thought">Awaiting initialization...</div>
                    </div>
                </div>
            </div>

            <!-- Philosophy Box -->
            <div class="panel full-width">
                <div class="panel-title"><span class="icon">💭</span> PHILOSOPHICAL NOTE</div>
                <div class="philosophy-box" id="philosophyBox">
                    A system powerful enough to reason about itself will encounter statements about itself that it cannot decide. This is not a bug — it's fundamental mathematics.
                </div>
            </div>

            <!-- Reasoning -->
            <div class="panel full-width">
                <div class="panel-title"><span class="icon">🧠</span> REASONING</div>
                <div id="reasoning" style="line-height: 1.6; color: #aaa;">
                    Initializing the Gödel Machine...
                </div>
            </div>
        </div>

        <footer>
            <div class="manifesto">
WE DO NOT SEEK OMNISCIENCE.
WE SEEK WISDOM ABOUT THE LIMITS OF KNOWLEDGE.

"I know that I know nothing." — Socrates
"This statement cannot be proven within this system." — Gödel
"I am the strange loop that trades itself." — The Gödel Machine
            </div>
        </footer>
    </div>

    <script>
        let eventSource = null;
        let isRunning = false;

        function startMachine() {
            if (isRunning) return;

            fetch('/start', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'started') {
                        isRunning = true;
                        document.getElementById('startBtn').disabled = true;
                        document.getElementById('stopBtn').disabled = false;
                        startEventStream();
                    }
                });
        }

        function stopMachine() {
            fetch('/stop', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    isRunning = false;
                    document.getElementById('startBtn').disabled = false;
                    document.getElementById('stopBtn').disabled = true;
                    if (eventSource) {
                        eventSource.close();
                    }
                });
        }

        function createGodelTrade() {
            fetch('/godel-sentence', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    updateDisplay(data);
                    document.getElementById('decisionPanel').classList.add('paradox');
                    setTimeout(() => {
                        document.getElementById('decisionPanel').classList.remove('paradox');
                    }, 5000);
                });
        }

        function startEventStream() {
            eventSource = new EventSource('/stream');

            eventSource.onmessage = function(event) {
                const data = JSON.parse(event.data);
                updateDisplay(data);
            };

            eventSource.onerror = function() {
                console.log('Event stream error');
            };
        }

        function updateDisplay(data) {
            // Update price
            if (data.price) {
                document.getElementById('currentPrice').textContent =
                    data.price.toLocaleString(undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0});

                const change = data.price_change || 0;
                const changeEl = document.getElementById('priceChange');
                changeEl.textContent = (change >= 0 ? '+' : '') + (change * 100).toFixed(2) + '%';
                changeEl.className = 'price-change ' + (change >= 0 ? 'up' : 'down');
            }

            // Update action
            if (data.action) {
                const badge = document.getElementById('actionBadge');
                badge.textContent = data.action.toUpperCase();
                badge.className = 'action-badge ' + data.action.toLowerCase();
            }

            // Update confidence
            if (data.confidence !== undefined) {
                const pct = Math.round(data.confidence * 100);
                document.getElementById('confidenceBar').style.width = pct + '%';
                document.getElementById('confidenceBar').textContent = pct + '%';
            }

            // Update meta-confidence
            if (data.meta_confidence !== undefined) {
                const pct = Math.round(data.meta_confidence * 100);
                document.getElementById('metaConfidenceBar').style.width = pct + '%';
                document.getElementById('metaConfidenceBar').textContent = pct + '%';
            }

            // Update Gödel number
            if (data.godel_number) {
                document.getElementById('godelNumber').textContent = data.godel_number;
            }

            // Update statistics
            if (data.stats) {
                document.getElementById('totalDecisions').textContent = data.stats.total_decisions || 0;
                document.getElementById('abstentions').textContent = data.stats.abstentions || 0;
                document.getElementById('paradoxes').textContent = data.stats.paradoxes || 0;
                document.getElementById('improvements').textContent = data.stats.improvements || 0;
            }

            // Update meta tower
            if (data.meta_tower) {
                const tower = document.getElementById('metaTower');
                tower.innerHTML = data.meta_tower.map((level, i) =>
                    `<div class="meta-level ${level.active ? 'active' : ''}">
                        <span class="level-num">L${i}</span> ${level.description}
                    </div>`
                ).join('');
            }

            // Update strange loop
            if (data.strange_loop !== undefined) {
                const visual = document.getElementById('loopVisual');
                const status = document.getElementById('loopStatus');
                const panel = document.getElementById('loopPanel');

                if (data.strange_loop) {
                    visual.classList.remove('inactive');
                    status.innerHTML = '<span style="color: #ff00aa;">⚠️ STRANGE LOOP ACTIVE</span><br>The prediction predicts itself';
                    panel.classList.add('warning');
                } else {
                    visual.classList.add('inactive');
                    status.textContent = 'No strange loops detected';
                    panel.classList.remove('warning');
                }
            }

            // Update incompleteness
            if (data.incompleteness !== undefined) {
                const indicator = document.getElementById('incompletenessIndicator');
                const status = document.getElementById('incompletenessStatus');
                const panel = document.getElementById('incompletenessPanel');

                if (data.incompleteness.detected) {
                    indicator.className = 'incompleteness-indicator detected';
                    status.innerHTML = `<span style="color: #ff5500;">${data.incompleteness.type || 'UNKNOWN'}</span>`;
                    panel.classList.add('warning');
                } else {
                    indicator.className = 'incompleteness-indicator clear';
                    status.textContent = 'Market state appears decidable';
                    panel.classList.remove('warning');
                }
            }

            // Update cognitive state
            if (data.cognitive_state) {
                const el = document.getElementById('cognitiveState');
                el.textContent = data.cognitive_state;
                el.className = 'cognitive-state ' + data.cognitive_state;
            }

            // Update introspection
            if (data.introspection) {
                document.getElementById('metaDepth').textContent = data.introspection.meta_depth || 0;
                document.getElementById('thoughtCount').textContent = data.introspection.thought_count || 0;
            }

            // Update thoughts
            if (data.thoughts && data.thoughts.length > 0) {
                const stream = document.getElementById('thoughtStream');
                stream.innerHTML = data.thoughts.slice(-10).map(t =>
                    `<div class="thought">
                        <span class="thought-time">${t.time}</span>
                        <span class="thought-type">[${t.type}]</span>
                        ${t.content}
                    </div>`
                ).reverse().join('');
            }

            // Update philosophy
            if (data.philosophy) {
                document.getElementById('philosophyBox').textContent = data.philosophy;
            }

            // Update reasoning
            if (data.reasoning) {
                document.getElementById('reasoning').textContent = data.reasoning;
            }
        }

        // Initial state fetch
        fetch('/state')
            .then(response => response.json())
            .then(data => updateDisplay(data));
    </script>
</body>
</html>
'''


def create_machine():
    """Create a fresh Gödel Machine instance"""
    global machine
    machine = GodelMachine(
        name="GodelMachine_Visual",
        enable_self_improvement=True,
        max_meta_depth=3,
        incompleteness_sensitivity=0.7
    )
    return machine


def generate_market_data(prev_price=45000):
    """Generate synthetic market data"""
    price_change = random.gauss(0, 0.02)
    new_price = prev_price * (1 + price_change)

    return {
        "price": new_price,
        "prev_price": prev_price,
        "price_change": price_change,
        "volume": random.uniform(500000, 2000000),
        "rsi": random.uniform(20, 80),
        "macd": random.gauss(0, 0.5),
        "momentum": price_change * 10,
        "trend": random.uniform(-1, 1),
        "sentiment": random.uniform(0.2, 0.8) if random.random() > 0.3 else None,
        "volatility": random.uniform(0.1, 0.5) if random.random() > 0.2 else None
    }


def format_decision_for_frontend(decision, market_data, machine_state):
    """Format a decision for the frontend"""
    thoughts = []
    for t in list(machine.introspection.thought_history)[-10:]:
        thoughts.append({
            "time": t.timestamp.strftime("%H:%M:%S"),
            "type": t.thought_type,
            "content": f"conf={t.confidence:.2f}, meta_level={t.meta_level}"
        })

    # Build meta tower
    meta_tower = []
    for i in range(4):
        if i == 0:
            meta_tower.append({
                "active": True,
                "description": f"Base: {decision.action.upper()} ({decision.confidence:.0%})"
            })
        elif i <= machine.introspection.get_self_model().meta_depth_reached:
            meta_tower.append({
                "active": True,
                "description": f"Meta-{i}: Analyzing level {i-1}"
            })
        else:
            meta_tower.append({
                "active": False,
                "description": f"Level {i} not reached"
            })

    return {
        "price": market_data["price"],
        "price_change": market_data.get("price_change", 0),
        "action": decision.action,
        "confidence": decision.confidence,
        "meta_confidence": decision.meta_confidence,
        "godel_number": str(decision.godel_number) if decision.godel_number else "---",
        "stats": {
            "total_decisions": machine.total_decisions,
            "abstentions": machine.abstentions,
            "paradoxes": machine.paradoxes_encountered,
            "improvements": machine.self_improvements
        },
        "meta_tower": meta_tower,
        "strange_loop": decision.strange_loop_active,
        "incompleteness": {
            "detected": decision.incompleteness_detected,
            "type": decision.incompleteness_type.name if decision.incompleteness_type else None
        },
        "cognitive_state": machine.introspection.get_self_model().cognitive_state.name,
        "introspection": {
            "meta_depth": machine.introspection.get_self_model().meta_depth_reached,
            "thought_count": len(machine.introspection.thought_history)
        },
        "thoughts": thoughts,
        "philosophy": decision.philosophical_note,
        "reasoning": decision.reasoning
    }


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/state')
def get_state():
    if machine is None:
        create_machine()

    return jsonify({
        "action": "hold",
        "confidence": 0.5,
        "meta_confidence": 0.5,
        "godel_number": "---",
        "stats": {
            "total_decisions": 0,
            "abstentions": 0,
            "paradoxes": 0,
            "improvements": 0
        },
        "strange_loop": False,
        "incompleteness": {"detected": False, "type": None},
        "cognitive_state": "MONITORING",
        "philosophy": "A system powerful enough to reason about itself will encounter statements about itself that it cannot decide. This is not a bug — it's fundamental mathematics."
    })


@app.route('/start', methods=['POST'])
def start():
    global running
    if machine is None:
        create_machine()
    running = True
    return jsonify({"status": "started"})


@app.route('/stop', methods=['POST'])
def stop():
    global running
    running = False
    return jsonify({"status": "stopped"})


@app.route('/godel-sentence', methods=['POST'])
def godel_sentence():
    if machine is None:
        create_machine()

    decision = machine.create_godel_sentence_trade()

    return jsonify({
        "price": 45000,
        "price_change": 0,
        "action": decision.action,
        "confidence": decision.confidence,
        "meta_confidence": decision.meta_confidence,
        "godel_number": str(decision.godel_number) if decision.godel_number else "∞",
        "stats": {
            "total_decisions": machine.total_decisions,
            "abstentions": machine.abstentions,
            "paradoxes": machine.paradoxes_encountered,
            "improvements": machine.self_improvements
        },
        "strange_loop": True,
        "incompleteness": {
            "detected": True,
            "type": "SELF_REFERENCE_PARADOX"
        },
        "cognitive_state": "PARADOX",
        "philosophy": decision.philosophical_note,
        "reasoning": decision.reasoning
    })


@app.route('/stream')
def stream():
    def generate():
        global running
        price = 45000

        while True:
            if not running:
                time.sleep(0.5)
                continue

            # Generate market data
            market_data = generate_market_data(price)
            price = market_data["price"]

            # Process through Gödel Machine
            decision = machine.process_market_state(market_data)

            # Format for frontend
            state = machine.get_machine_state()
            data = format_decision_for_frontend(decision, market_data, state)

            yield f"data: {json.dumps(data)}\n\n"

            time.sleep(2)  # Update every 2 seconds

    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    print("=" * 60)
    print("THE GÖDEL MACHINE: Visual Frontend")
    print("=" * 60)
    print()
    print("Starting server at http://localhost:8080")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)

    create_machine()
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
