import requests, re
text=requests.get('https://www.burnkitsdk.xyz/', headers={'User-Agent': 'Mozilla/5.0'}).text
print(set(re.findall(r'(/_next/static/[^"\']+)', text)))
