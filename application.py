from flask import Flask, render_template_string, jsonify
from datetime import datetime
import os
import random

# Specify your actual GitHub repository URL here
GITHUB_REPO_URL = "https://github.com/your-username/your-repo-name" 

application = Flask(__name__)

# HTML template styled with Tailwind CSS (Solar-Grid / Clean Tech Theme)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project: HELIOS | AWS Elastic Beanstalk</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=JetBrains+Mono:wght@400;600&display=swap');
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        .mono {
            font-family: 'JetBrains Mono', monospace;
        }
    </style>
    <script>
        // Update dashboard metrics dynamically via API call
        async function fetchMetrics() {
            try {
                const response = await fetch('/api/metrics');
                const data = await response.json();
                
                document.getElementById('solar-output').textContent = data.solar_output_kw + ' kW';
                document.getElementById('grid-efficiency').textContent = data.efficiency_percentage + '%';
                document.getElementById('active-nodes').textContent = data.active_nodes;
                document.getElementById('last-sync').textContent = data.timestamp_utc;
            } catch (err) {
                console.error("Metric sync failed", err);
            }
        }
        
        // Refresh every 3 seconds
        setInterval(fetchMetrics, 3000);
    </script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-between">

    <!-- Glowing Background Gradients -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
        <div class="absolute -top-40 -left-40 w-96 h-96 bg-amber-500/10 rounded-full blur-3xl"></div>
        <div class="absolute top-1/2 right-0 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl"></div>
    </div>

    <!-- Navigation Header -->
    <header class="relative z-10 border-b border-slate-800/80 bg-slate-900/50 backdrop-blur-md px-6 py-4">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <div class="h-3 w-3 rounded-full bg-amber-400 animate-pulse"></div>
                <span class="font-bold tracking-wider text-sm text-slate-200">HELIOS // GRID MONITOR v2.4</span>
            </div>
            <div class="flex items-center space-x-4 text-xs font-mono">
                <span class="px-2.5 py-1 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800">
                    REGION: {{ aws_region }}
                </span>
                <span class="px-2.5 py-1 rounded-full bg-slate-800 text-slate-400 border border-slate-700">
                    ENV: {{ env_name }}
                </span>
            </div>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="relative z-10 max-w-7xl mx-auto w-full px-6 py-10 flex-grow flex flex-col justify-center">
        
        <!-- Welcome Hero Section -->
        <div class="mb-10 text-center md:text-left">
            <h1 class="text-3xl md:text-5xl font-extrabold tracking-tight text-white mb-2">
                Node Deployment <span class="text-amber-400">Online</span>
            </h1>
            <p class="text-slate-400 text-base max-w-2xl">
                AWS Elastic Beanstalk cluster operational. Real-time telemetry connection established over Gunicorn execution engine.
            </p>
        </div>

        <!-- Telemetry Stats Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            
            <!-- Card 1 -->
            <div class="bg-slate-900/80 border border-slate-800 rounded-xl p-6 shadow-xl backdrop-blur-sm">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Current Generation</p>
                <div class="flex items-baseline space-x-2">
                    <span id="solar-output" class="text-3xl font-extrabold text-amber-400 mono">482.5 kW</span>
                </div>
                <p class="text-xs text-slate-500 mt-2">Simulated live feed from solar array</p>
            </div>

            <!-- Card 2 -->
            <div class="bg-slate-900/80 border border-slate-800 rounded-xl p-6 shadow-xl backdrop-blur-sm">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Efficiency Rating</p>
                <div class="flex items-baseline space-x-2">
                    <span id="grid-efficiency" class="text-3xl font-extrabold text-emerald-400 mono">98.4%</span>
                </div>
                <p class="text-xs text-slate-500 mt-2">Optimal conversion metrics</p>
            </div>

            <!-- Card 3 -->
            <div class="bg-slate-900/80 border border-slate-800 rounded-xl p-6 shadow-xl backdrop-blur-sm">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Active Cluster Nodes</p>
                <div class="flex items-baseline space-x-2">
                    <span id="active-nodes" class="text-3xl font-extrabold text-sky-400 mono">12 / 12</span>
                </div>
                <p class="text-xs text-slate-500 mt-2">Auto-scaled instances running</p>
            </div>

        </div>

        <!-- System Details & Quick Actions -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- Terminal Log Window -->
            <div class="lg:col-span-2 bg-slate-900/90 border border-slate-800 rounded-xl p-6 font-mono text-xs text-slate-300">
                <div class="flex justify-between items-center pb-3 mb-3 border-b border-slate-800 text-slate-500">
                    <span>SYSTEM_LOGS</span>
                    <span id="last-sync" class="text-slate-400">{{ current_time }}</span>
                </div>
                <div class="space-y-1.5 text-slate-400">
                    <p class="text-emerald-400">[SYS_OK] Flask 3.x WSGI application initial handshake complete.</p>
                    <p>[INFO] AWS Elastic Beanstalk reverse proxy configured via Nginx/Gunicorn.</p>
                    <p>[INFO] Health check ping standard active at /health.</p>
                    <p class="text-amber-400">[LIVE] Periodic telemetry task running on 3000ms loop.</p>
                </div>
            </div>

            <!-- Quick Action Links -->
            <div class="bg-slate-900/80 border border-slate-800 rounded-xl p-6 flex flex-col justify-center space-y-4">
                <a href="/health" class="w-full text-center py-3 px-4 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-sm transition shadow-lg shadow-amber-500/10">
                    Endpoint Health Check
                </a>
                <a href="{{ github_url }}" target="_blank" class="w-full text-center py-3 px-4 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-sm border border-slate-700 transition flex items-center justify-center space-x-2">
                    <span>GitHub Repository</span>
                </a>
            </div>

        </div>

    </main>

    <!-- Footer -->
    <footer class="relative z-10 py-4 border-t border-slate-900 text-center text-xs text-slate-500">
        Project Helios Operations Platform &bull; AWS Elastic Beanstalk Deployment
    </footer>

</body>
</html>
"""

@application.route('/')
def home():
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    env_name = os.environ.get('AWS_EB_ENVIRONMENT_NAME', 'LOCAL_DEV')
    aws_region = os.environ.get('AWS_REGION', 'us-west-2')
    
    return render_template_string(
        HTML_TEMPLATE, 
        current_time=now,
        github_url=GITHUB_REPO_URL,
        env_name=env_name,
        aws_region=aws_region
    )

@application.route('/api/metrics')
def metrics():
    # Return simulated dynamic data for JS polling
    return jsonify({
        "solar_output_kw": round(random.uniform(450.0, 520.0), 1),
        "efficiency_percentage": round(random.uniform(96.5, 99.2), 1),
        "active_nodes": random.randint(10, 12),
        "timestamp_utc": datetime.utcnow().strftime('%H:%M:%S UTC')
    }), 200

@application.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "service_name": "helios-grid-monitor",
        "timestamp_utc": datetime.utcnow().isoformat()
    }), 200

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
