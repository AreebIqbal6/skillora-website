import sys
import re

html_file = 'index.html'

try:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"Error: {html_file} not found.")
    sys.exit(1)

# ====================================================
# STEP 1: Fix the Framer CSS token block in the <style>
# The framer CSS block sets all variables in body{}
# We need to update those to our dark/blue palette
# ====================================================

# The key token variables in the body{} block need correct values
# Replace the body token block with our Skillora palette
token_fixes = [
    # Background tokens
    ('--token-79a6bc92-0037-43aa-add7-96dca20830ea:#0b0b0b', '--token-79a6bc92-0037-43aa-add7-96dca20830ea:#060610'),
    # Text color - main (currently #fff - good)
    # Text color secondary
    ('--token-23bf38ef-7d86-447a-9b72-58d35e71b182:#888', '--token-23bf38ef-7d86-447a-9b72-58d35e71b182:#666888'),
    # Card bg glass
    ('--token-0ed94250-d537-41c9-bd02-bb402916bf2c:rgba(255,255,255,0.03)', '--token-0ed94250-d537-41c9-bd02-bb402916bf2c:rgba(0,50,255,0.06)'),
    # Secondary background (nav etc)
    ('--token-8724acf4-60a3-4686-b4b9-c5e36bef17c0:#0b0b0b', '--token-8724acf4-60a3-4686-b4b9-c5e36bef17c0:rgba(6,6,16,0.85)'),
    # Accent color (orange replaced by blue)
    ('--token-3bec1af9-cd4c-4fff-9125-924324e26d0b:#05f', '--token-3bec1af9-cd4c-4fff-9125-924324e26d0b:#2563ff'),
    # Button bg
    ('--token-05f35d53-b2c8-4da9-9daf-3ee4dbb2014e:#05f', '--token-05f35d53-b2c8-4da9-9daf-3ee4dbb2014e:#2563ff'),
    # dark overlay
    ('--token-ac88bdb2-3c45-418b-8250-5746da7a4cc4:#000', '--token-ac88bdb2-3c45-418b-8250-5746da7a4cc4:#060610'),
]

for old, new in token_fixes:
    content = content.replace(old, new)

# ====================================================
# STEP 2: Inject a master override <style> block LAST in <head>
# This wins specificity wars over all Framer styles
# ====================================================

