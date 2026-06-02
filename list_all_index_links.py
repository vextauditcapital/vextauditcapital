from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.in_a = False
        self.current_href = ""
        self.current_text = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.in_a = True
            self.current_text = []
            for attr in attrs:
                if attr[0] == "href":
                    self.current_href = attr[1]

    def handle_endtag(self, tag):
        if tag == "a" and self.in_a:
            text = "".join(self.current_text).strip()
            self.links.append((self.current_href, text))
            self.in_a = False

    def handle_data(self, data):
        if self.in_a:
            self.current_text.append(data)

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

parser = MyHTMLParser()
parser.feed(content)

print(f"Total links found: {len(parser.links)}")
for i, (href, text) in enumerate(parser.links):
    print(f"{i+1}: href='{href}' text='{text}'")
