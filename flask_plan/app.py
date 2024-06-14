from flask import Flask, render_template, request
from flask_cors import CORS
import plan
import json

myGPT = plan.PlanGPT()
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/gpt", methods=['POST'])
def gpt():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        print(data['query'])
        print(data['user_plan'])
        result = myGPT.sendGpt(plan=data['user_plan'], msg=data['query'])
        return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5555)