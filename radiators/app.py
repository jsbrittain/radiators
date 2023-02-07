"""
Flask server to provide 
"""

import base64
from flask import Flask
from radiators import display_data

app = Flask(__name__)


@app.route("/")
def main():
    """Root server request returns monitor logs over 24hrs."""
    buf = display_data.display_data(timescale="24h")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    html = f"""
<p style="margin-left: 30px; margin-top: 20px;"><font size=5><b>Radiators (24hrs)</b></font></p>
<div><img src='data:image/png;base64,{data}'/></div>
"""
    return html
