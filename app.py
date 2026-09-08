import time
from datetime import datetime, timezone
from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated in-memory database for API demonstration
TODOS = [
    {"id": 1, "task": "Configure Jenkins Pipeline", "done": True},
    {"id": 2, "task": "Deploy Helm Chart to Kubernetes", "done": False}
]

START_TIME = time.time()

# -------------------------------------------------------------------
# Core Routes & Health Probes (Required for Helm/Kubernetes)
# -------------------------------------------------------------------

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "flask-devops-demo",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200

@app.route('/healthz')
def health_check():
    """Liveness probe for Helm/Kubernetes deployment."""
    return jsonify({"status": "healthy"}), 200

@app.route('/ready')
def readiness_check():
    """Readiness probe for Helm/Kubernetes ingress traffic."""
    return jsonify({"status": "ready"}), 200

@app.route('/metrics')
def metrics():
    """Basic runtime metrics endpoint."""
    uptime_seconds = round(time.time() - START_TIME, 2)
    return jsonify({
        "uptime_seconds": uptime_seconds,
        "total_todos": len(TODOS)
    }), 200

# -------------------------------------------------------------------
# REST API Endpoints
# -------------------------------------------------------------------

@app.route('/api/v1/todos', methods=['GET'])
def get_todos():
    return jsonify({"count": len(TODOS), "data": TODOS}), 200

@app.route('/api/v1/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({"error": "Field 'task' is required"}), 400
    
    new_item = {
        "id": len(TODOS) + 1,
        "task": data['task'],
        "done": False
    }
    TODOS.append(new_item)
    return jsonify({"message": "Task added", "item": new_item}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
