import sys
import re

html_file = 'index.html'

try:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"Error: {html_file} not found.")
    sys.exit(1)

# 1. Flip the specific card background token to glassmorphism
content = content.replace("--token-0ed94250-d537-41c9-bd02-bb402916bf2c, rgb(255, 255, 255)", "--token-0ed94250-d537-41c9-bd02-bb402916bf2c, rgba(255, 255, 255, 0.03)")
content = content.replace("--token-0ed94250-d537-41c9-bd02-bb402916bf2c, #fff", "--token-0ed94250-d537-41c9-bd02-bb402916bf2c, rgba(255, 255, 255, 0.03)")
content = content.replace("--token-0ed94250-d537-41c9-bd02-bb402916bf2c:#fff", "--token-0ed94250-d537-41c9-bd02-bb402916bf2c:rgba(255,255,255,0.03)")

# 2. Add backdrop-filter to all divs to ensure glassmorphism blur works!
glass_css = """
<style>
  /* Force blur on glassmorphism tokens */
  * {
    --token-0ed94250-d537-41c9-bd02-bb402916bf2c: rgba(255, 255, 255, 0.03) !important;
  }
  /* Target common Framer card containers and force blur */
  div[style*="background-color: rgba(255, 255, 255, 0.03)"],
  div[style*="background-color: var(--token-0ed94250"],
  div[style*="background-color:var(--token-0ed94250"] {
      backdrop-filter: blur(40px) !important;
      -webkit-backdrop-filter: blur(40px) !important;
      border: 1px solid rgba(255, 255, 255, 0.08) !important;
  }
</style>
"""
if "</head>" in content:
    content = content.replace("</head>", glass_css + "</head>")

# 3. Standard color flips
replacements = {
    # Inline white backgrounds to glassmorphism
    "background-color:rgb(255, 255, 255)": "background-color:rgba(255, 255, 255, 0.03); backdrop-filter:blur(40px); border:1px solid rgba(255,255,255,0.08)",
    "background-color: rgb(255, 255, 255)": "background-color:rgba(255, 255, 255, 0.03); backdrop-filter:blur(40px); border:1px solid rgba(255,255,255,0.08)",
    "background-color:#fff": "background-color:rgba(255, 255, 255, 0.03); backdrop-filter:blur(40px); border:1px solid rgba(255,255,255,0.08)",
    "background-color: #fff": "background-color:rgba(255, 255, 255, 0.03); backdrop-filter:blur(40px); border:1px solid rgba(255,255,255,0.08)",
    "background-color:#ffffff": "background-color:rgba(255, 255, 255, 0.03); backdrop-filter:blur(40px); border:1px solid rgba(255,255,255,0.08)",
    "background-color: #ffffff": "background-color:rgba(255, 255, 255, 0.03); backdrop-filter:blur(40px); border:1px solid rgba(255,255,255,0.08)",

    # Backgrounds
    "rgb(220, 220, 220)": "rgb(11, 11, 11)",
    "#dcdcdc": "#0b0b0b",
    
    # Secondary Backgrounds
    "rgb(240, 240, 240)": "rgba(255, 255, 255, 0.03)",
    "#f0f0f0": "rgba(255, 255, 255, 0.03)",
    
    # Primary Text
    "rgb(19, 19, 19)": "rgb(255, 255, 255)",
    "#131313": "#ffffff",
    "rgb(0, 0, 0)": "rgb(255, 255, 255)",
    "#000000": "#ffffff",
    
    # Secondary Text
    "rgb(92, 92, 92)": "rgb(136, 136, 136)",
    "#5c5c5c": "#888888",
    
    # Agero Orange -> Skillora Blue
    "rgb(255, 77, 0)": "rgb(0, 85, 255)",
    "#ff4d00": "#0055ff",
    "#FF4D00": "#0055ff",
}

for old, new in replacements.items():
    content = content.replace(old, new)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Dark mode glassmorphism applied successfully.")
