import base64
from flask import Flask
from radiators import display_data

app = Flask(__name__)


@app.route("/")
def hello():
    buf = display_data()
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    html = f"""
<p style="margin-left: 30px; margin-top: 20px;"><font size=5><b>Radiators (24hrs)</b></font></p>
<div><img src='data:image/png;base64,{data}'/></div>
"""
    return html
