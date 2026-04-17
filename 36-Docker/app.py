from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML template (inside same file)
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Multiplication Table</title>
</head>
<body>
    <h2>Multiplication Table Generator</h2>

    <form method="post">
        <input type="number" name="number" placeholder="Enter a number" required>
        <button type="submit">Generate Table</button>
    </form>

    {% if table %}
        <h3>Table of {{ number }}</h3>
        <ul>
        {% for line in table %}
            <li>{{ line }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    table = []
    number = None

    if request.method == "POST":
        number = int(request.form["number"])

        table = [f"{number} x {i} = {number * i}" for i in range(1, 11)]

    return render_template_string(HTML, table=table, number=number)


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)