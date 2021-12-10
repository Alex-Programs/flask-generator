from flask import Flask, render_template, send_from_directory
from waitress import serve

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/assets/<path:path>")
def send_assets(path):
    return send_from_directory("assets", path)


debug = False
if debug:
    print("DEBUG ENABLED: DEBUG POSES A SIGNIFICANT SECURITY RISK\n" * 32)

    port = int("$PORT")

    app.run(host="127.0.0.1", port=port)

else:
    port = int("$PORT")
    print("Serving")
    serve(app, host="0.0.0.0", port=port)