import re

content = open(r'C:\Users\Noman Traders\.gemini\antigravity\brain\ddb5f484-14d4-4232-81c4-935d633885ec\.system_generated\steps\2162\content.md', encoding='utf-8').read()
imgs = re.findall(r'https://skilloraofficial\.com/wp-content/uploads/[^\s\"\')\]]+', content)
for i in sorted(set(imgs)):
    print(i)
