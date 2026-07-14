import re

content = open('index.html', encoding='utf-8').read()

# The badge is the framer-fe71dh-container div which contains the badge link
# Find and remove all instances of it from the HTML body
# It appears as <div class="framer-fe71dh-container" ...>...</div>

# Use regex to remove the entire container div
# The pattern wraps from the opening div to its matching close
# Since HTML isn't perfectly parseable with regex for nested divs,
# we'll find the exact string and cut it

# Find all occurrences of framer-fe71dh-container in the body
idx = 890327 - 200  # Start from near the badge HTML

# Find the opening tag
open_tag = 'class="framer-fe71dh-container"'
positions = []
start = 0
while True:
    i = content.find(open_tag, start)
    if i == -1:
        break
    positions.append(i)
    start = i + 1

print(f"Found {len(positions)} badge containers at:", positions)

# For each position, find the full wrapping div and remove it
# Walk backwards to find the <div start
for pos in sorted(positions, reverse=True):
    # Find the start of the <div tag
    div_start = content.rfind('<div', 0, pos)
    
    # Now count nested divs to find the matching close
    depth = 0
    i = div_start
    while i < len(content):
        if content[i:i+4] == '<div':
            depth += 1
            i += 4
        elif content[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                div_end = i + 6
                snippet = content[div_start:div_start+80]
                print(f"Removing from {div_start} to {div_end}: {snippet[:60]}...")
                content = content[:div_start] + content[div_end:]
                break
            i += 6
        else:
            i += 1

# Also remove the "NEW TEMPLATES" text directly as backup
content = content.replace('>NEW TEMPLATES</p>', '></p>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Badge div removed from HTML.")
