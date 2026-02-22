from flask import Flask, render_template, request, jsonify  # pyright: ignore[reportMissingImports]
from quake_alert import check_threat

app = Flask(__name__, static_url_path='/static', static_folder='static')

precautions = [
    "Drop, Cover, and Hold On during shaking.",
    "Stay indoors until the shaking stops and it is safe to go outside.",
    "Stay away from windows, glass, and heavy objects.",
    "If outside, move to an open area away from buildings and power lines.",
    "Have an emergency kit ready with food, water, and medical supplies.",
    "Plan and practice earthquake drills with your family."
]

@app.route("/")
def index():
    # Pass initial status
    return render_template("index.html", status="System ready. Monitoring earthquakes...")

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    lat = float(data.get("lat", 0))
    lon = float(data.get("lon", 0))

    alerts = check_threat((lat, lon))

    return jsonify({
        "alerts": alerts,
        "precautions": precautions
    })

if __name__ == "__main__":
    app.run(debug=True)
