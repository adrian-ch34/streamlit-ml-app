import os
import pickle
from flask import Flask, request, render_template_string

MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Iris Predictor</title>
  <style>
    body { font-family: Arial; max-width: 720px; margin: 40px auto; }
    .card { padding: 20px; border: 1px solid #ddd; border-radius: 12px; }
    label { display:block; margin-top: 10px; }
    input { width: 100%; padding: 10px; margin-top: 6px; }
    button { margin-top: 16px; padding: 10px 14px; }
    .result { margin-top: 16px; font-weight: bold; }
    small { color: #666; }
  </style>
</head>
<body>
  <h1>Iris deploy (demo)</h1>
  <div class="card">
    <p>Ingresa medidas (cm): <small>sepal length, sepal width, petal length, petal width</small></p>
    <form method="POST">
      <label>Sepal length</label>
      <input name="sl" type="number" step="0.1" required value="{{sl}}">
      <label>Sepal width</label>
      <input name="sw" type="number" step="0.1" required value="{{sw}}">
      <label>Petal length</label>
      <input name="pl" type="number" step="0.1" required value="{{pl}}">
      <label>Petal width</label>
      <input name="pw" type="number" step="0.1" required value="{{pw}}">
      <button type="submit">Predecir</button>
    </form>

    {% if result %}
      <div class="result">Predicción: {{ result }}</div>
    {% endif %}
  </div>
</body>
</html>
"""

def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

model = None
classes = ["setosa", "versicolor", "virginica"]

@app.route("/", methods=["GET", "POST"])
def index():
    global model
    if model is None:
        model = load_model()

    default_vals = {"sl":"5.1","sw":"3.5","pl":"1.4","pw":"0.2"}
    result = None

    if request.method == "POST":
        sl = request.form.get("sl", default_vals["sl"])
        sw = request.form.get("sw", default_vals["sw"])
        pl = request.form.get("pl", default_vals["pl"])
        pw = request.form.get("pw", default_vals["pw"])

        X = [[float(sl), float(sw), float(pl), float(pw)]]
        pred = int(model.predict(X)[0])
        result = classes[pred]

        return render_template_string(HTML, result=result, sl=sl, sw=sw, pl=pl, pw=pw)

    return render_template_string(HTML, result=result, **default_vals)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