skillora_override = """
<style id="skillora-override">
  /* ===== SKILLORA DARK THEME OVERRIDE ===== */
  
  /* Global page background */
  html, body, #main {
    background: #060610 !important;
  }
  
  /* Root page wrapper */
  .framer-TqF0O.framer-1m4s77b,
  .framer-TqF0O.framer-4l4qfv,
  .framer-TqF0O.framer-oysice {
    background-color: #060610 !important;
  }

  /* ---- AURORA GLOW BACKGROUND ---- */
  .framer-wec74e {
    background: radial-gradient(ellipse 80% 60% at 20% 20%, rgba(0,85,255,0.18) 0%, transparent 60%),
                radial-gradient(ellipse 70% 50% at 80% 80%, rgba(100,0,255,0.12) 0%, transparent 60%),
                radial-gradient(ellipse 60% 40% at 50% 50%, rgba(0,30,120,0.08) 0%, transparent 70%),
                #060610 !important;
  }

  /* ---- NAVIGATION ---- */
  header.framer-1vb53dl,
  header.framer-JIjAQ {
    background: rgba(6,6,16,0.7) !important;
    backdrop-filter: blur(24px) saturate(1.8) !important;
    -webkit-backdrop-filter: blur(24px) saturate(1.8) !important;
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
  }
  
  /* Nav bar pill */
  nav.framer-cxdqtj {
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 100px !important;
  }

  /* ---- AVAILABILITY NOTCH ---- */
  .framer-1n7k6km {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 100px !important;
  }

  /* ---- ALL GLASS CARDS ---- */
  /* Target the main section containers */
  .framer-Je19z > section,
  .framer-Je19z > div > section {
    position: relative;
  }

  /* Card-like containers – service cards, work cards, testimonial cards */
  [class*="framer-"] [data-border="true"],
  [class*="framer-"][data-border="true"] {
    border-color: rgba(255,255,255,0.08) !important;
  }

  /* Force white text where black was set inline */
  [style*="color:rgb(19, 19, 19)"],
  [style*="color: rgb(19, 19, 19)"],
  [style*="color:#131313"],
  [style*="color: #131313"] {
    color: #ffffff !important;
  }

  /* Force gray subtext */
  [style*="color:rgb(92, 92, 92)"],
  [style*="color: rgb(92, 92, 92)"],
  [style*="color:#5c5c5c"],
  [style*="color:#888888"],
  [style*="color: #888888"] {
    color: #8892b0 !important;
  }

  /* ---- HERO SECTION ---- */
  section#hero,
  .framer-1bclbgn {
    position: relative;
    z-index: 2;
  }
  
  /* Hero heading text */
  section#hero h1.framer-text,
  .framer-1bclbgn h1.framer-text {
    background: linear-gradient(135deg, #ffffff 0%, #a0b4ff 60%, #6685ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* ---- CTA BUTTONS ---- */
  a[style*="background-color:rgb(0, 85, 255)"],
  a[style*="background-color: rgb(0, 85, 255)"],
  a[style*="background-color:#0055ff"],
  a[style*="background-color: #0055ff"] {
    background: linear-gradient(135deg, #2563ff, #7c3aed) !important;
    box-shadow: 0 0 40px rgba(37,99,255,0.4), 0 8px 32px rgba(0,0,0,0.4) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    transition: box-shadow 0.3s ease, transform 0.2s ease !important;
  }
  a[style*="background-color:rgb(0, 85, 255)"]:hover,
  a[style*="background-color: rgb(0, 85, 255)"]:hover,
  a[style*="background-color:#0055ff"]:hover {
    box-shadow: 0 0 60px rgba(37,99,255,0.6), 0 12px 40px rgba(0,0,0,0.5) !important;
    transform: translateY(-1px) !important;
  }

  /* ---- WHITE/LIGHT BG CARDS → GLASS ---- */
  [style*="background-color:rgba(255, 255, 255, 0.03)"],
  [style*="background-color: rgba(255, 255, 255, 0.03)"],
  [style*="background-color:rgba(255,255,255,0.03)"] {
    background: rgba(15, 20, 60, 0.4) !important;
    backdrop-filter: blur(20px) saturate(1.5) !important;
    -webkit-backdrop-filter: blur(20px) saturate(1.5) !important;
    border: 1px solid rgba(100, 130, 255, 0.15) !important;
    border-radius: 16px;
  }

  /* Kill any remaining white backgrounds */
  [style*="background-color:rgb(255, 255, 255)"],
  [style*="background-color: rgb(255, 255, 255)"],
  [style*="background-color:#ffffff"],
  [style*="background-color: #ffffff"],
  [style*="background-color:#fff"],
  [style*="background-color: #fff"] {
    background-color: rgba(15, 20, 60, 0.4) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(100, 130, 255, 0.15) !important;
  }

  /* Kill light gray backgrounds */
  [style*="background-color:rgb(240, 240, 240)"],
  [style*="background-color: rgb(240, 240, 240)"],
  [style*="background-color:#f0f0f0"],
  [style*="background-color:rgb(220, 220, 220)"],
  [style*="background-color: rgb(220, 220, 220)"],
  [style*="background-color:#dcdcdc"] {
    background-color: rgba(15, 20, 60, 0.3) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
  }

  /* ---- TICKER / MARQUEE STRIP ---- */
  .framer-nv5Gc,
  [class*="framer-"][class*="anhk9k"] {
    background: rgba(10, 14, 50, 0.6) !important;
    border-top: 1px solid rgba(100,130,255,0.12) !important;
    border-bottom: 1px solid rgba(100,130,255,0.12) !important;
  }

  /* Ticker text */
  .framer-nv5Gc p,
  .framer-nv5Gc span {
    color: #8892b0 !important;
  }

  /* ---- SECTION SEPARATORS ---- */
  hr, [class*="divider"] {
    border-color: rgba(255,255,255,0.06) !important;
  }

  /* ---- FAQ ITEMS ---- */
  .framer-DIoSH,
  .framer-hMZdx,
  .framer-NWaN7,
  [class*="framer-"][class*="faq"] {
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
  }

  /* ---- FOOTER ---- */
  .framer-d1bq8h,
  footer {
    background: #040408 !important;
    border-top: 1px solid rgba(100,130,255,0.1) !important;
  }

  /* ---- BLUE ACCENT COLORS (scrolling ticker dot, underlines) ---- */
  [style*="background-color:rgb(0, 85, 255)"],
  [style*="background-color: rgb(0, 85, 255)"],
  [style*="background-color:#0055ff"] {
    background-color: #2563ff !important;
  }

  /* ---- MAKE ALL TEXT MATCH DARK MODE ---- */
  .framer-text {
    color: inherit;
  }

  /* Available dot - keep green */
  .framer-jjw234 {
    background-color: #22c55e !important;
    box-shadow: 0 0 8px rgba(34,197,94,0.6) !important;
  }
  
  /* Glow shimmer on service cards on hover */
  .framer-Je19z > * > section > * > *:hover {
    box-shadow: 0 0 60px rgba(37,99,255,0.08) !important;
    border-color: rgba(100,130,255,0.25) !important;
    transition: all 0.3s ease !important;
  }
  
  /* ---- STAT NUMBERS ---- */
  .framer-text[style*="font-size:80px"],
  .framer-text[style*="font-size: 80px"],
  .framer-text[style*="font-size:72px"],
  .framer-text[style*="font-size: 72px"] {
    color: #ffffff !important;
  }

  /* Blue gradient accent line */
  body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #2563ff, #7c3aed, transparent);
    z-index: 9999;
    pointer-events: none;
  }

  /* Subtle radial glow behind hero */
  .framer-1bclbgn::before {
    content: '';
    position: absolute;
    top: -200px;
    left: 50%;
    transform: translateX(-50%);
    width: 800px;
    height: 800px;
    background: radial-gradient(ellipse, rgba(37,99,255,0.12) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }

  /* Prevent the Framer badge from showing */
  #__framer-badge-container {
    display: none !important;
  }
</style>
"""

if "</head>" in content:
    content = content.replace("</head>", skillora_override + "\n</head>")

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Skillora premium dark theme applied successfully.")
