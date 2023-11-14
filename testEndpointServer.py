from flask import Flask, request, jsonify
import socket
import json

app = Flask(__name__)
frontend_server_address = ('localhost', 9000)

@app.route('/api/v1/sync/request', methods=['POST'])
def forward_request():
    try:
        data = json.dumps(request.json)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(frontend_server_address)
            s.sendall(data.encode())
        
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11000)