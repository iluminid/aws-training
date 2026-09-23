from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import uuid

application = Flask(__name__)

JOURNALS = [
    {
        "id": "pearl",
        "name": "Pearl No. 01",
        "tone": "Warm Ivory",
        "price": 6800,
        "image": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?auto=format&fit=crop&w=1200&q=88"
    },
    {
        "id": "mauve",
        "name": "Mauve No. 02",
        "tone": "Dusty Rose",
        "price": 7200,
        "image": "https://images.unsplash.com/photo-1517842645767-c639042777db?auto=format&fit=crop&w=1200&q=88"
    },
    {
        "id": "sage",
        "name": "Sage No. 03",
        "tone": "Muted Green",
        "price": 7200,
        "image": "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?auto=format&fit=crop&w=1200&q=88"
    }
]

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ilume — Objects for Thought</title>
    <meta name="description" content="Ilume journals — refined objects for reflection, intention and quiet ritual.">

    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        porcelain: '#F6F1EA',
                        paper: '#FBF8F3',
                        plum: '#4D3C46',
                        mist: '#CFC6CD',
                        olive: '#A5A89B',
                        blush: '#D8C4C0',
                        almond: '#D9CCBC',
                        charcoal: '#282522'
                    },
                    fontFamily: {
                        display: ['DM Serif Display', 'serif'],
                        body: ['Manrope', 'sans-serif']
                    }
                }
            }
        }
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Manrope:wght@300;400;500;600&display=swap" rel="stylesheet">

    <style>
        html { scroll-behavior: smooth; }
        body { background:#F6F1EA; color:#282522; }

        .noise {
            background-image:
                radial-gradient(circle at 20% 20%, rgba(255,255,255,.7), transparent 18%),
                radial-gradient(circle at 80% 0%, rgba(207,198,205,.28), transparent 22%),
                radial-gradient(circle at 60% 70%, rgba(216,196,192,.22), transparent 25%);
        }

        .hairline { border-color: rgba(40,37,34,.12); }

        .card-glow {
            box-shadow: 0 25px 70px rgba(65,52,58,.10);
        }

        .soft-float {
            animation: float 7s ease-in-out infinite;
        }

        @keyframes float {
            0%,100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        .marquee {
            overflow:hidden;
            white-space:nowrap;
        }

        .marquee-track {
            display:inline-block;
            animation: marquee 20s linear infinite;
        }

        @keyframes marquee {
            from { transform: translateX(0); }
            to { transform: translateX(-50%); }
        }

        .pill {
            transition: all .25s ease;
        }

        .pill:hover {
            background:#282522;
            color:#F6F1EA;
        }

        .product img {
            transition: transform .7s cubic-bezier(.2,.7,.2,1);
        }

        .product:hover img {
            transform: scale(1.035);
        }

        input, textarea, select {
            outline:none;
        }

        ::selection {
            background:#D8C4C0;
            color:#282522;
        }
    </style>
</head>

<body class="font-body antialiased noise">

    <!-- TOP NOTE -->
    <div class="bg-charcoal text-porcelain text-[10px] sm:text-xs tracking-[0.22em] uppercase text-center py-2.5">
        Complimentary islandwide delivery on orders over LKR 10,000
    </div>

    <!-- NAV -->
    <header class="sticky top-0 z-40 bg-porcelain/90 backdrop-blur-xl border-b hairline">
        <div class="max-w-[1440px] mx-auto px-6 lg:px-10 h-20 flex items-center justify-between">
            <a href="#" class="font-display text-[34px] tracking-tight lowercase">ilume</a>

            <nav class="hidden md:flex items-center gap-10 text-xs uppercase tracking-[0.18em] text-charcoal/60">
                <a href="#collection" class="hover:text-charcoal transition">Shop</a>
                <a href="#atelier" class="hover:text-charcoal transition">Atelier</a>
                <a href="#details" class="hover:text-charcoal transition">Details</a>
            </nav>

            <button onclick="openOrder()" class="pill border border-charcoal/20 rounded-full px-5 py-2.5 text-[11px] uppercase tracking-[0.18em]">
                Order Journal
            </button>
        </div>
    </header>

    <main>

        <!-- HERO -->
        <section class="max-w-[1440px] mx-auto px-6 lg:px-10 pt-10 lg:pt-16 pb-24">
            <div class="grid lg:grid-cols-[1.05fr_.95fr] gap-8 lg:gap-14 items-stretch">

                <!-- editorial panel -->
                <div class="min-h-[700px] bg-paper rounded-[36px] p-8 sm:p-12 lg:p-16 flex flex-col justify-between border hairline">
                    <div class="flex items-center justify-between text-[10px] sm:text-xs tracking-[0.2em] uppercase text-charcoal/45">
                        <span>Edition 01 — 2026</span>
                        <span>Objects for Thought</span>
                    </div>

                    <div class="max-w-3xl my-14">
                        <div class="text-xs uppercase tracking-[0.22em] text-charcoal/40 mb-7">
                            For quiet minds & beautiful routines
                        </div>

                        <h1 class="font-display text-[68px] sm:text-[88px] lg:text-[110px] leading-[.84] tracking-[-0.04em]">
                            A softer<br>
                            way to
                            <span class="italic text-plum">begin.</span>
                        </h1>

                        <p class="mt-9 max-w-xl text-base sm:text-lg leading-8 text-charcoal/60 font-light">
                            Ilume journals are designed like small interior objects:
                            tactile, poised, timeless and made to live beautifully beside you.
                        </p>
                    </div>

                    <div class="flex flex-col sm:flex-row sm:items-center gap-5 sm:gap-8">
                        <a href="#collection" class="inline-flex items-center justify-center rounded-full bg-charcoal text-porcelain px-7 py-4 text-[11px] uppercase tracking-[0.18em]">
                            Discover Edition 01
                        </a>

                        <div class="text-xs text-charcoal/45">
                            Lay-flat binding · 120gsm paper · Linen-touch covers
                        </div>
                    </div>
                </div>

                <!-- art image -->
                <div class="relative min-h-[700px] rounded-[36px] overflow-hidden card-glow">
                    <img
                        src="https://images.unsplash.com/photo-1497215728101-856f4ea42174?auto=format&fit=crop&w=1500&q=90"
                        alt="Minimal luxury desk with journal"
                        class="absolute inset-0 w-full h-full object-cover"
                    >
                    <div class="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-charcoal/30"></div>

                    <div class="absolute left-6 right-6 bottom-6 bg-porcelain/88 backdrop-blur-xl rounded-[26px] p-6 sm:p-7">
                        <div class="flex items-end justify-between gap-6">
                            <div>
                                <div class="text-[10px] uppercase tracking-[0.22em] text-charcoal/45">Studio note</div>
                                <div class="font-display text-3xl sm:text-4xl mt-2">Made to sit beautifully in your day.</div>
                            </div>
                            <div class="hidden sm:block text-xs text-charcoal/50 max-w-[170px] leading-6">
                                Minimal forms. Gentle texture. A calm place for everything in your head.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- MARQUEE -->
        <section class="border-y hairline py-5 bg-porcelain/60">
            <div class="marquee text-[11px] tracking-[0.28em] uppercase text-charcoal/45">
                <div class="marquee-track">
                    Ilume&nbsp;&nbsp;·&nbsp;&nbsp;Write Slowly&nbsp;&nbsp;·&nbsp;&nbsp;Keep Beautifully&nbsp;&nbsp;·&nbsp;&nbsp;Reflect Often&nbsp;&nbsp;·&nbsp;&nbsp;
                    Ilume&nbsp;&nbsp;·&nbsp;&nbsp;Write Slowly&nbsp;&nbsp;·&nbsp;&nbsp;Keep Beautifully&nbsp;&nbsp;·&nbsp;&nbsp;Reflect Often&nbsp;&nbsp;·&nbsp;&nbsp;
                </div>
            </div>
        </section>

        <!-- PRODUCTS -->
        <section id="collection" class="max-w-[1440px] mx-auto px-6 lg:px-10 py-28">
            <div class="grid lg:grid-cols-[.65fr_1.35fr] gap-14">
                <div class="lg:sticky lg:top-28 lg:self-start">
                    <div class="text-[10px] uppercase tracking-[0.24em] text-charcoal/40">Edition 01</div>
                    <h2 class="font-display text-5xl sm:text-6xl mt-4 leading-[.95]">
                        Three tones.<br>One quiet ritual.
                    </h2>
                    <p class="mt-6 max-w-sm leading-7 text-charcoal/55 text-sm">
                        A restrained palette inspired by calm interiors, early light,
                        linen, dried petals and quiet rooms.
                    </p>
                </div>

                <div class="space-y-8">
                    {% for journal in journals %}
                    <article class="product bg-paper rounded-[30px] overflow-hidden border hairline grid md:grid-cols-[1.1fr_.9fr] min-h-[430px]">
                        <div class="overflow-hidden">
                            <img src="{{ journal.image }}" alt="{{ journal.name }}" class="w-full h-full object-cover min-h-[360px]">
                        </div>

                        <div class="p-8 sm:p-10 flex flex-col justify-between">
                            <div>
                                <div class="flex items-center justify-between text-[10px] uppercase tracking-[0.2em] text-charcoal/40">
                                    <span>{{ journal.tone }}</span>
                                    <span>Edition 01</span>
                                </div>

                                <h3 class="font-display text-4xl sm:text-5xl mt-7">{{ journal.name }}</h3>

                                <p class="mt-5 text-sm leading-7 text-charcoal/55">
                                    192 softly toned pages, subtle ruled layout,
                                    ribbon marker and understated foil detail.
                                </p>
                            </div>

                            <div class="mt-10 flex items-center justify-between gap-4">
                                <div>
                                    <div class="text-[10px] uppercase tracking-[0.18em] text-charcoal/40">Price</div>
                                    <div class="font-display text-2xl mt-1">LKR {{ "{:,}".format(journal.price) }}</div>
                                </div>

                                <button onclick="openOrder('{{ journal.id }}')" class="pill rounded-full border border-charcoal/20 px-6 py-3 text-[11px] uppercase tracking-[0.18em]">
                                    Select
                                </button>
                            </div>
                        </div>
                    </article>
                    {% endfor %}
                </div>
            </div>
        </section>

        <!-- ATELIER -->
        <section id="atelier" class="bg-plum text-porcelain py-28">
            <div class="max-w-[1280px] mx-auto px-6 lg:px-10 grid lg:grid-cols-2 gap-16 items-center">
                <div class="relative">
                    <div class="absolute -top-5 -left-5 w-28 h-28 border border-white/15 rounded-full"></div>
                    <img
                        src="https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1200&q=88"
                        alt="Handwriting in a journal"
                        class="relative rounded-[34px] w-full aspect-[4/5] object-cover"
                    >
                </div>

                <div class="lg:pl-8">
                    <div class="text-[10px] uppercase tracking-[0.24em] text-white/45">The atelier</div>
                    <h2 class="font-display text-5xl sm:text-6xl mt-5 leading-[.98]">
                        Designed for people who notice small things.
                    </h2>

                    <p class="mt-8 leading-8 text-white/65 font-light">
                        The weight of a page. The way a cover feels in the hand.
                        The quiet satisfaction of a ribbon falling exactly where it should.
                    </p>

                    <p class="mt-5 leading-8 text-white/65 font-light">
                        Ilume is less about productivity and more about presence.
                        A private place to collect ideas, memories, lists, plans and unfinished thoughts.
                    </p>

                    <div class="grid grid-cols-3 gap-5 mt-12">
                        <div>
                            <div class="font-display text-3xl">192</div>
                            <div class="text-[10px] uppercase tracking-[0.18em] text-white/40 mt-1">Pages</div>
                        </div>
                        <div>
                            <div class="font-display text-3xl">120gsm</div>
                            <div class="text-[10px] uppercase tracking-[0.18em] text-white/40 mt-1">Paper</div>
                        </div>
                        <div>
                            <div class="font-display text-3xl">A5</div>
                            <div class="text-[10px] uppercase tracking-[0.18em] text-white/40 mt-1">Format</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- DETAIL GRID -->
        <section id="details" class="max-w-[1280px] mx-auto px-6 lg:px-10 py-28">
            <div class="text-center max-w-2xl mx-auto">
                <div class="text-[10px] uppercase tracking-[0.24em] text-charcoal/40">Considered details</div>
                <h2 class="font-display text-5xl sm:text-6xl mt-4">Nothing loud. Nothing accidental.</h2>
            </div>

            <div class="grid md:grid-cols-3 gap-6 mt-16">
                <div class="rounded-[28px] bg-paper border hairline p-8">
                    <div class="font-display text-5xl text-mist">01</div>
                    <h3 class="font-display text-3xl mt-8">Soft paper</h3>
                    <p class="mt-3 text-sm leading-7 text-charcoal/55">
                        Smooth enough for fountain pens, substantial enough to feel special.
                    </p>
                </div>

                <div class="rounded-[28px] bg-[#EAE0DC] border hairline p-8">
                    <div class="font-display text-5xl text-plum/30">02</div>
                    <h3 class="font-display text-3xl mt-8">Quiet palette</h3>
                    <p class="mt-3 text-sm leading-7 text-charcoal/55">
                        Tones chosen to complement your desk, shelf, bedside and everyday carry.
                    </p>
                </div>

                <div class="rounded-[28px] bg-[#E6E5DD] border hairline p-8">
                    <div class="font-display text-5xl text-olive/50">03</div>
                    <h3 class="font-display text-3xl mt-8">Lay-flat form</h3>
                    <p class="mt-3 text-sm leading-7 text-charcoal/55">
                        Opens naturally so writing feels effortless from first page to last.
                    </p>
                </div>
            </div>
        </section>

        <!-- CTA -->
        <section class="px-6 lg:px-10 pb-24">
            <div class="max-w-[1440px] mx-auto rounded-[38px] bg-[#DDD3C8] px-8 sm:px-12 lg:px-16 py-16 lg:py-20 flex flex-col lg:flex-row items-start lg:items-end justify-between gap-12">
                <div class="max-w-3xl">
                    <div class="text-[10px] uppercase tracking-[0.24em] text-charcoal/40">For your next chapter</div>
                    <h2 class="font-display text-5xl sm:text-7xl mt-4 leading-[.9]">
                        Choose the journal you’ll want to keep forever.
                    </h2>
                </div>

                <button onclick="openOrder()" class="rounded-full bg-charcoal text-porcelain px-8 py-4 text-[11px] uppercase tracking-[0.18em] whitespace-nowrap">
                    Place Order
                </button>
            </div>
        </section>

    </main>

    <footer class="border-t hairline">
        <div class="max-w-[1440px] mx-auto px-6 lg:px-10 py-10 flex flex-col md:flex-row gap-5 md:items-center md:justify-between">
            <div class="font-display text-3xl lowercase">ilume</div>
            <div class="text-xs text-charcoal/45">Objects for thought. Made for slow living.</div>
            <div class="text-xs text-charcoal/45">&copy; {{ year }} Ilume</div>
        </div>
    </footer>

    <!-- ORDER OVERLAY -->
    <div id="orderOverlay" class="fixed inset-0 z-[80] hidden">
        <div class="absolute inset-0 bg-charcoal/40 backdrop-blur-md" onclick="closeOrder()"></div>

        <div class="absolute inset-x-3 bottom-3 sm:inset-auto sm:right-5 sm:top-5 sm:bottom-5 sm:w-[560px] bg-paper rounded-[34px] overflow-y-auto shadow-2xl">
            <div class="p-7 sm:p-9">

                <div class="flex items-start justify-between gap-6">
                    <div>
                        <div class="text-[10px] uppercase tracking-[0.22em] text-charcoal/40">Private order</div>
                        <h2 class="font-display text-4xl mt-2">Choose your Ilume.</h2>
                    </div>

                    <button onclick="closeOrder()" class="w-10 h-10 rounded-full border border-charcoal/15 text-lg">
                        ×
                    </button>
                </div>

                <form id="orderForm" class="mt-8 space-y-5">

                    <div>
                        <label class="block text-[10px] uppercase tracking-[0.18em] text-charcoal/45 mb-2">Journal</label>
                        <select id="journal" name="journal" class="w-full rounded-2xl border border-charcoal/10 bg-porcelain px-4 py-4" required>
                            {% for journal in journals %}
                            <option value="{{ journal.id }}">{{ journal.name }} — LKR {{ "{:,}".format(journal.price) }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="grid sm:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-[10px] uppercase tracking-[0.18em] text-charcoal/45 mb-2">Quantity</label>
                            <input name="quantity" type="number" min="1" max="10" value="1" required
                                   class="w-full rounded-2xl border border-charcoal/10 bg-porcelain px-4 py-4">
                        </div>

                        <div>
                            <label class="block text-[10px] uppercase tracking-[0.18em] text-charcoal/45 mb-2">Full name</label>
                            <input name="name" type="text" required placeholder="Your name"
                                   class="w-full rounded-2xl border border-charcoal/10 bg-porcelain px-4 py-4">
                        </div>
                    </div>

                    <div>
                        <label class="block text-[10px] uppercase tracking-[0.18em] text-charcoal/45 mb-2">Email</label>
                        <input name="email" type="email" required placeholder="you@example.com"
                               class="w-full rounded-2xl border border-charcoal/10 bg-porcelain px-4 py-4">
                    </div>

                    <div>
                        <label class="block text-[10px] uppercase tracking-[0.18em] text-charcoal/45 mb-2">Phone</label>
                        <input name="phone" type="tel" required placeholder="+94 7X XXX XXXX"
                               class="w-full rounded-2xl border border-charcoal/10 bg-porcelain px-4 py-4">
                    </div>

                    <div>
                        <label class="block text-[10px] uppercase tracking-[0.18em] text-charcoal/45 mb-2">Delivery address</label>
                        <textarea name="address" rows="4" required placeholder="Street, city, postal code"
                                  class="w-full rounded-2xl border border-charcoal/10 bg-porcelain px-4 py-4 resize-none"></textarea>
                    </div>

                    <div>
                        <label class="block text-[10px] uppercase tracking-[0.18em] text-charcoal/45 mb-2">Gift note <span class="normal-case tracking-normal">(optional)</span></label>
                        <textarea name="note" rows="3" placeholder="Add a message..."
                                  class="w-full rounded-2xl border border-charcoal/10 bg-porcelain px-4 py-4 resize-none"></textarea>
                    </div>

                    <button type="submit"
                            class="w-full rounded-full bg-charcoal text-porcelain px-7 py-4 text-[11px] uppercase tracking-[0.18em]">
                        Confirm Order
                    </button>

                    <p class="text-center text-[10px] leading-5 text-charcoal/40">
                        Demo checkout. Connect the Flask order endpoint to your database and payment gateway for production.
                    </p>
                </form>

                <div id="successState" class="hidden py-16 text-center">
                    <div class="w-16 h-16 mx-auto rounded-full bg-[#E8DFD7] flex items-center justify-center text-2xl">
                        ✓
                    </div>
                    <div class="font-display text-4xl mt-6">Beautiful choice.</div>
                    <p class="mt-3 text-sm text-charcoal/55">Your Ilume order has been received.</p>
                    <div id="orderReference" class="mt-5 text-[10px] uppercase tracking-[0.2em] text-charcoal/45"></div>

                    <button onclick="closeOrder()"
                            class="mt-8 rounded-full border border-charcoal/15 px-6 py-3 text-[11px] uppercase tracking-[0.18em]">
                        Continue browsing
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        function openOrder(journalId) {
            const overlay = document.getElementById('orderOverlay');
            overlay.classList.remove('hidden');
            document.body.style.overflow = 'hidden';

            if (journalId) {
                document.getElementById('journal').value = journalId;
            }
        }

        function closeOrder() {
            document.getElementById('orderOverlay').classList.add('hidden');
            document.body.style.overflow = '';
            document.getElementById('orderForm').classList.remove('hidden');
            document.getElementById('successState').classList.add('hidden');
        }

        document.getElementById('orderForm').addEventListener('submit', async function(event) {
            event.preventDefault();

            const button = event.target.querySelector('button[type="submit"]');
            const original = button.textContent;
            button.disabled = true;
            button.textContent = 'Submitting...';

            const payload = Object.fromEntries(new FormData(event.target).entries());

            try {
                const response = await fetch('/api/order', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.message || 'Unable to place order.');
                }

                document.getElementById('orderForm').classList.add('hidden');
                document.getElementById('successState').classList.remove('hidden');
                document.getElementById('orderReference').textContent =
                    'Order reference · ' + data.order_id;

                event.target.reset();

            } catch (error) {
                alert(error.message);
            } finally {
                button.disabled = false;
                button.textContent = original;
            }
        });
    </script>

</body>
</html>
"""

@application.route("/")
def home():
    return render_template_string(
        PAGE,
        journals=JOURNALS,
        year=datetime.now().year
    )

@application.route("/api/order", methods=["POST"])
def place_order():
    data = request.get_json(silent=True) or {}

    required = ["journal", "quantity", "name", "email", "phone", "address"]
    missing = [field for field in required if not str(data.get(field, "")).strip()]

    if missing:
        return jsonify({
            "success": False,
            "message": "Please complete all required fields."
        }), 400

    selected = next((j for j in JOURNALS if j["id"] == data["journal"]), None)
    if not selected:
        return jsonify({
            "success": False,
            "message": "The selected journal is not available."
        }), 400

    try:
        quantity = int(data["quantity"])
        if quantity < 1 or quantity > 10:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Quantity must be between 1 and 10."
        }), 400

    order_id = "ILM-" + uuid.uuid4().hex[:8].upper()
    total = selected["price"] * quantity

    # In production:
    # 1. Save order to a database.
    # 2. Trigger email/WhatsApp confirmation.
    # 3. Redirect to a payment gateway if required.
    print({
        "order_id": order_id,
        "journal": selected["name"],
        "quantity": quantity,
        "total_lkr": total,
        "customer": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "address": data.get("address"),
        "note": data.get("note", "")
    })

    return jsonify({
        "success": True,
        "order_id": order_id,
        "total_lkr": total,
        "message": "Order received."
    }), 201

@application.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "ilume-edition-01",
        "timestamp_utc": datetime.utcnow().isoformat() + "Z"
    }), 200

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000, debug=True)
