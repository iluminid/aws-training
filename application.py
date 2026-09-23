from flask import Flask, render_template_string, request, jsonify
from datetime import datetime
import uuid

application = Flask(__name__)

PRODUCTS = [
    {
        "id": "ivory",
        "name": "The Ivory Journal",
        "subtitle": "Quiet luxury, made for slow mornings.",
        "price": 6900,
        "image": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=1200&q=88"
    },
    {
        "id": "sage",
        "name": "The Sage Journal",
        "subtitle": "A soft green companion for thoughtful days.",
        "price": 7200,
        "image": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?auto=format&fit=crop&w=1200&q=88"
    },
    {
        "id": "rose",
        "name": "The Blush Journal",
        "subtitle": "Warm, delicate, and designed to be kept.",
        "price": 7200,
        "image": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=1200&q=88"
    }
]

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ilume — Journals for a Beautiful Life</title>
    <meta name="description" content="Ilume creates timeless journals designed for reflection, intention and beautifully lived days.">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {
        theme: {
          extend: {
            colors: {
              cream: '#F7F3EC',
              sand: '#E8DFD2',
              taupe: '#B7A896',
              ink: '#2E2A26',
              sage: '#A8AD9D',
              rose: '#DCC8C1'
            },
            fontFamily: {
              serif: ['Cormorant Garamond', 'serif'],
              sans: ['Inter', 'sans-serif']
            }
          }
        }
      }
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

    <style>
        html { scroll-behavior: smooth; }
        body { background: #F7F3EC; color: #2E2A26; }
        .glass {
            background: rgba(247,243,236,.78);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }
        .soft-shadow { box-shadow: 0 30px 80px rgba(67, 53, 39, .10); }
        .lift { transition: transform .35s ease, box-shadow .35s ease; }
        .lift:hover { transform: translateY(-6px); box-shadow: 0 24px 60px rgba(67, 53, 39, .13); }
        .reveal { animation: reveal .9s ease both; }
        @keyframes reveal {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .line { width: 42px; height: 1px; background: #B7A896; }
        input, textarea, select { outline: none; }
        ::selection { background: #DCC8C1; color: #2E2A26; }
    </style>
</head>

<body class="font-sans antialiased">
    <header class="fixed top-0 inset-x-0 z-50 glass border-b border-black/5">
        <div class="max-w-7xl mx-auto px-6 lg:px-10 h-20 flex items-center justify-between">
            <a href="#" class="font-serif text-3xl tracking-[0.18em] lowercase">ilume</a>

            <nav class="hidden md:flex items-center gap-9 text-[13px] tracking-[0.16em] uppercase text-ink/70">
                <a href="#collection" class="hover:text-ink transition">Collection</a>
                <a href="#story" class="hover:text-ink transition">Our Story</a>
                <a href="#ritual" class="hover:text-ink transition">The Ritual</a>
            </nav>

            <button onclick="openOrder()" class="rounded-full border border-ink/20 px-5 py-2.5 text-xs tracking-[0.16em] uppercase hover:bg-ink hover:text-cream transition">
                Place Order
            </button>
        </div>
    </header>

    <main>
        <!-- HERO -->
        <section class="min-h-screen pt-20 grid lg:grid-cols-2">
            <div class="flex items-center px-7 sm:px-12 lg:px-20 xl:px-28 py-16">
                <div class="max-w-xl reveal">
                    <div class="flex items-center gap-4 mb-8">
                        <div class="line"></div>
                        <span class="text-[11px] tracking-[0.28em] uppercase text-ink/55">A slower way to remember</span>
                    </div>

                    <h1 class="font-serif text-6xl sm:text-7xl xl:text-[92px] leading-[0.92] font-medium tracking-[-0.03em]">
                        Make space<br>for what <em class="font-normal text-taupe">matters.</em>
                    </h1>

                    <p class="mt-8 text-base sm:text-lg leading-8 text-ink/65 max-w-lg font-light">
                        Thoughtfully crafted journals for ideas, intentions, quiet reflections
                        and the beautiful details you never want to forget.
                    </p>

                    <div class="mt-10 flex flex-wrap gap-4">
                        <a href="#collection" class="rounded-full bg-ink text-cream px-7 py-4 text-xs tracking-[0.18em] uppercase hover:opacity-90 transition">
                            Explore the collection
                        </a>
                        <a href="#story" class="rounded-full border border-ink/15 px-7 py-4 text-xs tracking-[0.18em] uppercase hover:bg-white/50 transition">
                            Discover Ilume
                        </a>
                    </div>

                    <div class="mt-14 flex items-center gap-8 text-xs text-ink/55">
                        <div><span class="block font-serif text-2xl text-ink">192</span>cream pages</div>
                        <div class="h-9 w-px bg-ink/10"></div>
                        <div><span class="block font-serif text-2xl text-ink">120gsm</span>premium paper</div>
                        <div class="h-9 w-px bg-ink/10"></div>
                        <div><span class="block font-serif text-2xl text-ink">A5</span>lay-flat binding</div>
                    </div>
                </div>
            </div>

            <div class="relative min-h-[620px] lg:min-h-0 overflow-hidden">
                <img
                    src="https://images.unsplash.com/photo-1494438639946-1ebd1d20bf85?auto=format&fit=crop&w=1600&q=90"
                    alt="Elegant journal and lifestyle setting"
                    class="absolute inset-0 w-full h-full object-cover"
                >
                <div class="absolute inset-0 bg-gradient-to-t from-black/25 via-transparent to-transparent"></div>
                <div class="absolute left-8 bottom-8 bg-cream/90 backdrop-blur-md rounded-2xl px-5 py-4 soft-shadow max-w-[260px]">
                    <div class="font-serif text-xl">The art of writing by hand.</div>
                    <div class="text-xs text-ink/60 mt-1 leading-5">Designed to feel beautiful before the first word is written.</div>
                </div>
            </div>
        </section>

        <!-- COLLECTION -->
        <section id="collection" class="px-6 sm:px-10 lg:px-16 py-28 max-w-7xl mx-auto">
            <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-6 mb-14">
                <div>
                    <span class="text-[11px] tracking-[0.28em] uppercase text-ink/50">The first collection</span>
                    <h2 class="font-serif text-5xl sm:text-6xl mt-3">Journals to keep close.</h2>
                </div>
                <p class="max-w-sm text-sm leading-7 text-ink/55">
                    Linen-inspired covers, understated palettes and paper chosen for the pleasure of writing.
                </p>
            </div>

            <div class="grid md:grid-cols-3 gap-7">
                {% for product in products %}
                <article class="group lift bg-[#FBF8F3] rounded-[28px] overflow-hidden border border-black/5">
                    <div class="aspect-[4/5] overflow-hidden">
                        <img src="{{ product.image }}" alt="{{ product.name }}" class="w-full h-full object-cover group-hover:scale-[1.03] transition duration-700">
                    </div>
                    <div class="p-6">
                        <div class="flex items-start justify-between gap-4">
                            <div>
                                <h3 class="font-serif text-3xl">{{ product.name }}</h3>
                                <p class="mt-2 text-sm leading-6 text-ink/55">{{ product.subtitle }}</p>
                            </div>
                            <div class="text-sm whitespace-nowrap">LKR {{ "{:,}".format(product.price) }}</div>
                        </div>
                        <button onclick="openOrder('{{ product.id }}')" class="mt-6 w-full rounded-full border border-ink/15 px-5 py-3 text-xs tracking-[0.16em] uppercase hover:bg-ink hover:text-cream transition">
                            Order this journal
                        </button>
                    </div>
                </article>
                {% endfor %}
            </div>
        </section>

        <!-- STORY -->
        <section id="story" class="bg-[#EEE7DD] py-28 px-6 sm:px-10">
            <div class="max-w-7xl mx-auto grid lg:grid-cols-2 gap-14 lg:gap-24 items-center">
                <div class="relative">
                    <img
                        src="https://images.unsplash.com/photo-1456324504439-367cee3b3c32?auto=format&fit=crop&w=1400&q=88"
                        alt="Writing in a journal"
                        class="rounded-[36px] w-full aspect-[5/6] object-cover soft-shadow"
                    >
                    <div class="absolute -bottom-8 -right-2 sm:right-10 bg-cream p-7 rounded-3xl max-w-xs soft-shadow">
                        <p class="font-serif text-2xl leading-8">“A journal should feel like an invitation, never an obligation.”</p>
                    </div>
                </div>

                <div class="lg:pr-10">
                    <span class="text-[11px] tracking-[0.28em] uppercase text-ink/50">The Ilume philosophy</span>
                    <h2 class="font-serif text-5xl sm:text-6xl leading-[1.02] mt-4">
                        Beautiful things make everyday rituals feel sacred.
                    </h2>
                    <p class="mt-8 text-base leading-8 text-ink/60 font-light">
                        Ilume was imagined for people who still believe in paper, pause and presence.
                        Our journals are intentionally simple: soft colors, tactile materials, generous pages
                        and no unnecessary noise.
                    </p>
                    <p class="mt-5 text-base leading-8 text-ink/60 font-light">
                        Keep plans, dreams, sketches, gratitude lists, private thoughts or nothing at all.
                        The blank page is yours.
                    </p>
                </div>
            </div>
        </section>

        <!-- RITUAL -->
        <section id="ritual" class="py-28 px-6 sm:px-10">
            <div class="max-w-6xl mx-auto text-center">
                <span class="text-[11px] tracking-[0.28em] uppercase text-ink/50">Your daily ritual</span>
                <h2 class="font-serif text-5xl sm:text-6xl mt-4">Light a moment. Write it down.</h2>
                <p class="max-w-2xl mx-auto mt-6 text-ink/55 leading-8">
                    Five quiet minutes in the morning or one final page before bed.
                    Ilume is made for the ritual you create for yourself.
                </p>

                <div class="grid sm:grid-cols-3 gap-8 mt-16 text-left">
                    <div class="border-t border-ink/15 pt-6">
                        <div class="font-serif text-4xl text-taupe">01</div>
                        <h3 class="font-serif text-2xl mt-4">Pause</h3>
                        <p class="mt-2 text-sm leading-6 text-ink/55">Step away from the screen and create a little room to think.</p>
                    </div>
                    <div class="border-t border-ink/15 pt-6">
                        <div class="font-serif text-4xl text-taupe">02</div>
                        <h3 class="font-serif text-2xl mt-4">Write</h3>
                        <p class="mt-2 text-sm leading-6 text-ink/55">Put thoughts into words without editing them before they arrive.</p>
                    </div>
                    <div class="border-t border-ink/15 pt-6">
                        <div class="font-serif text-4xl text-taupe">03</div>
                        <h3 class="font-serif text-2xl mt-4">Return</h3>
                        <p class="mt-2 text-sm leading-6 text-ink/55">Come back later and rediscover the person you were on that page.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- CTA -->
        <section class="px-6 pb-24">
            <div class="max-w-7xl mx-auto rounded-[36px] bg-ink text-cream px-8 sm:px-14 py-16 sm:py-20 flex flex-col lg:flex-row justify-between lg:items-center gap-10 overflow-hidden relative">
                <div class="absolute -right-16 -top-16 w-72 h-72 rounded-full border border-white/10"></div>
                <div class="absolute -right-4 -top-4 w-44 h-44 rounded-full border border-white/10"></div>
                <div class="relative max-w-2xl">
                    <span class="text-[11px] tracking-[0.28em] uppercase text-white/45">Start your Ilume ritual</span>
                    <h2 class="font-serif text-5xl sm:text-6xl mt-4">Your next chapter deserves a beautiful beginning.</h2>
                </div>
                <button onclick="openOrder()" class="relative shrink-0 rounded-full bg-cream text-ink px-8 py-4 text-xs tracking-[0.18em] uppercase hover:bg-white transition">
                    Place an order
                </button>
            </div>
        </section>
    </main>

    <footer class="border-t border-ink/10 px-6 py-10">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row gap-5 md:items-center md:justify-between text-xs text-ink/50">
            <div class="font-serif text-2xl tracking-[0.16em] text-ink lowercase">ilume</div>
            <div>Journals for a beautifully lived life.</div>
            <div>&copy; {{ year }} Ilume. All rights reserved.</div>
        </div>
    </footer>

    <!-- ORDER MODAL -->
    <div id="orderModal" class="fixed inset-0 z-[80] hidden">
        <div class="absolute inset-0 bg-ink/45 backdrop-blur-sm" onclick="closeOrder()"></div>

        <div class="absolute inset-y-0 right-0 w-full sm:max-w-xl bg-cream shadow-2xl overflow-y-auto">
            <div class="p-7 sm:p-10">
                <div class="flex items-center justify-between">
                    <div>
                        <span class="text-[10px] tracking-[0.26em] uppercase text-ink/45">Ilume order</span>
                        <h2 class="font-serif text-4xl mt-1">Make it yours.</h2>
                    </div>
                    <button onclick="closeOrder()" class="w-10 h-10 rounded-full border border-ink/15 text-xl">&times;</button>
                </div>

                <form id="orderForm" class="mt-9 space-y-5">
                    <div>
                        <label class="text-xs uppercase tracking-[0.15em] text-ink/55">Journal</label>
                        <select id="product" name="product" required class="mt-2 w-full bg-white/55 border border-ink/10 rounded-2xl px-4 py-4">
                            {% for product in products %}
                            <option value="{{ product.id }}">{{ product.name }} — LKR {{ "{:,}".format(product.price) }}</option>
                            {% endfor %}
                        </select>
                    </div>

                    <div class="grid sm:grid-cols-2 gap-4">
                        <div>
                            <label class="text-xs uppercase tracking-[0.15em] text-ink/55">Quantity</label>
                            <input name="quantity" type="number" min="1" max="10" value="1" required class="mt-2 w-full bg-white/55 border border-ink/10 rounded-2xl px-4 py-4">
                        </div>
                        <div>
                            <label class="text-xs uppercase tracking-[0.15em] text-ink/55">Name</label>
                            <input name="name" type="text" required placeholder="Your name" class="mt-2 w-full bg-white/55 border border-ink/10 rounded-2xl px-4 py-4">
                        </div>
                    </div>

                    <div>
                        <label class="text-xs uppercase tracking-[0.15em] text-ink/55">Email</label>
                        <input name="email" type="email" required placeholder="you@example.com" class="mt-2 w-full bg-white/55 border border-ink/10 rounded-2xl px-4 py-4">
                    </div>

                    <div>
                        <label class="text-xs uppercase tracking-[0.15em] text-ink/55">Phone</label>
                        <input name="phone" type="tel" required placeholder="+94 7X XXX XXXX" class="mt-2 w-full bg-white/55 border border-ink/10 rounded-2xl px-4 py-4">
                    </div>

                    <div>
                        <label class="text-xs uppercase tracking-[0.15em] text-ink/55">Delivery address</label>
                        <textarea name="address" rows="4" required placeholder="Street, city, postal code" class="mt-2 w-full bg-white/55 border border-ink/10 rounded-2xl px-4 py-4 resize-none"></textarea>
                    </div>

                    <div>
                        <label class="text-xs uppercase tracking-[0.15em] text-ink/55">A note for us <span class="normal-case tracking-normal">(optional)</span></label>
                        <textarea name="note" rows="3" placeholder="Gift note, delivery preference..." class="mt-2 w-full bg-white/55 border border-ink/10 rounded-2xl px-4 py-4 resize-none"></textarea>
                    </div>

                    <button type="submit" class="w-full rounded-full bg-ink text-cream px-7 py-4 text-xs tracking-[0.18em] uppercase hover:opacity-90 transition">
                        Confirm order
                    </button>

                    <p class="text-[11px] leading-5 text-ink/45 text-center">
                        Demo checkout: orders are accepted by the Flask backend. Connect this endpoint to your database/payment gateway for production.
                    </p>
                </form>

                <div id="successBox" class="hidden mt-12 bg-white/50 rounded-3xl p-8 text-center border border-ink/10">
                    <div class="font-serif text-4xl">Thank you.</div>
                    <p class="mt-3 text-sm leading-6 text-ink/60">Your Ilume order has been received.</p>
                    <p id="orderNumber" class="mt-4 text-xs tracking-[0.16em] uppercase"></p>
                    <button onclick="closeOrder()" class="mt-7 rounded-full border border-ink/15 px-6 py-3 text-xs tracking-[0.15em] uppercase">Continue browsing</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        function openOrder(productId) {
            const modal = document.getElementById('orderModal');
            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';

            if (productId) {
                document.getElementById('product').value = productId;
            }
        }

        function closeOrder() {
            document.getElementById('orderModal').classList.add('hidden');
            document.body.style.overflow = '';
            document.getElementById('orderForm').classList.remove('hidden');
            document.getElementById('successBox').classList.add('hidden');
        }

        document.getElementById('orderForm').addEventListener('submit', async function(event) {
            event.preventDefault();
            const formData = Object.fromEntries(new FormData(event.target).entries());

            const button = event.target.querySelector('button[type="submit"]');
            const originalText = button.textContent;
            button.disabled = true;
            button.textContent = 'Placing order...';

            try {
                const response = await fetch('/api/order', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(formData)
                });

                const data = await response.json();

                if (!response.ok) throw new Error(data.message || 'Unable to place order');

                document.getElementById('orderForm').classList.add('hidden');
                document.getElementById('successBox').classList.remove('hidden');
                document.getElementById('orderNumber').textContent = 'Order ' + data.order_id;
                event.target.reset();
            } catch (error) {
                alert(error.message);
            } finally {
                button.disabled = false;
                button.textContent = originalText;
            }
        });
    </script>
</body>
</html>
"""

@application.route("/")
def home():
    return render_template_string(
        HTML_TEMPLATE,
        products=PRODUCTS,
        year=datetime.now().year
    )

@application.route("/api/order", methods=["POST"])
def place_order():
    data = request.get_json(silent=True) or {}

    required_fields = ["product", "quantity", "name", "email", "phone", "address"]
    missing = [field for field in required_fields if not str(data.get(field, "")).strip()]

    if missing:
        return jsonify({
            "success": False,
            "message": "Please complete all required fields."
        }), 400

    selected_product = next((p for p in PRODUCTS if p["id"] == data["product"]), None)
    if not selected_product:
        return jsonify({
            "success": False,
            "message": "Selected journal was not found."
        }), 400

    try:
        quantity = int(data["quantity"])
        if quantity < 1 or quantity > 10:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "message": "Quantity must be between 1 and 10."
        }), 400

    order_id = "IL-" + uuid.uuid4().hex[:8].upper()
    total = selected_product["price"] * quantity

    # Production note:
    # Save the order to a database and integrate your payment gateway here.
    print({
        "order_id": order_id,
        "product": selected_product["name"],
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
        "message": "Your Ilume order has been received."
    }), 201

@application.route("/health")
def health_check():
    return jsonify({
        "status": "ok",
        "service": "ilume-store",
        "timestamp_utc": datetime.utcnow().isoformat() + "Z"
    }), 200

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000, debug=True)
