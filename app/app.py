import os
import socket

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        message=os.getenv("GREETING", "Hola desde Docker y Kubernetes"),
        version=os.getenv("APP_VERSION", "v1"),
        hostname=socket.gethostname(),
    )


@app.get("/health")
def health():
    return jsonify(status="ok")
