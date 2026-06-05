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
                    class="w-full h-28 bg-[#0d1321] text-slate-200 border-2 border-slate-800 rounded-xl p-4 text-base md:text-lg
