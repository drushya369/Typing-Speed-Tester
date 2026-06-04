from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# Pool of different text challenges to load again and again
CHALLENGES = [
    "The beautiful western ghats of Karnataka are filled with dense green forests and waterfalls.",
    "Writing a clean compiler or operating system requires an expert understanding of data structures.",
    "Quantum computing utilizes the principles of superposition and entanglement to process data streams.",
    "The quick brown fox jumps over the lazy dog loops continuously in typewriter testing blocks."
]

# Upgraded Premium Dark UI Template String using Tailwind CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Speed Typing Monitor Pro</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
        body { font-family: 'Plus Jakarta Sans', sans-serif; }
        .mono-font { font-family: 'JetBrains Mono', monospace; }
    </style>
</head>
<body class="bg-[#0b0f19] text-slate-200 min-h-screen flex items-center justify-center p-4 antialiased selection:bg-purple-500/30">

    <div class="w-full max-w-2xl bg-[#161f32] border border-slate-800/80 rounded-2xl p-6 md:p-8 shadow-2xl shadow-purple-950/10 backdrop-blur-md transition-all duration-300">
        
        <header class="text-center mb-8">
            <div class="inline-flex items-center gap-2 bg-purple-500/10 text-purple-400 px-3 py-1 rounded-full text-xs font-semibold tracking-wider uppercase mb-3 border border-purple-500/20">
                ⚡ Metrics Diagnostic Engine
            </div>
            <h1 class="text-2xl md:text-3xl font-bold tracking-tight text-white bg-gradient-to-r from-purple-400 via-indigo-300 to-blue-400 bg-clip-text text-transparent">
                Blind Typing Speed Monitor
            </h1>
            <p class="text-sm text-slate-400 mt-2">
                Evaluate your lexical mapping capabilities and keystroke accuracies instantly.
            </p>
        </header>
        
        <main class="space-y-6">
            <div class="relative bg-[#0d1321] border border-slate-800 rounded-xl p-5 shadow-inner">
                <span class="absolute -top-2 left-4 px-2 py-0.5 text-[10px] font-bold text-slate-500 bg-[#161f32] rounded uppercase tracking-widest border border-slate-800">
                    Active Challenge
                </span>
                <p id="targetText" class="text-base md:text-lg text-slate-300 font-medium leading-relaxed tracking-wide selection:bg-indigo-500/40">
                    {{ target_text }}
                </p>
            </div>
            
            <div class="relative group">
                <textarea id="typeArea" 
                    class="w-full h-28 bg-[#0d1321] text-slate-200 border-2 border-slate-800 rounded-xl p-4 text-base md:text-lg resize-none placeholder-slate-600 transition-all duration-300 focus:outline-none focus:border-purple-500/80 focus:ring-4 focus:ring-purple-500/10 disabled:opacity-50 disabled:cursor-not-allowed shadow-inner"
                    placeholder="Click inside this workspace module and start typing to trigger the telemetry timer..."></textarea>
                <div id="statusIndicator" class="absolute bottom-3 right-4 text-xs font-semibold text-purple-500/60 flex items-center gap-1.5 pointer-events-none">
                    <span class="h-2 w-2 rounded-full bg-purple-500 animate-pulse"></span> Ready
                </div>
            </div>
            
            <section class="grid grid-cols-2 gap-4 pt-2">
                <div class="bg-[#1c263c] border border-slate-800 p-4 rounded-xl text-center shadow-md transition-all duration-300 hover:border-slate-700/60">
                    <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">Gross Velocity</span>
                    <div class="mono-font text-3xl font-bold mt-1 text-purple-400 flex items-baseline justify-center gap-1">
                        <span id="wpmValue">0.0</span>
                        <span class="text-xs text-slate-500 font-sans tracking-normal">WPM</span>
                    </div>
                </div>
                <div class="bg-[#1c263c] border border-slate-800 p-4 rounded-xl text-center shadow-md transition-all duration-300 hover:border-slate-700/60">
                    <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">Accuracy Ratio</span>
                    <div class="mono-font text-3xl font-bold mt-1 text-emerald-400 flex items-baseline justify-center gap-0.5">
                        <span id="accuracyValue">0.0</span>
                        <span class="text-xs text-slate-500 font-sans tracking-normal">%</span>
                    </div>
                </div>
            </section>
            
            <div class="text-center pt-2">
                <a href="/" class="inline-flex items-center gap-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold text-sm px-6 py-3 rounded-xl shadow-lg shadow-purple-950/40 hover:from-purple-500 hover:to-indigo-500 active:scale-98 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-purple-500/40">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 1121.253 8H18"></path></svg>
                    Load Next Challenge
                </a>
            </div>
        </main>
    </div>

    <div class="absolute top-0 left-1/4 w-96 h-96 bg-purple-900/10 rounded-full blur-3xl -z-10 pointer-events-none"></div>
    <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-900/10 rounded-full blur-3xl -z-10 pointer-events-none"></div>

    <script>
        const targetText = document.getElementById('targetText').innerText.trim();
        const typeArea = document.getElementById('typeArea');
        const indicator = document.getElementById('statusIndicator');
        
        let startTime = null;
        let timerTriggered = false;

        typeArea.addEventListener('input', () => {
            if (!timerTriggered) {
                startTime = performance.now();
                timerTriggered = true;
                indicator.innerHTML = '<span class="h-2 w-2 rounded-full bg-indigo-400 animate-ping"></span> Live Capturing Telemetry';
                indicator.className = "absolute bottom-3 right-4 text-xs font-semibold text-indigo-400 flex items-center gap-1.5 pointer-events-none";
            }

            const typedText = typeArea.value;

            // Trigger analysis when text length matching threshold is reached
            if (typedText.length >= targetText.length) {
                const endTime = performance.now();
                const totalTimeSeconds = (endTime - startTime) / 1000;
                typeArea.disabled = true;
                
                indicator.innerHTML = '<span class="h-2 w-2 rounded-full bg-emerald-500"></span> Evaluation Compiled';
                indicator.className = "absolute bottom-3 right-4 text-xs font-semibold text-emerald-400 flex items-center gap-1.5 pointer-events-none";
                typeArea.className = "w-full h-28 bg-[#0d1321] text-slate-400 border-2 border-emerald-950 rounded-xl p-4 text-base md:text-lg resize-none disabled:opacity-80 transition-all duration-300 shadow-inner shadow-emerald-950/20";

                // Post analytical arrays using Fetch API pipeline
                fetch('/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        target: targetText,
                        typed: typedText,
                        time_taken: totalTimeSeconds
                    })
                })
                .then(res => res.json())
                .then(data => {
                    // Update frontend components smoothly
                    document.getElementById('wpmValue').innerText = data.wpm;
                    document.getElementById('accuracyValue').innerText = data.accuracy;
                })
                .catch(err => {
                    console.error("Transmission Error:", err);
                    indicator.innerText = "⚠️ Network Diagnostics Failure";
                });
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    target_text = random.choice(CHALLENGES)
    return render_template_string(HTML_TEMPLATE, target_text=target_text)

@app.route('/calculate', methods=['POST'])
def calculate_metrics():
    data = request.json
    target = data.get('target', '').strip()
    typed = data.get('typed', '').strip()
    time_taken = float(data.get('time_taken', 1.0))
    
    # Calculate character exact match alignments
    correct_chars = sum(1 for t, p in zip(target, typed) if t == p)
    total_target_chars = len(target)
    accuracy = round((correct_chars / total_target_chars) * 100, 2) if total_target_chars > 0 else 0
    
    # Calculate WPM based on standard semantic unit scaling
    wpm = round((len(typed) / 5) / (time_taken / 60), 2)
    
    return jsonify({
        "wpm": wpm,
        "accuracy": accuracy
    })

if __name__ == '__main__':
    app.run(debug=True)
