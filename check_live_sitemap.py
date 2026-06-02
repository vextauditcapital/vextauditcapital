import urllib.request

urls = [
    "https://www.vextaudit.com/sitemap.xml",
    "https://vextaudit.com/sitemap.xml"
]

for url in urls:
    print(f"Checking live URL: {url} ...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            length = len(response.read())
            print(f"  SUCCESS: Status={status}, length={length} bytes\n")
    except Exception as e:
        print(f"  FAILED: {e}\n")
