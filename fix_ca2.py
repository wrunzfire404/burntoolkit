import os
import glob

files = glob.glob('public/_next/**/*.js', recursive=True) + glob.glob('index.html')

for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    
    if '2uSM…pump' in content:
        new_content = content.replace('2uSM…pump', 'coming soon on pump.fun')
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Fixed {f}")
