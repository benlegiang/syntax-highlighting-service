from flask import Flask, jsonify, request
from app.utils.SHModelUtils import *

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return jsonify({'message':'syntax highlighting prediction api!'})

@app.route('/predict', methods=['POST'])
def predict():
    # TODO!!!
    
    data = request.get_json()

    
    model = SHModel(PYTHON3_LANG_NAME, "PythonModel") # Second argument: name for pytorch file

    # tokenIds from LToks for prediction
    model.setup_for_prediction()
    p = model.predict([1, 25, 30, 44, 55])

    return jsonify({'result': p})

# Use this endpoint to pull best model from mongo and call setu_up_for_prediction
# Check if there's a downtime
@app.route('/update', methods=['POST'])
def pull_latest_model():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=5555)

