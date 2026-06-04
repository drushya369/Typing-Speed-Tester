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

# Combined HTML Interface Template String
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Speed Typing Monitor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 700px; margin: 50px auto; padding: 20px; background: #fafafa; color: #333; text-align: center; }
        .card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 5px solid #673ab7; }
        .target-box { background: #f3e5f5; padding: 20px; border-radius: 8px; font-size: 18px; font-weight: 500; text-align: left; margin-bottom: 20px; line-height: 1.5; letter-spacing: 0.5px; }
        textarea { width: 100%; height: 90px; padding: 12px; box-sizing: border-box; border: 2px solid #cbd5e0; border-radius: 6px; font-size: 16px; resize: none; }
        textarea:focus { border-color: #673ab7; outline: none; }
        .dashboard-row { display: flex; justify-content: space-around; margin-top: 25px; }
        .metric-box { background: #f8f9fa; border: 1px solid #e2e8f0; padding: 15px 30px; border-radius: 8px; min-width: 120px; }
        .metric-box strong { font-size: 26px; color: #673ab7; display: block; margin-top: 5px; }
        .refresh-btn { background: #673ab7; color: white; border: none; padding: 10px 20px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-top: 15px; text-decoration: none; display: inline-block; }
    </style>
</head>
<body>

    <div class="card">
        <h2>⌨️ Blind Typing Speed Monitor</h2>
        <p style="color:#718096; margin-bottom:25px;">Test your lexical mapping capabilities and keystroke accuracies in real time.</p>
        
        <div class="target-box" id="targetText">{{ target_text }}</div>
        
        <textarea id="typeArea" placeholder="Click here and start typing the sentence above to trigger the timer..."></textarea>
        
        <div class="dashboard-row">
            <div class="metric-box">Speed <strong><span id="wpmValue">0.0</span> <span style="font-size:12px; color:#666;">WPM</span></strong></div>
            <div class="metric-box">Accuracy <strong><span id="accuracyValue">0.0</span><span style="font-size:12px; color:#666;">%</span></strong></div>
        </div>

        <a href="/" class="refresh-btn">🔄 Next Sentence Challenge</a>
    </div>

    <script>
        const targetText = document.getElementById('targetText').innerText;
        const typeArea = document.getElementById('typeArea');
        
        let startTime = null;
        let timerTriggered = false;

        typeArea.addEventListener('input', () => {
            // Initialize time marker on the absolute first keystroke event
            if (!timerTriggered) {
                startTime = performance.now();
                timerTriggered = true;
            }

            const typedText = typeArea.value;

            // Continuous background verification hook when challenge is met
            if (typedText.length >= targetText.length) {
                const endTime = performance.now();
                const totalTimeSeconds = (endTime - startTime) / 1000;
                typeArea.disabled = true;

                // Fire background telemetry payload to the Python server
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
                    document.getElementById('wpmValue').innerText = data.wpm;
                    document.getElementById('accuracyValue').innerText = data.accuracy;
                });
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    # Pick a random challenge string on page load
    target_text = random.choice(CHALLENGES)
    return render_template_string(HTML_TEMPLATE, target_text=target_text)

@app.route('/calculate', methods=['POST'])
def calculate_metrics():
    data = request.json
    target = data.get('target', '')
    typed = data.get('typed', '')
    time_taken = float(data.get('time_taken', 1.0)) # Avoid division by zero
    
    # 1. Calculate Accuracy Percentage
    correct_chars = sum(1 for t, p in zip(target, typed) if t == p)
    total_target_chars = len(target)
    accuracy = round((correct_chars / total_target_chars) * 100, 2) if total_target_chars > 0 else 0
    
    # 2. Calculate WPM (Standard rule: 1 word = 5 characters)
    wpm = round((len(typed) / 5) / (time_taken / 60), 2)
    
    return jsonify({
        "wpm": wpm,
        "accuracy": accuracy
    })

if __name__ == '__main__':
    app.run(debug=True)
  
