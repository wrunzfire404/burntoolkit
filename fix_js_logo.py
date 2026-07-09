import re
filepath = r'public/_next/static/chunks/328-34a6e55955c198ce.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

new_content = re.sub(
    r'\([0-9]+,[a-zA-Z0-9_.]+\)\([a-zA-Z0-9_.]+,{src:"/logo\.png"',
    lambda m: m.group(0).split(')(')[0] + ')("img",{src:"/logo.png"',
    content
)

if new_content != content:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Fixed JS logo!")
else:
    print("No change needed.")
