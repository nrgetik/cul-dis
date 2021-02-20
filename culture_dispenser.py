from flask import Flask
app = Flask(__name__)

@app.route("/")
def dispense_culture():
    return "Here's some culture for you, ya dirty animal"

def main():
    app.run()

if __name__ == "__main__":
    main()
