import sys

html_file = 'framer_clone.html'
out_file = 'index.html'

try:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"Error: {html_file} not found.")
    sys.exit(1)

# The optimized aurora canvas HTML
canvas_html = """
<!-- SKILLORA AURORA CANVAS (60FPS OPTIMIZED) -->
<canvas id="aurora" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 1; pointer-events: none; mix-blend-mode: screen; will-change: transform;"></canvas>
<script>
  window.addEventListener('load', function() {
      const canvas = document.getElementById('aurora');
      if (canvas) {
        const ctx = canvas.getContext('2d', { alpha: true, desynchronized: true });
        let W, H, mouseX = -9999, mouseY = -9999;
        const GAP = 32;
        const DOT_R = 1.2;
        const GLOW_R = 180;
        const BASE_ALPHA = 0.1;

        function resize() {
          const dpr = window.devicePixelRatio || 1;
          W = window.innerWidth;
          H = window.innerHeight;
          canvas.width = W * dpr;
          canvas.height = H * dpr;
          ctx.scale(dpr, dpr);
        }
        resize();
        window.addEventListener('resize', resize, { passive: true });
        window.addEventListener('mousemove', e => { mouseX = e.clientX; mouseY = e.clientY; }, { passive: true });
        window.addEventListener('mouseleave', () => { mouseX = -9999; mouseY = -9999; }, { passive: true });

        // Touch support for mobile interaction
        window.addEventListener('touchmove', e => {
            mouseX = e.touches[0].clientX;
            mouseY = e.touches[0].clientY;
        }, { passive: true });
        window.addEventListener('touchend', () => { mouseX = -9999; mouseY = -9999; }, { passive: true });

        function drawGrid() {
          ctx.clearRect(0, 0, W, H);
          const cols = Math.ceil(W / GAP) + 1;
          const rows = Math.ceil(H / GAP) + 1;
          const offsetX = (W % GAP) / 2;
          const offsetY = (H % GAP) / 2;
          
          let currentMouseX = mouseX;
          let currentMouseY = mouseY;
          const isMobile = W <= 768;
          
          // READ DOM ONLY ONCE PER FRAME TO PREVENT LAYOUT THRASHING
          if (isMobile && mouseX === -9999) {
             const scrollMax = Math.max(1, document.body.scrollHeight - H);
             const scrollP = window.scrollY / scrollMax;
             currentMouseY = scrollP * H;
          }

          for (let row = 0; row < rows; row++) {
            for (let col = 0; col < cols; col++) {
              const x = offsetX + col * GAP;
              const y = offsetY + row * GAP;
              
              let dist;
              if (isMobile && mouseX === -9999) {
                 // Mobile auto-scroll line glow
                 dist = Math.abs(y - currentMouseY);
              } else {
                 // Desktop or active touch glow
                 const dx = x - currentMouseX;
                 const dy = y - currentMouseY;
                 dist = Math.sqrt(dx * dx + dy * dy);
              }

              let alpha = BASE_ALPHA;
              let radius = DOT_R;
              let r = 255;
              let g = 255;
              let b = 255;

              if (dist < GLOW_R) {
                const t = 1 - dist / GLOW_R;
                // Faster ease function
                const ease = t * t * (3 - 2 * t);
                alpha = BASE_ALPHA + ease * 0.7;
                radius = DOT_R + ease * 1.2;
                
                r = 255 - Math.floor(ease * 255);
                g = 255 - Math.floor(ease * 170);
              }

              // Use fillRect instead of arc for massive performance boost
              ctx.fillStyle = `rgba(${r},${g},${b},${alpha})`;
              ctx.fillRect(x - radius, y - radius, radius * 2, radius * 2);
            }
          }
        }
        function animate() {
          drawGrid();
          requestAnimationFrame(animate);
        }
        requestAnimationFrame(animate);
      }
  });
</script>
</body>
"""

if "</body>" in content:
    content = content.replace("</body>", canvas_html)
else:
    content += canvas_html

with open(out_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Injected optimized 60fps aurora and saved to index.html")
