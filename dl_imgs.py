import urllib.request, os

dest = r'C:\Users\Noman Traders\.gemini\antigravity\scratch\skillora website\public\images'
os.makedirs(dest, exist_ok=True)

# Try Wayback Machine CDX API to find archived versions
archive_base = 'https://web.archive.org/web/20260101000000*/'

imgs = {
    'logo.png':   'https://skilloraofficial.com/wp-content/uploads/2023/04/Untitled-design-33-scaled.png',
    'work-1.png': 'https://skilloraofficial.com/wp-content/uploads/2026/01/1-1024x1024.png',
    'work-2.png': 'https://skilloraofficial.com/wp-content/uploads/2026/01/2-1024x1024.png',
    'work-3.png': 'https://skilloraofficial.com/wp-content/uploads/2026/01/3-1024x1024.png',
    'work-4.png': 'https://skilloraofficial.com/wp-content/uploads/2026/01/4-1024x1024.png',
    'work-7.png': 'https://skilloraofficial.com/wp-content/uploads/2026/01/7-1024x1024.png',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36',
}

for fname, orig_url in imgs.items():
    # Try Wayback Machine
    wb_url = f'https://web.archive.org/web/2026/{orig_url}'
    out = os.path.join(dest, fname)
    req = urllib.request.Request(wb_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            data = r.read()
        with open(out, 'wb') as f:
            f.write(data)
        print(f'OK {fname} from Wayback ({len(data)} bytes)')
    except Exception as e:
        print(f'FAIL {fname} via Wayback: {e}')
