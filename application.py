from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ILUME — Journals for Intentional Living</title>
<meta name="description" content="ILUME creates refined journals for reflection, intention and timeless living.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#171614; --muted:#6d675f; --paper:#fbf8f2; --cream:#f2ece2;
  --line:#ded5c8; --gold:#a8875d; --dark:#23211f;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:Inter,Arial,sans-serif;background:var(--paper);color:var(--ink);line-height:1.6}
a{text-decoration:none;color:inherit}
.container{width:min(1180px,90%);margin:auto}
header{position:sticky;top:0;z-index:20;background:rgba(251,248,242,.9);backdrop-filter:blur(14px);border-bottom:1px solid rgba(222,213,200,.7)}
.nav{height:78px;display:flex;align-items:center;justify-content:space-between}
.brand{font-family:"Playfair Display",serif;font-size:1.55rem;letter-spacing:.28em;font-weight:600}
.links{display:flex;gap:32px;color:var(--muted);font-size:.9rem}
.links a:hover{color:var(--ink)}
.hero{min-height:88vh;display:grid;align-items:center;padding:80px 0}
.hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:70px;align-items:center}
.eyebrow{text-transform:uppercase;letter-spacing:.22em;font-size:.76rem;color:var(--gold);margin-bottom:20px}
h1,h2,h3{font-family:"Playfair Display",serif;font-weight:500}
h1{font-size:clamp(3.5rem,7vw,7rem);line-height:.98;margin:0 0 28px}
h1 em{font-weight:500}
.hero p{max-width:590px;color:var(--muted);font-size:1.05rem;margin-bottom:34px}
.actions{display:flex;gap:14px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 24px;border:1px solid var(--ink);font-size:.88rem;transition:.25s}
.btn.primary{background:var(--ink);color:white}
.btn.primary:hover{background:transparent;color:var(--ink)}
.btn.secondary:hover{background:var(--ink);color:white}
.stage{position:relative;min-height:550px;display:grid;place-items:center}
.halo{position:absolute;width:430px;height:430px;border-radius:50%;background:radial-gradient(circle at 40% 35%,rgba(255,255,255,.95),rgba(200,181,154,.35) 46%,rgba(168,135,93,.08) 70%,transparent 72%)}
.book{position:relative;width:320px;height:430px;border-radius:5px 14px 14px 5px;background:linear-gradient(135deg,#1f1d1a,#3c3731);box-shadow:0 38px 70px rgba(45,37,28,.27);transform:rotate(-6deg);display:grid;place-items:center}
.book:before{content:"";position:absolute;left:12px;top:0;bottom:0;width:2px;background:rgba(255,255,255,.08)}
.book:after{content:"";position:absolute;inset:16px;border:1px solid rgba(205,169,111,.45);border-radius:4px 10px 10px 4px}
.book span{font-family:"Playfair Display",serif;color:#d5bb8d;letter-spacing:.28em;font-size:1.45rem;z-index:1}
.section{padding:115px 0}
.section-head{display:grid;grid-template-columns:.8fr 1.2fr;gap:60px;align-items:end;margin-bottom:60px}
h2{font-size:clamp(2.3rem,4.2vw,4.2rem);line-height:1.08;margin:0}
.section-head p{margin:0;color:var(--muted);max-width:630px}
.collection{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.card{border-top:1px solid var(--line);padding-top:24px}
.cover{height:380px;border-radius:4px 10px 10px 4px;margin-bottom:24px;display:grid;place-items:center;font-family:"Playfair Display",serif;letter-spacing:.2em;box-shadow:0 18px 40px rgba(70,58,44,.12)}
.cover.one{background:#2b2926;color:#d7bd8f}
.cover.two{background:#c6b59b;color:#2d2823}
.cover.three{background:#e6ded1;color:#41382f}
.card h3{font-size:1.55rem;margin:0 0 8px}
.card p{color:var(--muted);margin:0;font-size:.94rem}
.philosophy{background:var(--cream)}
.quote{max-width:900px;text-align:center;margin:auto}
.quote p{font-family:"Playfair Display",serif;font-size:clamp(2rem,4.4vw,4.5rem);line-height:1.15;margin:0}
.quote span{display:block;margin-top:28px;color:var(--muted);font-size:.8rem;letter-spacing:.14em;text-transform:uppercase}
.ritual{display:grid;grid-template-columns:repeat(3,1fr);gap:40px}
.ritual article{border-top:1px solid var(--line);padding-top:25px}
.no{color:var(--gold);font-size:.76rem;letter-spacing:.2em;margin-bottom:16px}
.ritual h3{font-size:1.55rem;margin:0 0 10px}
.ritual p{color:var(--muted);margin:0}
.news{background:var(--dark);color:#fff;padding:95px 0}
.news-grid{display:grid;grid-template-columns:1fr 1fr;gap:70px;align-items:end}
.news p{color:#c9c1b6;max-width:520px}
.signup{display:flex;border-bottom:1px solid #6d665d}
.signup input{flex:1;border:0;outline:0;background:transparent;color:#fff;padding:18px 0;font:inherit}
.signup input::placeholder{color:#918a80}
.signup button{border:0;background:none;color:#fff;cursor:pointer;font-size:.8rem;letter-spacing:.1em}
footer{background:var(--dark);color:#aaa198;border-top:1px solid rgba(255,255,255,.08);padding:30px 0}
.footer{display:flex;justify-content:space-between;gap:20px;font-size:.82rem}
@media(max-width:860px){
 .links{display:none}
 .hero-grid,.section-head,.news-grid{grid-template-columns:1fr}
 .collection,.ritual{grid-template-columns:1fr}
 .stage{min-height:460px}
 .book{width:270px;height:365px}
 .halo{width:340px;height:340px}
 .cover{height:320px}
 .section{padding:85px 0}
 .footer{flex-direction:column}
}
</style>
</head>
<body>
<header>
  <div class="container nav">
    <a href="#" class="brand">ILUME</a>
    <nav class="links">
      <a href="#collection">Collection</a>
      <a href="#philosophy">Philosophy</a>
      <a href="#ritual">The Ritual</a>
      <a href="#letters">Letters</a>
    </nav>
  </div>
</header>

<main>
<section class="hero">
  <div class="container hero-grid">
    <div>
      <div class="eyebrow">Journals for intentional living</div>
      <h1>Make space for what <em>matters.</em></h1>
      <p>ILUME creates beautifully considered journals for reflection, focus and quiet ambition. Designed to live beside you — through ideas, seasons and becoming.</p>
      <div class="actions">
        <a class="btn primary" href="#collection">Explore the collection</a>
        <a class="btn secondary" href="#philosophy">Our philosophy</a>
      </div>
    </div>
    <div class="stage">
      <div class="halo"></div>
      <div class="book"><span>ILUME</span></div>
    </div>
  </div>
</section>

<section class="section" id="collection">
  <div class="container">
    <div class="section-head">
      <div>
        <div class="eyebrow">The collection</div>
        <h2>Designed for the way you think.</h2>
      </div>
      <p>Purposeful pages, refined materials and understated design. Each ILUME journal is created to make writing feel like a ritual.</p>
    </div>

    <div class="collection">
      <article class="card">
        <div class="cover one">ILUME</div>
        <h3>The Reflection Journal</h3>
        <p>A quiet companion for daily notes, deeper reflection and thoughtful beginnings.</p>
      </article>
      <article class="card">
        <div class="cover two">ILUME</div>
        <h3>The Intention Journal</h3>
        <p>Designed around clarity, priorities and the small decisions that shape meaningful progress.</p>
      </article>
      <article class="card">
        <div class="cover three">ILUME</div>
        <h3>The Unbound Journal</h3>
        <p>Open pages for ideas without structure — sketches, fragments, observations and everything between.</p>
      </article>
    </div>
  </div>
</section>

<section class="section philosophy" id="philosophy">
  <div class="container quote">
    <p>“A beautiful life is rarely built in a rush. It begins with noticing.”</p>
    <span>The ILUME philosophy</span>
  </div>
</section>

<section class="section" id="ritual">
  <div class="container">
    <div class="section-head">
      <div>
        <div class="eyebrow">The ritual</div>
        <h2>A little more presence, every day.</h2>
      </div>
      <p>ILUME is not about writing more. It is about noticing more. A few intentional minutes can change the quality of an entire day.</p>
    </div>

    <div class="ritual">
      <article>
        <div class="no">01</div>
        <h3>Arrive</h3>
        <p>Put away the noise. Open your journal and give yourself one uninterrupted moment.</p>
      </article>
      <article>
        <div class="no">02</div>
        <h3>Notice</h3>
        <p>Write what is present — an idea, a feeling, a question, an intention worth keeping.</p>
      </article>
      <article>
        <div class="no">03</div>
        <h3>Illuminate</h3>
        <p>Return to what matters with greater clarity, perspective and purpose.</p>
      </article>
    </div>
  </div>
</section>

<section class="news" id="letters">
  <div class="container news-grid">
    <div>
      <div class="eyebrow">Letters from ILUME</div>
      <h2>Notes on reflection, creativity and intentional living.</h2>
      <p>Occasional letters for people who value beautiful objects, thoughtful routines and a slower kind of clarity.</p>
    </div>
    <form class="signup" onsubmit="event.preventDefault(); alert('Welcome to ILUME.');">
      <input type="email" placeholder="Your email address" required>
      <button type="submit">JOIN</button>
    </form>
  </div>
</section>
</main>

<footer>
  <div class="container footer">
    <div>© 2026 ILUME. All rights reserved.</div>
    <div>Designed for a life well considered.</div>
  </div>
</footer>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
