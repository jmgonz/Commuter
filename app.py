from flask import Flask, render_template, redirect
import random

app=Flask(__name__,static_folder='calendar')

@app.route("/")
def home():
	return redirect("/templates/calendar")

@app.route("/templates/calendar")
def home_template():
	return render_template("calendar.html")

@app.route("/templates/hrhistory")
def hr_template():
	return render_template("hrhistory.html")

@app.route("/templates/trip")
def trip_template():
	return render_template("trip.html")


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
