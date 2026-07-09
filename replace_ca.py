import os

target_dir = r"c:\Tools\project crypto\burntoolkit"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return # Skip binary files

    new_content = content.replace('2uSMmnzoGh5jV48hp5Zyh3jHzMbpKPMpcMYP5ipEpump', 'coming soon on pump.fun')
    
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

print("CA replaced!")
