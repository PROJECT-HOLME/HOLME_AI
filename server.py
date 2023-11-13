from flask import Flask, request, jsonify
from socket import *
import json
import random

app = Flask(__name__)
backendServer = ('localhost', 9000)

def save_action_parameters(request_data):
    parameters = {}
    # Extract action.parameters
    action_parameters = request_data.get('action', {}).get('parameters', {})
    for key, value in action_parameters.items():
        parameters[key] = value
    return parameters

@app.route('/action.aircon_change_airflow_direct', methods=['POST'])
def aircon_change_airflow_direct():
    try:
        request_data = request.get_json()

        # Send message via socket to backend server
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect(backendServer)
            client_socket.send(json.dumps(request_data).encode() + b'\n')  # Convert to bytes and add newline
            client_socket.close()
        except Exception as e:
            print(f"Failed to connect backend server: {str(e)}")

        response_data = {
            "version": "2.0",
            "resultCode": "OK",
            "output": {}
        }
        response_data = json.dumps(response_data, indent=2)
        return response_data
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)