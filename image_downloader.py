import os
import random
import requests
import urllib.parse

from api_keys import PEXELS_API_KEY, PIXABAY_API_KEY

IMAGES_DIR = "assets/images"
DATA_DIR = "data"

# -----------------------------
# 1. Read script / title / image_query
# -----------------------------
def load_text():
    script_path = os.path.join(DATA_DIR, "script.txt")
    title_path = os.path.join(DATA_DIR, "title.txt")
    iq_path = os.path.join(DATA_DIR, "image_query.txt")

    script = ""
    title = ""
    image_query = ""

    if os.path.exists(script_path):
        with open(script_path) as f:
            script = f.read().lower()

    if os.path.exists(title_path):
        with open(title_path) as f:
            title = f.read().lower()

    if os.path.exists(iq_path):
        with open(iq_path) as f:
            image_query = f.read().strip()

    return title, script, image_query


# -----------------------------
# 2. Detect car topic from text (fallback)
# -----------------------------
def detect_car_topic(title, script):
    text = f"{title} {script}"

    topics = [
        ("f1", ["formula 1", "f1", "grand prix", "verstappen", "hamilton"]),
        ("drift car", ["drift", "drifting", "tokyo", "initial d"]),
        ("jdm car", ["jdm", "supra", "rx7", "skyline", "gtr", "silvia"]),
        ("muscle car", ["muscle", "mustang", "camaro", "charger", "challenger"]),
        ("classic car", ["classic", "vintage", "retro", "1960", "1970"]),
        ("supercar", ["supercar", "hypercar", "ferrari", "lamborghini", "mclaren", "bugatti", "porsche"]),
        ("luxury car interior", ["interior", "leather seats", "dashboard", "infotainment"]),
        ("engine closeup", ["engine", "v8", "v10", "v12", "horsepower", "turbo", "twin-turbo"]),
        ("electric car", ["electric", "ev", "tesla", "battery", "motor"]),
        ("offroad suv", ["offroad", "4x4", "suv", "jeep", "dirt", "mud"]),
        ("race track car", ["track", "lap time", "racing", "race car"]),
    ]

    for topic, keywords in topics:
        if any(k in text for k in keywords):
            return topic

    if "car" in text or "cars" in text:
        return "cool car"

    return "supercar"


def build_queries(base_keywords):
    """
    Build multiple slightly different queries so we get variety.
    base_keywords: either AI image_query or detected topic.
    """
    base = base_keywords.strip()
    extras = [
        "",
        "4k",
        "high quality",
        "cinematic",
        "vertical",
        "night shot",
        "motion blur",
    ]
    queries = [f"{base} {e}".strip() for e in extras]
    random.shuffle(queries)
    return queries


# -----------------------------
# 3. Download from Pexels
# -----------------------------
def download_from_pexels(query, max_images=6):
    if not PEXELS_API_KEY:
        print("⚠️ No PEXELS_API_KEY set. Skipping Pexels.")
        return []

    print(f"🔍 Pexels search: {query!r}")
    url = "https://api.pexels.com/v1/search"
    params = {
        "query": query,
        "per_page": max_images,
        "orientation": "portrait",
    }
    headers = {"Authorization": PEXELS_API_KEY}

    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print("❌ Pexels request failed:", e)
        return []

    data = r.json()
    out = []
    for photo in data.get("photos", []):
        src = photo.get("src", {})
        link = src.get("large") or src.get("large2x") or src.get("original")
        if link:
            out.append(link)
    return out


# -----------------------------
# 4. Download from Pixabay
# -----------------------------
def download_from_pixabay(query, max_images=6):
    if not PIXABAY_API_KEY:
        print("⚠️ No PIXABAY_API_KEY set. Skipping Pixabay.")
        return []

    print(f"🔍 Pixabay search: {query!r}")
    url = "https://pixabay.com/api/"
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "image_type": "photo",
        "orientation": "vertical",
        "category": "transportation",
        "per_page": max_images,
        "safesearch": "true",
    }

    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print("❌ Pixabay request failed:", e)
        return []

    data = r.json()
    out = []
    for hit in data.get("hits", []):
        link = hit.get("largeImageURL") or hit.get("webformatURL")
        if link:
            out.append(link)
    return out


# -----------------------------
# 5. Save images locally
# -----------------------------
def save_images(urls, max_total=10):
    os.makedirs(IMAGES_DIR, exist_ok=True)

    for f in os.listdir(IMAGES_DIR):
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            os.remove(os.path.join(IMAGES_DIR, f))

    selected = urls[:max_total]
    print(f"⬇️ Downloading {len(selected)} images...")

    saved = []
    for i, url in enumerate(selected):
        ext = ".jpg"
        parsed = urllib.parse.urlparse(url)
        if parsed.path.lower().endswith((".png", ".webp", ".jpeg", ".jpg")):
            ext = os.path.splitext(parsed.path)[1]

        out_path = os.path.join(IMAGES_DIR, f"car_{i}{ext}")

        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            with open(out_path, "wb") as f:
                f.write(resp.content)
            saved.append(out_path)
            print(f"✅ {out_path}")
        except Exception as e:
            print(f"❌ Failed {url}: {e}")

    return saved


def main():
    title, script, image_query = load_text()

    if image_query:
        print("\n🧠 Using AI image_query from model:", image_query)
        base_keywords = image_query
    else:
        topic = detect_car_topic(title, script)
        print("\n🧠 No AI image_query found. Detected car topic:", topic)
        base_keywords = topic

    queries = build_queries(base_keywords)

    all_urls = []
    for q in queries:
        if len(all_urls) >= 12:
            break
        all_urls.extend(download_from_pexels(q, max_images=6))
        all_urls.extend(download_from_pixabay(q, max_images=6))

    seen = set()
    clean_urls = []
    for u in all_urls:
        if u not in seen:
            seen.add(u)
            clean_urls.append(u)

    if not clean_urls:
        print("⚠️ No images found. Falling back to generic 'supercar'.")
        fallback_queries = build_queries("supercar")
        for q in fallback_queries:
            if len(clean_urls) >= 10:
                break
            clean_urls.extend(download_from_pexels(q, max_images=6))
            clean_urls.extend(download_from_pixabay(q, max_images=6))

    if not clean_urls:
        raise SystemExit("❌ Still no images found. Check API keys or internet.")

    saved = save_images(clean_urls, max_total=10)

    print("\n🎉 Images downloaded successfully into 'images/':")
    for s in saved:
        print("   ", s)


if __name__ == "__main__":
    main()
