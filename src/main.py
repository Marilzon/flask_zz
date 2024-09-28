from httpx import get 

pl = get("https://duckduckgo.com/")

print(pl)