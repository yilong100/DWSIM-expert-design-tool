from flask import Flask, redirect, url_for, render_template, request
from dwsimautomation import PowerGenerated
from dwsimflowsheet import PowerGenerated1
import multiprocessing
from multiprocessing import Pool, Process, Value


# creates instance of flask application
app = Flask(__name__)

# home page
@app.route("/")
def home():
    return render_template("index.html")

# taking inputs page
# if value inputted, redirect to outputsPage, otherwise display inputsPage
# inputs concatenates the inputted values into a string seperated by a comma which will then be split into a list in outputsPage
# to add inputs, add from line 26 onwards
@app.route("/inputsPage", methods=["POST", "GET"])
def inputsPage():
    if request.method == "POST":
        inputs = ""
        inputs += request.form["mf"]
        inputs += ","
        inputs += request.form["t"]
        return redirect(url_for("outputsPage", inputs=inputs))
    else:
        return render_template("inputsPage.html")


# returning Power Generated from PowerGenerated1 in dwsimflowsheet
# line 40 - values splits string into a list so we can access the values 
# lines 36-38, 40-45 spawns a new process when calling PowerGenerated1 every time and allows the value returned
# from PowerGenerated1 to be shown
# to add values, enter in args() on line 43
@app.route("/<inputs>")
def outputsPage(inputs):
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    a_list = []
    values = inputs.split(",")
    p = Process(target = PowerGenerated1, args = (values[0], values[1], return_dict))
    a_list.append(p)
    p.start()
    p.join()
    #for element in a_list:
    #    element.join()
    return f"<h1>{return_dict.values()}</h1>"


# starts website
if __name__ == "__main__":
    app.run(debug=True)
  
