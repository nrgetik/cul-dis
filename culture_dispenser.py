import random
from flask import Flask
from flask import send_file
import artsy_db

app = Flask(__name__)

ARTWORKS = artsy_db.get_artworks()
ART_IDS = [artwork["__id"] for artwork in ARTWORKS]

@app.route("/")
def dispense_culture():
    return send_file(filename_or_fp=f"static/images/{random.choice(ART_IDS)}_optimized.jpg")

def main():
    app.run()

if __name__ == "__main__":
    main()
