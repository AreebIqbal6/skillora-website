content = open('index.html', encoding='utf-8').read()
# Check position 890327 - this should be in the body HTML
idx = 890327
print(repr(content[idx-200:idx+600]))
