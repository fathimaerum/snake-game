from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>🐍 Snake Game Project</h1>
    <p>This is my Python Snake Game.</p>
    <p>Run the game locally using snake_game_2.py</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
