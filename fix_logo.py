import os
import re

target_dir = r"c:\Tools\project crypto\burntoolkit"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return # Skip binary files

    # Replace Next.js Image component usage for logo with native <img>
    # (0,a.jsx)(s.default,{src:"/logo.png" -> (0,a.jsx)("img",{src:"/logo.png"
    new_content = re.sub(r'\([a-zA-Z0-9_.]+\)\([a-zA-Z0-9_.]+,{src:"/logo\.png"', lambda m: m.group(0).split(')(')[0] + ')("img",{src:"/logo.png"', content)
    
    # Also fix it in index.html where it's serialized
    # Replace /_next/image?url=%2Flogo.png&amp;w=32&amp;q=75 with /logo.png
    new_content = re.sub(r'/_next/image\?url=%2Flogo\.png(?:&amp;|&)w=\d+(?:&amp;|&)q=\d+', '/logo.png', new_content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

process_file(os.path.join(target_dir, "index.html"))

public_dir = os.path.join(target_dir, "public")
for root, dirs, files in os.walk(public_dir):
    for file in files:
        if file.endswith(('.js', '.css', '.html')):
            process_file(os.path.join(root, file))

print("Logo fixed!")
