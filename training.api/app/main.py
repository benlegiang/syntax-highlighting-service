from flask import Flask, Response, jsonify, request

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return jsonify({'message':'syntax highlighting training api'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8000)

