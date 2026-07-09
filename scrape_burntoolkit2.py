import os
import requests
import re
import concurrent.futures
import shutil

url_base = "https://www.burnkitsdk.xyz/"
target_dir = r"c:\Tools\project crypto\burntoolkit"
public_dir = os.path.join(target_dir, "public")

if os.path.exists(public_dir):
    shutil.rmtree(public_dir)
os.makedirs(public_dir)

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

print("Downloading index.html...")
res = session.get(url_base)
res.raise_for_status()
html_content = res.text

# Find all _next and asset paths in HTML
matches = set(re.findall(r'(/_next/[a-zA-Z0-9_./-]+(?:\?[a-zA-Z0-9_=]+)?)', html_content))
images = set(re.findall(r'(/[^"\'<>]+(?:\.png|\.jpg|\.jpeg|\.svg|\.webp|\.gif|\.ico))', html_content))
matches.update(images)

def process_content(file_content):
    if not isinstance(file_content, str):
        return file_content
    # Name replacements
    file_content = file_content.replace("BurnKit SDK", "BurnToolkit")
    file_content = file_content.replace("BurnKitSdk", "BurnToolkit")
    file_content = file_content.replace("BurnKit", "BurnToolkit")
    file_content = file_content.replace("burnkitsdk", "burntoolkit")
    file_content = file_content.replace("Burnkit", "Burntoolkit")
    
    # Twitter replacement
    file_content = re.sub(r'https://(?:www\.)?(?:twitter|x)\.com/[^\s"\'<>\\]+', 'https://x.com/burntoolkit', file_content)
    
    # Lovable traces (just in case)
    file_content = re.sub(r'lovable-badge[^"\'>]*', '', file_content, flags=re.IGNORECASE)
    file_content = re.sub(r'Made with Lovable', 'Made with ❤️', file_content, flags=re.IGNORECASE)
    
    # Let's fix relative _next paths for Vercel
    # We will just host it exactly as it is (in /_next/... directories in public folder)
    return file_content

def download_and_process(path):
    # Remove query string for local saving
    local_path = path.split('?')[0]
    
    file_url = url_base.rstrip('/') + path
    r = session.get(file_url)
    
    if r.status_code == 200 and not r.text.startswith('<!DOCTYPE html>'):
        is_text = False
        if local_path.endswith(".js") or local_path.endswith(".css"):
            is_text = True
        
        save_path = os.path.join(public_dir, local_path.lstrip('/'))
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        if is_text:
            file_content = process_content(r.text)
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(file_content)
            
            # Find more matches inside the CSS/JS
            new_matches = set(re.findall(r'(/_next/[a-zA-Z0-9_./-]+(?:\?[a-zA-Z0-9_=]+)?)', file_content))
            return new_matches
        else:
            with open(save_path, "wb") as f:
                f.write(r.content)
            return set()
    return set()

print(f"Downloading {len(matches)} chunks...")
processed = set()
to_process = set(matches)

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    while to_process:
        batch = list(to_process - processed)
        to_process.clear()
        processed.update(batch)
        
        if not batch:
            break
            
        futures = [executor.submit(download_and_process, p) for p in batch]
        for future in concurrent.futures.as_completed(futures):
            new_matches = future.result()
            to_process.update(new_matches - processed)

# Process HTML
html_content = process_content(html_content)

with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Full scrape completed!")
