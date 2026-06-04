from crawler.fda import fetch_fda

data = fetch_fda()

print("Total:", len(data))

for item in data[:5]:
    print(item["title"])