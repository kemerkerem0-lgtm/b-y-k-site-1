from flask import Flask, render_template
import requests
import time

app = Flask(__name__)

def get_platform_data():
    try:
        t = int(time.time())
        # Steam API'den ham veriyi alıyoruz
        url = f"https://store.steampowered.com/api/featuredcategories?cc=tr&l=turkish&t={t}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10).json()
        
        # 1. Öne Çıkan Dev Banner (YouTube'un en üstü gibi)
        featured = response.get('featured_win', {}).get('items', [])[:3]
        
        # 2. İndirimli Kartlar
        specials = response.get('specials', {}).get('items', [])[:12]
        
        # 3. En Çok Satanlar
        top_sellers = response.get('top_sellers', {}).get('items', [])[:8]

        return {
            "featured": featured,
            "specials": specials,
            "top_sellers": top_sellers
        }
    except Exception as e:
        print(f"Hata: {e}")
        return None

@app.route("/")
def index():
    content = get_platform_data()
    return render_template("index.html", content=content)

@app.route("/hakkimizda")
def hakkimizda(): return render_template("hakkimizda.html")

@app.route("/gizlilik")
def gizlilik(): return render_template("gizlilik.html")

if __name__ == "__main__":
    app.run(debug=True)