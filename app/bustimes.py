from __future__ import absolute_import
from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template
from flask import request
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)
app.config.from_envvar("SECRETS")
Bootstrap(app)

@app.route("/")
def routes():
    r = requests.get(app.config['API_URL'] + "/getroutes?key="
        + app.config['API_KEY'])
    xml = BeautifulSoup(r.text, "xml")
    return render_template('routes.html', routes=xml, title="Bus Routes")

@app.route("/directions/<rt>/<rtnm>")
def directions(rt, rtnm):
    r = requests.get(app.config['API_URL'] + "/getdirections?key="
        + app.config['API_KEY'] + "&rt=" + rt)
    xml = BeautifulSoup(r.text, "xml")
    return render_template('directions.html', directions=xml, rt=rt,
                            rtnm=rtnm, title="Bus Directions")

@app.route("/stops/<rt>/<rtnm>/<direction>")
def stops(rt, rtnm, direction):
    r = requests.get(app.config['API_URL'] + "/getstops?key="
        + app.config['API_KEY'] + "&rt=" + rt + "&dir=" + direction)
    xml = BeautifulSoup(r.text, "xml")
    return render_template('stops.html', stops=xml, rt=rt, rtnm=rtnm,
                           direction=direction, title="Bus Stops")

@app.route("/predictions/<rt>/<rtnm>/<direction>/<stop>")
def predictions(rt, rtnm, direction, stop):
    r = requests.get(app.config['API_URL'] + "/getpredictions?key="
        + app.config['API_KEY'] + "&rt=" + rt + "&dir=" + direction
        + "&stpid=" + stop)
    xml = BeautifulSoup(r.text, "xml")
    predictions = []
    for prediction in xml.find_all("prd"):
        predictions.append(
            {'stpnm':prediction.stpnm.text,
             'vid': prediction.vid.text,
             'rt': prediction.rt.text,
             'rtdir': prediction.rtdir.text,
             'des': prediction.des.text,
             'prdtm': prediction.prdtm.text
            })

    return render_template('predictions.html', predictions=predictions, rt=rt,
                           rtnm=rtnm, direction=direction, stop=stop,
                           title="Bus Predictions")

if __name__ == "__main__":
    app.debug = True
    app.run()
