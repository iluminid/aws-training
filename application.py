from flask import Flask, jsonify, render_template_string
from datetime import datetime
import math
import os
import random
import threading
import time

application = Flask(__name__)
app = application

_lock = threading.Lock()
_started_at = time.time()
_last_update = time.time()
_energy_kwh = 1842.620
_peak_power_kw = 0.0


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def generate_dummy_power_data():
    global _last_update, _energy_kwh, _peak_power_kw

    with _lock:
        now = time.time()
        elapsed = max(0.001, now - _last_update)
        _last_update = now

        # Realistic-looking industrial load that changes every request.
        total_kw = (
            52.0
            + math.sin(now / 23.0) * 5.0
            + math.sin(now / 7.0) * 2.0
            + random.uniform(-1.3, 1.3)
        )
        total_kw = clamp(total_kw, 38.0, 68.0)

        voltages = [
            231.0 + math.sin(now / 8.0) * 1.8 + random.uniform(-0.8, 0.8),
            230.5 + math.sin(now / 8.5 + 1.5) * 1.6 + random.uniform(-0.8, 0.8),
            231.7 + math.sin(now / 9.0 + 3.0) * 1.7 + random.uniform(-0.8, 0.8),
        ]

        power_factor = clamp(
            0.94 + math.sin(now / 14.0) * 0.018 + random.uniform(-0.008, 0.008),
            0.89,
            0.99,
        )

        shares = [
            0.333 + random.uniform(-0.012, 0.012),
            0.333 + random.uniform(-0.012, 0.012),
            0.334 + random.uniform(-0.012, 0.012),
        ]
        share_total = sum(shares)
        shares = [s / share_total for s in shares]
        phase_power = [total_kw * s for s in shares]

        currents = [
            phase_power[i] * 1000.0 / (voltages[i] * power_factor)
            for i in range(3)
        ]

        frequency = 50.0 + math.sin(now / 11.0) * 0.035 + random.uniform(-0.015, 0.015)
        apparent_kva = total_kw / max(power_factor, 0.01)
        reactive_kvar = math.sqrt(max(0.0, apparent_kva ** 2 - total_kw ** 2))

        _energy_kwh += total_kw * elapsed / 3600.0
        _peak_power_kw = max(_peak_power_kw, total_kw)

        avg_voltage = sum(voltages) / 3.0
        avg_current = sum(currents) / 3.0
        imbalance = (max(currents) - min(currents)) / max(avg_current, 0.01) * 100.0

        if total_kw > 65:
            status = "HIGH LOAD"
            status_level = "warning"
        elif power_factor < 0.91:
            status = "LOW POWER FACTOR"
            status_level = "warning"
        elif avg_voltage < 218 or avg_voltage > 242:
            status = "VOLTAGE ALERT"
            status_level = "danger"
        else:
            status = "NORMAL"
            status_level = "normal"

        return {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "status": status,
            "status_level": status_level,
            "total_power_kw": round(total_kw, 2),
            "apparent_power_kva": round(apparent_kva, 2),
            "reactive_power_kvar": round(reactive_kvar, 2),
            "energy_kwh": round(_energy_kwh, 3),
            "peak_power_kw": round(_peak_power_kw, 2),
            "power_factor": round(power_factor, 3),
            "frequency_hz": round(frequency, 2),
            "avg_voltage_v": round(avg_voltage, 1),
            "avg_current_a": round(avg_current, 1),
            "current_imbalance_pct": round(imbalance, 1),
            "uptime_seconds": int(now - _started_at),
            "phases": {
                "L1": {
                    "voltage_v": round(voltages[0], 1),
                    "current_a": round(currents[0], 1),
                    "power_kw": round(phase_power[0], 2),
                },
                "L2": {
                    "voltage_v": round(voltages[1], 1),
                    "current_a": round(currents[1], 1),
                    "power_kw": round(phase_power[1], 2),
                },
                "L3": {
                    "voltage_v": round(voltages[2], 1),
                    "current_a": round(currents[2], 1),
                    "power_kw": round(phase_power[2], 2),
                },
            },
        }


