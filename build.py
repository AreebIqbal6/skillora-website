"""
SKILLORA MASTER BUILD PIPELINE
Runs in order: rebrand → theme → aurora injection
"""
import sys
import re

# ============================================================
# STEP 1: Load base clone
# ============================================================
try:
    with open('framer_clone.html', 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print("ERROR: framer_clone.html not found.")
    sys.exit(1)

print("[1/4] Loaded framer_clone.html")

# ============================================================
# STEP 2: REBRAND - Agero → Skillora
# ============================================================
content = content.replace("Agero - Modern Portfolio &amp; Creative Agency Framer Template", "Skillora — Senior Web &amp; Mobile Development Agency")
content = content.replace("Agero is a sleek and minimal portfolio", "Skillora is a premium full-stack development agency")
content = content.replace("franklin@agero.com", "info@skilloraofficial.com")
content = content.replace("mailto:franklin@agero.com", "mailto:info@skilloraofficial.com")
# Text content replacement only (not CSS classes)
content = content.replace(">Founder at Agero<", ">Co-Founder at Skillora<")
content = content.replace(">franklin<", ">info<")
content = content.replace("@agero.com<", "@skilloraofficial.com<")
content = content.replace("Agero", "Skillora")
content = content.replace("agero", "skillora")

print("[2/4] Rebranded: Agero -> Skillora")

# ============================================================
# STEP 3: Fix Framer CSS token variable block (body{...})
# These are in a minified inline <style> block
# ============================================================

# Dark background tokens
content = content.replace(
    "--token-79a6bc92-0037-43aa-add7-96dca20830ea,rgb(220,220,220)",
    "--token-79a6bc92-0037-43aa-add7-96dca20830ea,#060610"
)
content = content.replace(
    "--token-79a6bc92-0037-43aa-add7-96dca20830ea,#dcdcdc",
    "--token-79a6bc92-0037-43aa-add7-96dca20830ea,#060610"
)

# In the body{} token shorthand block
body_token_replacements = [
    ("--token-79a6bc92-0037-43aa-add7-96dca20830ea:#dcdcdc;", "--token-79a6bc92-0037-43aa-add7-96dca20830ea:#060610;"),
    ("--token-8724acf4-60a3-4686-b4b9-c5e36bef17c0:#f0f0f0;", "--token-8724acf4-60a3-4686-b4b9-c5e36bef17c0:rgba(6,6,22,0.85);"),
    ("--token-486472f1-4db8-4c0e-a40e-5ea99c9098b9:#131313;", "--token-486472f1-4db8-4c0e-a40e-5ea99c9098b9:#ffffff;"),
    ("--token-23bf38ef-7d86-447a-9b72-58d35e71b182:#5c5c5c;", "--token-23bf38ef-7d86-447a-9b72-58d35e71b182:#8892b0;"),
    ("--token-3bec1af9-cd4c-4fff-9125-924324e26d0b:#ff4d00;", "--token-3bec1af9-cd4c-4fff-9125-924324e26d0b:#2563ff;"),
    ("--token-0ed94250-d537-41c9-bd02-bb402916bf2c:#fff;", "--token-0ed94250-d537-41c9-bd02-bb402916bf2c:rgba(15,25,70,0.4);"),
    ("--token-ac88bdb2-3c45-418b-8250-5746da7a4cc4:#000;", "--token-ac88bdb2-3c45-418b-8250-5746da7a4cc4:#060610;"),
    # Also fix inline style colors
    ("rgb(19, 19, 19)", "rgb(255, 255, 255)"),
    ("rgb(220, 220, 220)", "rgb(6, 6, 16)"),
    ("rgb(240, 240, 240)", "rgba(6, 6, 22, 0.85)"),
    ("rgb(255, 77, 0)", "rgb(37, 99, 255)"),
    ("#ff4d00", "#2563ff"),
    ("#FF4D00", "#2563ff"),
    ("#131313", "#ffffff"),
    ("#5c5c5c", "#8892b0"),
    ("#dcdcdc", "#060610"),
    ("#f0f0f0", "rgba(6,6,22,0.85)"),
]

for old, new in body_token_replacements:
    content = content.replace(old, new)

print("[3/4] Applied dark mode token fixes")

# ============================================================
# STEP 4: Inject master override CSS + Aurora canvas
# ============================================================

skillora_css = """
<style id="skillora-override">
  /* ===== SKILLORA DARK PREMIUM THEME ===== */

  html, body, #main {
    background: #060610 !important;
  }

  /* Page wrapper */
  .framer-TqF0O {
    background-color: #060610 !important;
  }

  /* Top gradient accent line */
  body::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #2563ff 40%, #7c3aed 60%, transparent 100%);
    z-index: 99999;
    pointer-events: none;
  }

  /* Aurora background section */
  .framer-wec74e {
    background:
      radial-gradient(ellipse 90% 60% at 15% 10%, rgba(37,99,255,0.15) 0%, transparent 60%),
      radial-gradient(ellipse 70% 50% at 85% 85%, rgba(124,58,237,0.1) 0%, transparent 60%),
      #060610 !important;
  }

  /* NAVIGATION */
  header.framer-1vb53dl {
    background: rgba(6,6,16,0.75) !important;
    backdrop-filter: blur(32px) saturate(1.8) !important;
    -webkit-backdrop-filter: blur(32px) saturate(1.8) !important;
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
  }

  nav.framer-cxdqtj {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-radius: 100px !important;
  }

  /* Availability notch */
  .framer-1n7k6km {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 100px !important;
  }

  /* Green status dot glow */
  .framer-jjw234 {
    background-color: #22c55e !important;
    box-shadow: 0 0 8px rgba(34,197,94,0.7), 0 0 16px rgba(34,197,94,0.3) !important;
  }

  /* CTAs */
  a[style*="background-color:rgb(0, 85, 255)"],
  a[style*="background-color: rgb(0, 85, 255)"],
  a[style*="background-color:rgb(37, 99, 255)"],
  a[style*="background-color: rgb(37, 99, 255)"] {
    background: linear-gradient(135deg, #2563ff 0%, #7c3aed 100%) !important;
    box-shadow: 0 0 32px rgba(37,99,255,0.35), 0 8px 24px rgba(0,0,0,0.4) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
  }
  a[style*="background-color:rgb(0, 85, 255)"]:hover,
  a[style*="background-color: rgb(0, 85, 255)"]:hover,
  a[style*="background-color:rgb(37, 99, 255)"]:hover {
    box-shadow: 0 0 48px rgba(37,99,255,0.55), 0 12px 32px rgba(0,0,0,0.5) !important;
    transform: translateY(-2px) !important;
  }

  /* Hero section hero text gradient */
  .framer-1bclbgn h1.framer-text {
    background: linear-gradient(120deg, #ffffff 0%, #c8d4ff 50%, #a5b4fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  /* Hero subtle glow */
  .framer-1bclbgn::before {
    content: '';
    position: absolute;
    top: -300px; left: 50%;
    transform: translateX(-50%);
    width: 1000px; height: 800px;
    background: radial-gradient(ellipse, rgba(37,99,255,0.1) 0%, transparent 65%);
    pointer-events: none;
    z-index: 0;
  }

  /* Glass cards — force ALL white bg containers to dark glass */
  [style*="background-color:rgba(255,255,255,0.03)"],
  [style*="background-color: rgba(255, 255, 255, 0.03)"],
  [style*="background-color:rgba(15,25,70,0.4)"],
  [style*="background-color: rgba(15, 25, 70, 0.4)"] {
    background: rgba(8, 14, 50, 0.5) !important;
    backdrop-filter: blur(24px) saturate(1.6) !important;
    -webkit-backdrop-filter: blur(24px) saturate(1.6) !important;
    border: 1px solid rgba(100,130,255,0.12) !important;
    border-radius: 16px !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
  }
  [style*="background-color:rgba(8, 14, 50, 0.5)"]:hover,
  [style*="background-color: rgba(8, 14, 50, 0.5)"]:hover {
    border-color: rgba(100,130,255,0.25) !important;
    box-shadow: 0 0 40px rgba(37,99,255,0.08) !important;
  }

  /* Kill remaining white backgrounds */
  [style*="background-color:rgb(255, 255, 255)"],
  [style*="background-color: rgb(255, 255, 255)"],
  [style*="background-color:#ffffff"],
  [style*="background-color: #ffffff"] {
    background-color: rgba(8, 14, 50, 0.5) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(100,130,255,0.12) !important;
  }

  /* Ticker/marquee strip */
  .framer-nv5Gc {
    background: rgba(8,10,32,0.7) !important;
    border-top: 1px solid rgba(100,130,255,0.1) !important;
    border-bottom: 1px solid rgba(100,130,255,0.1) !important;
  }

  /* Footer */
  .framer-d1bq8h {
    background: #040408 !important;
    border-top: 1px solid rgba(100,130,255,0.08) !important;
  }

  /* data-border elements */
  [data-border="true"]::after {
    border-color: rgba(100,130,255,0.1) !important;
  }

  /* Dark overlays on images */
  [style*="background-color:rgba(0, 0, 0, 0.77)"],
  [style*="background-color: rgba(0, 0, 0, 0.77)"] {
    background-color: rgba(6,6,16,0.8) !important;
  }

  /* Hide Framer badge */
  #__framer-badge-container { display: none !important; }

  /* Scroll indicator line */
  .framer-d1bq8h, .framer-TqF0O .framer-d1bq8h {
    overflow: hidden;
  }
</style>
"""

aurora_js = """
<!-- SKILLORA AURORA DOT GRID (60fps) -->
<canvas id="sk-aurora" style="position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:0;pointer-events:none;mix-blend-mode:screen;" aria-hidden="true"></canvas>
<script>
(function(){
  var canvas = document.getElementById('sk-aurora');
  if(!canvas) return;
  var ctx = canvas.getContext('2d', {alpha:true, desynchronized:true});
  var W, H, mx=-9999, my=-9999;
  var GAP=34, DOT_R=1.2, GLOW_R=200, BASE_A=0.08;
  
  function resize(){
    var dpr = window.devicePixelRatio||1;
    W = window.innerWidth; H = window.innerHeight;
    canvas.width = W*dpr; canvas.height = H*dpr;
    canvas.style.width = W+'px'; canvas.style.height = H+'px';
    ctx.scale(dpr,dpr);
  }
  resize();
  
  window.addEventListener('resize', resize, {passive:true});
  window.addEventListener('mousemove', function(e){ mx=e.clientX; my=e.clientY; }, {passive:true});
  window.addEventListener('mouseleave', function(){ mx=-9999; my=-9999; }, {passive:true});
  window.addEventListener('touchmove', function(e){ mx=e.touches[0].clientX; my=e.touches[0].clientY; }, {passive:true});
  window.addEventListener('touchend', function(){ mx=-9999; my=-9999; }, {passive:true});

  // Smooth lerped mouse
  var lx=mx, ly=my;
  
  function draw(){
    ctx.clearRect(0,0,W,H);
    
    // Smooth lerp
    lx += (mx - lx) * 0.1;
    ly += (my - ly) * 0.1;
    
    var isMobile = W <= 768;
    var cmx = lx, cmy = ly;
    
    if(isMobile && mx===-9999){
      var sp = window.scrollY / Math.max(1, document.body.scrollHeight - H);
      cmy = sp * H;
    }
    
    var cols = Math.ceil(W/GAP)+1;
    var rows = Math.ceil(H/GAP)+1;
    var ox = (W%GAP)/2;
    var oy = (H%GAP)/2;
    
    for(var row=0; row<rows; row++){
      for(var col=0; col<cols; col++){
        var x = ox + col*GAP;
        var y = oy + row*GAP;
        
        var dist;
        if(isMobile && mx===-9999){
          dist = Math.abs(y - cmy);
        } else {
          var dx = x-cmx, dy = y-cmy;
          dist = Math.sqrt(dx*dx+dy*dy);
        }
        
        var a = BASE_A;
        var r = 255, g = 255, b = 255;
        var rad = DOT_R;
        
        if(dist < GLOW_R){
          var t = 1 - dist/GLOW_R;
          var ease = t*t*(3-2*t);
          a = BASE_A + ease*0.65;
          rad = DOT_R + ease*1.4;
          // Blue-purple glow
          r = Math.round(37 + ease*(255-37));
          g = Math.round(99 + ease*(255-99));
          b = 255;
        }
        
        ctx.fillStyle = 'rgba('+r+','+g+','+b+','+a.toFixed(3)+')';
        ctx.fillRect(x-rad, y-rad, rad*2, rad*2);
      }
    }
    requestAnimationFrame(draw);
  }
  requestAnimationFrame(draw);
})();
</script>
</body>
"""

# Inject CSS before </head>
content = content.replace("</head>", skillora_css + "\n</head>")

# Inject aurora before </body>
content = content.replace("</body>", aurora_js)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("[4/4] Injected Skillora CSS theme + Aurora canvas")
print("DONE: Build complete -> index.html")
