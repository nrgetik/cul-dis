import random
from flask import Flask
from flask import render_template
import artsy_db

app = Flask(__name__)

ARTWORKS = artsy_db.get_artworks()
ART_IDS = [artwork["__id"] for artwork in ARTWORKS]

# Catch all paths with these route rules
@app.route("/", defaults={"path": ""}, strict_slashes=False)
@app.route("/<path:path>", strict_slashes=False)
def dispense_culture(path):
    path = None if path else None
    werk_id = random.choice(ART_IDS)
    artwerk = next(werk for werk in ARTWORKS if werk["__id"] == werk_id)
    return render_template("index.html",
        ART_ID=artwerk["__id"],
        ART_ARTIST=artwerk["artists"][0] if artwerk["artists"] else None,
        ART_TITLE=artwerk["title"] if artwerk["title"] else None,
        ART_CIRCA=artwerk["date"] if artwerk["date"] else None,
        ART_MEDIUM=artwerk["medium"] if artwerk["medium"] else None,
        ART_HELD=artwerk["collecting_institution"] if artwerk["collecting_institution"] else None,
        ART_ICON=artwerk["iconicity"] if artwerk["iconicity"] else None)

def main():
    app.run()

if __name__ == "__main__":
    main()