DASHBOARD_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PowerPulse | IoT Power Monitor</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
:root{
  --bg:#06101f;--panel:rgba(13,29,50,.84);--border:rgba(111,168,255,.14);
  --text:#eef6ff;--muted:#7f98b7;--accent:#55d8ff;--good:#8dffcf;
  --warn:#ffc857;--danger:#ff6b7a;
}
*{box-sizing:border-box} body{margin:0;min-height:100vh;color:var(--text);font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;background:radial-gradient(circle at 10% 0%,rgba(35,139,255,.16),transparent 33%),radial-gradient(circle at 90% 10%,rgba(73,255,196,.08),transparent 30%),linear-gradient(145deg,var(--bg),#050b14 70%)}
body:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.14;background-image:linear-gradient(rgba(255,255,255,.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.03) 1px,transparent 1px);background-size:36px 36px}
.wrap{width:min(1480px,calc(100% - 32px));margin:auto;padding:24px 0 38px;position:relative;z-index:1}
header{display:flex;justify-content:space-between;align-items:center;gap:18px;margin-bottom:20px}.brand{display:flex;align-items:center;gap:12px}.logo{width:46px;height:46px;display:grid;place-items:center;border-radius:14px;border:1px solid rgba(85,216,255,.34);background:linear-gradient(145deg,rgba(85,216,255,.2),rgba(141,255,207,.08));font-size:23px;color:var(--accent)}
h1{margin:0;font-size:1.18rem}.sub{margin:4px 0 0;color:var(--muted);font-size:.82rem}.live{display:flex;align-items:center;gap:10px;padding:9px 13px;border:1px solid var(--border);border-radius:999px;background:rgba(8,22,38,.72);color:var(--muted);font-size:.8rem}.dot{width:9px;height:9px;border-radius:50%;background:var(--good);box-shadow:0 0 0 0 rgba(141,255,207,.55);animation:pulse 1.8s infinite}@keyframes pulse{70%{box-shadow:0 0 0 8px rgba(141,255,207,0)}}
.grid-hero{display:grid;grid-template-columns:1.2fr .8fr;gap:18px;margin-bottom:16px}.panel{background:linear-gradient(145deg,var(--panel),rgba(8,20,35,.84));border:1px solid var(--border);border-radius:22px;box-shadow:0 18px 55px rgba(0,0,0,.28);backdrop-filter:blur(14px)}.power{padding:25px 28px}.eyebrow{color:var(--muted);text-transform:uppercase;letter-spacing:.12em;font-size:.7rem;font-weight:700}.big{display:flex;align-items:baseline;gap:10px;margin-top:13px}.big strong{font-size:clamp(3.1rem,7vw,6rem);line-height:.92;letter-spacing:-.055em;font-weight:650}.big span{color:var(--accent);font-weight:700}.meta{display:flex;flex-wrap:wrap;gap:18px 28px;margin-top:22px;color:var(--muted);font-size:.8rem}.meta b{display:block;color:var(--text);margin-top:5px;font-size:.98rem}
.status{padding:22px}.status-head{display:flex;justify-content:space-between;gap:14px}.status-name{font-size:1.25rem;font-weight:680;margin-top:8px}.pill{padding:8px 11px;border-radius:999px;font-size:.7rem;font-weight:800;letter-spacing:.06em;background:rgba(141,255,207,.09);color:var(--good);border:1px solid rgba(141,255,207,.22)}.pill.warning{background:rgba(255,200,87,.1);color:var(--warn);border-color:rgba(255,200,87,.25)}.pill.danger{background:rgba(255,107,122,.1);color:var(--danger);border-color:rgba(255,107,122,.25)}
.quality{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:18px}.mini{padding:14px;border-radius:15px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.05)}.mini span{color:var(--muted);font-size:.73rem}.mini strong{display:block;margin-top:7px;font-size:1.05rem}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:16px}.metric{padding:17px 18px}.label{color:var(--muted);font-size:.73rem;font-weight:700}.value{margin-top:13px;font-size:1.55rem;font-weight:670}.unit{color:var(--accent);font-size:.78rem;margin-left:5px}.hint{margin-top:6px;color:#607995;font-size:.7rem}
.main{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(310px,.72fr);gap:18px}.chart-panel,.phase-panel{padding:21px}.title{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}.title h2{margin:0;font-size:.96rem}.title span{color:var(--muted);font-size:.7rem}.chart-wrap{height:315px}.phase-list{display:flex;flex-direction:column;gap:10px}.phase{padding:15px;border-radius:15px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.05)}.phase-top{display:flex;justify-content:space-between;margin-bottom:12px}.phase-name{font-weight:750;font-size:.8rem}.phase-values{display:grid;grid-template-columns:1fr 1fr;gap:8px;color:var(--muted);font-size:.7rem}.phase-values b{color:var(--text);float:right}.error{display:none;margin-bottom:14px;padding:11px 13px;border-radius:11px;color:#ff9ca7;background:rgba(255,107,122,.09);border:1px solid rgba(255,107,122,.22);font-size:.8rem}footer{display:flex;justify-content:space-between;gap:10px;color:#526983;font-size:.7rem;margin-top:16px;padding:0 4px}
@media(max-width:1000px){.grid-hero,.main{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}}@media(max-width:620px){.wrap{width:min(100% - 20px,1480px);padding-top:13px}.live .extra{display:none}.power,.status,.chart-panel,.phase-panel{padding:18px}.metrics{gap:9px}.metric{padding:14px}.chart-wrap{height:260px}footer{flex-direction:column}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="brand"><div class="logo">⚡</div><div><h1>PowerPulse</h1><p class="sub">Industrial IoT Energy Monitoring</p></div></div>
  <div class="live"><span class="dot"></span><b>LIVE</b><span class="extra">• refreshes every 1 second</span><span id="updated">--:--:--</span></div>
</header>
<div id="error" class="error">Live data connection lost. Retrying automatically…</div>

<section class="grid-hero">
  <div class="panel power">
    <div class="eyebrow">Real-time active power</div>
    <div class="big"><strong id="total">--</strong><span>kW</span></div>
    <div class="meta">
      <div>Total Energy<b><span id="energy">--</span> kWh</b></div>
      <div>Peak Demand<b><span id="peak">--</span> kW</b></div>
      <div>Apparent Power<b><span id="apparent">--</span> kVA</b></div>
      <div>Reactive Power<b><span id="reactive">--</span> kvar</b></div>
    </div>
  </div>
  <div class="panel status">
    <div class="status-head"><div><div class="eyebrow">System condition</div><div class="status-name">Main Distribution Board</div></div><div id="status" class="pill">NORMAL</div></div>
    <div class="quality">
      <div class="mini"><span>Power Factor</span><strong id="pf">--</strong></div>
      <div class="mini"><span>Frequency</span><strong><span id="freq">--</span> Hz</strong></div>
      <div class="mini"><span>Avg. Voltage</span><strong><span id="avgV">--</span> V</strong></div>
      <div class="mini"><span>Current Imbalance</span><strong><span id="imb">--</span> %</strong></div>
    </div>
  </div>
</section>

<section class="metrics">
  <div class="panel metric"><div class="label">L1 ACTIVE POWER</div><div class="value"><span id="l1kw">--</span><span class="unit">kW</span></div><div class="hint">Phase 1 demand</div></div>
  <div class="panel metric"><div class="label">L2 ACTIVE POWER</div><div class="value"><span id="l2kw">--</span><span class="unit">kW</span></div><div class="hint">Phase 2 demand</div></div>
  <div class="panel metric"><div class="label">L3 ACTIVE POWER</div><div class="value"><span id="l3kw">--</span><span class="unit">kW</span></div><div class="hint">Phase 3 demand</div></div>
  <div class="panel metric"><div class="label">AVERAGE CURRENT</div><div class="value"><span id="avgI">--</span><span class="unit">A</span></div><div class="hint">Across three phases</div></div>
</section>

<section class="main">
  <div class="panel chart-panel">
    <div class="title"><h2>Live Power Consumption</h2><span>Last 60 seconds</span></div>
    <div class="chart-wrap"><canvas id="powerChart"></canvas></div>
  </div>
  <div class="panel phase-panel">
    <div class="title"><h2>Three-Phase Measurements</h2><span>Live</span></div>
    <div class="phase-list">
      <div class="phase"><div class="phase-top"><div class="phase-name">● L1</div><b><span id="p1">--</span> kW</b></div><div class="phase-values"><div>Voltage <b><span id="v1">--</span> V</b></div><div>Current <b><span id="i1">--</span> A</b></div></div></div>
      <div class="phase"><div class="phase-top"><div class="phase-name">● L2</div><b><span id="p2">--</span> kW</b></div><div class="phase-values"><div>Voltage <b><span id="v2">--</span> V</b></div><div>Current <b><span id="i2">--</span> A</b></div></div></div>
      <div class="phase"><div class="phase-top"><div class="phase-name">● L3</div><b><span id="p3">--</span> kW</b></div><div class="phase-values"><div>Voltage <b><span id="v3">--</span> V</b></div><div>Current <b><span id="i3">--</span> A</b></div></div></div>
    </div>
  </div>
</section>
<footer><span>Data source: simulated smart-meter telemetry</span><span>API: /api/power • Polling: 1000 ms</span></footer>
</div>

<script>
const el=id=>document.getElementById(id);
const ctx=el('powerChart').getContext('2d');
const grad=ctx.createLinearGradient(0,0,0,310);grad.addColorStop(0,'rgba(85,216,255,.25)');grad.addColorStop(1,'rgba(85,216,255,.01)');
const chart=new Chart(ctx,{type:'line',data:{labels:[],datasets:[{data:[],borderColor:'#55d8ff',backgroundColor:grad,fill:true,pointRadius:0,borderWidth:2.2,tension:.35}]},options:{responsive:true,maintainAspectRatio:false,animation:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false},ticks:{maxTicksLimit:7,color:'#526b88'}},y:{suggestedMin:30,suggestedMax:72,grid:{color:'rgba(255,255,255,.055)'},ticks:{color:'#526b88',callback:v=>v+' kW'}}}}});
function txt(id,v){el(id).textContent=v}
function apply(d){
  txt('total',d.total_power_kw.toFixed(2));txt('energy',d.energy_kwh.toFixed(3));txt('peak',d.peak_power_kw.toFixed(2));txt('apparent',d.apparent_power_kva.toFixed(2));txt('reactive',d.reactive_power_kvar.toFixed(2));
  txt('pf',d.power_factor.toFixed(3));txt('freq',d.frequency_hz.toFixed(2));txt('avgV',d.avg_voltage_v.toFixed(1));txt('avgI',d.avg_current_a.toFixed(1));txt('imb',d.current_imbalance_pct.toFixed(1));
  const phases=['L1','L2','L3'];phases.forEach((p,n)=>{const x=d.phases[p];txt('l'+(n+1)+'kw',x.power_kw.toFixed(2));txt('p'+(n+1),x.power_kw.toFixed(2));txt('v'+(n+1),x.voltage_v.toFixed(1));txt('i'+(n+1),x.current_a.toFixed(1));});
  const pill=el('status');pill.textContent=d.status;pill.className='pill'+(d.status_level==='normal'?'':' '+d.status_level);
  const t=new Date(d.timestamp).toLocaleTimeString([], {hour:'2-digit',minute:'2-digit',second:'2-digit'});txt('updated',t);chart.data.labels.push(t);chart.data.datasets[0].data.push(d.total_power_kw);if(chart.data.labels.length>60){chart.data.labels.shift();chart.data.datasets[0].data.shift()}chart.update('none');
}
let busy=false;async function refresh(){if(busy)return;busy=true;try{const r=await fetch('/api/power',{cache:'no-store'});if(!r.ok)throw new Error(r.status);apply(await r.json());el('error').style.display='none'}catch(e){console.error(e);el('error').style.display='block'}finally{busy=false}}
refresh();setInterval(refresh,1000);
</script>
</body>
</html>'''


@application.route("/")
def index():
    return render_template_string(DASHBOARD_HTML)


@application.route("/api/power")
def api_power():
    response = jsonify(generate_dummy_power_data())
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response


@application.route("/health")
def health():
    return jsonify(
        status="ok",
        service="PowerPulse IoT Monitor",
        timestamp=datetime.now().isoformat(timespec="seconds"),
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.run(host="0.0.0.0", port=port, debug=True)
