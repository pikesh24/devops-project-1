from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_request_count_total",
    "Total HTTP request count",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "HTTP request latency in seconds",
    ["endpoint"]
)


def track(endpoint):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                response = fn(*args, **kwargs)
                status = response[1] if isinstance(response, tuple) else 200
                REQUEST_COUNT.labels("GET", endpoint, status).inc()
                return response
            finally:
                REQUEST_LATENCY.labels(endpoint).observe(time.time() - start)
        wrapper.__name__ = fn.__name__
        return wrapper
    return decorator


@app.route("/")
@track("/")
def home():
    return jsonify({"message": "DevOps Demo App", "status": "running"})


@app.route("/health")
@track("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/data")
@track("/data")
def data():
    time.sleep(random.uniform(0.05, 0.3))
    return jsonify({"items": list(range(10)), "count": 10})


@app.route("/error")
@track("/error")
def trigger_error():
    return jsonify({"error": "simulated error"}), 500


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
