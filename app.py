from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Welcome Nilesh Rathod to Flask DevOps Demo</h1>
    <h3>Application deployed successfully using Docker, Jenkins, Helm and Kubernetes.</h3>
    """

@app.route("/health")
def health():
    return jsonify({
        "status": "UP"
    })

@app.route("/version")
def version():
    return jsonify({
        "application": "flask-devops-demo",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
