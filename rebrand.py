import sys

html_file = 'index.html'

try:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"Error: {html_file} not found.")
    sys.exit(1)

# Specific Replacements
content = content.replace("franklin@agero.com", "info@skilloraofficial.com")
content = content.replace('franklin<span class="framer-text"', 'info<span class="framer-text"')
content = content.replace("agero.com", "skilloraofficial.com")

# SEO Replacements
content = content.replace("Agero - Modern Portfolio &amp; Creative Agency Framer Template", "Skillora - Senior Web &amp; Mobile Development")
content = content.replace("Agero is a sleek and minimal portfolio", "Skillora provides premium web and mobile development")

# General Replacements
content = content.replace("Agero", "Skillora")
content = content.replace("agero", "skillora")

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Rebranded index.html successfully.")
