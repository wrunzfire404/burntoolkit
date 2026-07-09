import os
import requests
import re
import concurrent.futures
import shutil

url_base = "https://www.burnkitsdk.xyz/"
target_dir = r"c:\Tools\project crypto\burntoolkit"
public_dir = os.path.join(target_dir, "public")
assets_dir = os.path.join(public_dir, "assets")

if os.path.exists(assets_dir):
    shutil.rmtree(assets_dir)
os.makedirs(assets_dir)

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

print("Downloading index.html...")
res = session.get(url_base)
res.raise_for_status()
html_content = res.text

# Find index JS and CSS
js_match = re.search(r'src="(/assets/index-[a-zA-Z0-9_-]+\.js)"', html_content)
css_match = re.search(r'href="(/assets/index-[a-zA-Z0-9_-]+\.css)"', html_content)

main_js_path = js_match.group(1) if js_match else None
main_css_path = css_match.group(1) if css_match else None

matches = set()
if main_js_path:
    print(f"Downloading main JS: {main_js_path}")
    main_js_content = session.get(url_base.rstrip('/') + main_js_path).text
    matches.update(re.findall(r'([a-zA-Z0-9_-]+\.(?:js|css))', main_js_content))
    matches.add(main_js_path.replace('/assets/', ''))
    
if main_css_path:
    print(f"Downloading main CSS: {main_css_path}")
    main_css_content = session.get(url_base.rstrip('/') + main_css_path).text
    matches.update(re.findall(r'([a-zA-Z0-9_-]+\.(?:woff2|woff|ttf|png|svg|jpg))', main_css_content))
    matches.add(main_css_path.replace('/assets/', ''))

def process_content(file_content):
    if not isinstance(file_content, str):
        return file_content
    # Name replacements
    file_content = file_content.replace("BurnKit SDK", "BurnToolkit")
    file_content = file_content.replace("BurnKitSdk", "BurnToolkit")
    file_content = file_content.replace("BurnKit", "BurnToolkit")
    file_content = file_content.replace("burnkitsdk", "burntoolkit")
    
    # Twitter replacement
    file_content = re.sub(r'https://(?:www\.)?(?:twitter|x)\.com/[^\s"\'<>]+', 'https://x.com/burntoolkit', file_content)
    
    # Lovable traces
    file_content = re.sub(r'lovable-badge[^"\'>]*', '', file_content, flags=re.IGNORECASE)
    file_content = re.sub(r'Made with Lovable', 'Made with ❤️', file_content, flags=re.IGNORECASE)
    
    # Absolute paths for root images to prevent 404
    images = re.findall(r'["\'](/[^"\']+\.(?:png|jpg|jpeg|svg|webp|gif|ico))["\']', file_content)
    for img in set(images):
        file_content = file_content.replace(f'"{img}"', f'"https://www.burnkitsdk.xyz{img}"')
        file_content = file_content.replace(f"'{img}'", f"'https://www.burnkitsdk.xyz{img}'")
        
    return file_content

def download_and_process(filename):
    file_url = url_base.rstrip('/') + '/assets/' + filename
    r = session.get(file_url)
    
    if r.status_code == 200 and not r.text.startswith('<!DOCTYPE html>'):
        if filename.endswith(".js") or filename.endswith(".css"):
            file_content = process_content(r.text)
            with open(os.path.join(assets_dir, filename), "w", encoding="utf-8") as f:
                f.write(file_content)
        else:
            with open(os.path.join(assets_dir, filename), "wb") as f:
                f.write(r.content)
        print(f"Downloaded chunk: {filename}")
        return True
    return False

print(f"Downloading {len(matches)} chunks...")
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(download_and_process, filename) for filename in matches]
    concurrent.futures.wait(futures)

# Process HTML
html_content = process_content(html_content)

with open(os.path.join(target_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print("Full scrape completed!")
