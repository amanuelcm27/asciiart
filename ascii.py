import requests
from html.parser import HTMLParser

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_td = False
        self.cells = []

    def handle_starttag(self, tag, attrs):
        if tag == "td":
            self.in_td = True
            self.current_data = ""

    def handle_data(self, data):
        if self.in_td:
            text = data.strip()
            if text:
                self.current_data += text

    def handle_endtag(self, tag):
        if tag == "td" and self.in_td:
            self.in_td = False
            if self.current_data:
                self.cells.append(self.current_data)

def reconstruct_ascii(url):
    html = requests.get(url).text
    parser = TableParser()
    parser.feed(html)

    # Group (x, char, y)
    triples = []
    for i in range(0, len(parser.cells), 3):
        try:
            x = int(parser.cells[i])
            char = parser.cells[i + 1]
            y = int(parser.cells[i + 2])
            triples.append((x, char, y))
        except (ValueError, IndexError):
            continue

    min_x = min(x for x, _, _ in triples)
    min_y = min(y for _, _, y in triples)
    max_x = max(x for x, _, _ in triples)
    max_y = max(y for _, _, y in triples)

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    grid = [[" " for _ in range(width)] for _ in range(height)]

    for x, char, y in triples:
        grid_y = max_y - y   # invert Y so 0 is top
        grid_x = x - min_x
        grid[grid_y][grid_x] = char

    print("\n Reconstructed ASCII Art:\n")
    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    url = "https://docs.google.com/document/d/e/2PACX-1vSHZVsgUa7oCncQUD3UWOTCIIpdDyM2EEHJ5MQnUSSQQ6sd2MX0FGiJaMD3QAzjnPOUNHNmATyc72Ob/pub"
    reconstruct_ascii(url)
