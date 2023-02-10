"""
Flask server
"""

import base64
from flask import Flask
from radiators import display_data

app = Flask(__name__)


def display_graph(timescale="24h") -> str:
    """Return graphical monitor logs over specified timescale."""
    buf = display_data.display_data(timescale)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    html = f"""
<p style="margin-left: 30px; margin-top: 20px;"><font size=5><b>Radiators ({timescale})</b></font></p>
<div><img src='data:image/png;base64,{data}'/></div>
"""
    return html


@app.route("/")
def main() -> str:
    return display_graph()


@app.route("/24hr")
def display24h() -> str:
    return display_graph("24h")


@app.route("/1day")
def display1day() -> str:
    return display_graph("24h")


@app.route("/1hr")
def display1hr() -> str:
    return display_graph("1h")


@app.route("/1week")
def display1week() -> str:
    return display_graph("168h")


@app.route("/1month")
def display1month() -> str:
    return display_graph("672h")
