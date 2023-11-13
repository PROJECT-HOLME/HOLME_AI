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
    
@app.route('/action.aircon_change_airflow_indirect', methods=['POST'])
def aircon_change_airflow_indirect():
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

@app.route('/action.aircon_change_mode', methods=['POST'])
def aircon_change_mode():
    try:
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        
        # Send message via socket to backend server
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect(backendServer)
            client_socket.send(json.dumps(request_data).encode() + b'\n')  # Convert to bytes and add newline
            client_socket.close()
        except Exception as e:
            print(f"Failed to connect backend server: {str(e)}")

        # Extract parameters from request_data
        airconMode_parameters = action_parameters.get('airconMode', {})
        output_dict = {'airconMode': airconMode_parameters['value']}
        response_data = {
            "version": "2.0",
            "resultCode": "OK",
            "output": output_dict
        }
        response_data = json.dumps(response_data, indent=2)
        return response_data
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/action.aircon_change_fan_speed', methods=['POST'])
def aircon_change_fan_speed():
    try:
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        
        # Send message via socket to backend server
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect(backendServer)
            client_socket.send(json.dumps(request_data).encode() + b'\n')  # Convert to bytes and add newline
            client_socket.close()
        except Exception as e:
            print(f"Failed to connect backend server: {str(e)}")

        # Extract parameters from request_data
        fanSpeed_parameters = action_parameters.get('fanSpeed', {})
        output_dict = {'fanSpeed': fanSpeed_parameters['value']}
        response_data = {
            "version": "2.0",
            "resultCode": "OK",
            "output": output_dict
        }
        response_data = json.dumps(response_data, indent=2)
        return response_data
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/action.aircon_change_screen_brightness', methods=['POST'])
def aircon_change_screen_brightness():
    try:
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        
        # Send message via socket to backend server
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect(backendServer)
            client_socket.send(json.dumps(request_data).encode() + b'\n')  # Convert to bytes and add newline
            client_socket.close()
        except Exception as e:
            print(f"Failed to connect backend server: {str(e)}")

        # Extract parameters from request_data
        screen_brightness_parameters = action_parameters.get('screenBrightness', {})
        output_dict = {'screenBrightness': screen_brightness_parameters['value']}
        response_data = {
            "version": "2.0",
            "resultCode": "OK",
            "output": output_dict
        }
        response_data = json.dumps(response_data, indent=2)
        return response_data
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/action.aircon_change_temp', methods=['POST'])
def aircon_change_temp():
    try:
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        
        # Send message via socket to backend server
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect(backendServer)
            client_socket.send(json.dumps(request_data).encode() + b'\n')  # Convert to bytes and add newline
            client_socket.close()
        except Exception as e:
            print(f"Failed to connect backend server: {str(e)}")

        # Extract parameters from request_data
        setTemp_parameters = action_parameters.get('setTemp', {})
        output_dict = {'setTemp': setTemp_parameters['value']}
        response_data = {
            "version": "2.0",
            "resultCode": "OK",
            "output": output_dict
        }
        response_data = json.dumps(response_data, indent=2)
        return response_data
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/action.aircon_check_cur_temp', methods=['POST'])
def aircon_check_cur_temp():
    try:
        request_data = request.get_json()

        # Extract parameters from request_data
        output_dict = {'curTemp': str(round(random.uniform(18.0, 28.0)), 1)}
        response_data = {
            "version": "2.0",
            "resultCode": "OK",
            "output": output_dict
        }
        response_data = json.dumps(response_data, indent=2)
        return response_data
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/action.aircon_shut_down_timer', methods=['POST'])
def aircon_shut_down_timer():
    try:
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        
        # Send message via socket to backend server
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect(backendServer)
            client_socket.send(json.dumps(request_data).encode() + b'\n')  # Convert to bytes and add newline
            client_socket.close()
        except Exception as e:
            print(f"Failed to connect backend server: {str(e)}")

        # Extract parameters from request_data
        shut_down_parameters = action_parameters.get('shutdownHour', {})
        output_dict = {'shutdownHour': shut_down_parameters['value']}
        response_data = {
            "version": "2.0",
            "resultCode": "OK",
            "output": output_dict
        }
        response_data = json.dumps(response_data, indent=2)
        return response_data
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/action.aircon_stop_shut_down_timer', methods=['POST'])
def aircon_stop_shut_down_timer():
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

@app.route('/action.aircon_wakeup_timer', methods=['POST'])
def aircon_wakeup_timer():
    try:
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        
        # Send message via socket to backend server
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect(backendServer)
            client_socket.send(json.dumps(request_data).encode() + b'\n')  # Convert to bytes and add newline
            client_socket.close()
        except Exception as e:
            print(f"Failed to connect backend server: {str(e)}")

        # Extract parameters from request_data
        wake_up_parameters = action_parameters.get('wakeupHour', {})
        output_dict = {'wakeupHour': wake_up_parameters['value']}
        response_data = {
            "version": "2.0",
            "resultCode": "OK",
            "output": output_dict
        }
        response_data = json.dumps(response_data, indent=2)
        return response_data
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/action.aircon_stop_wakeup_timer', methods=['POST'])
def aircon_stop_wakeup_timer():
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

@app.route('/action.aircon_turn_on', methods=['POST'])
def aircon_turn_on():
    try:
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        
        # Send message via socket to backend server
        try:
            client_socket = socket(AF_INET, SOCK_STREAM)
            client_socket.connect(backendServer)
            client_socket.send(json.dumps(action_parameters).encode() + b'\n')  # Convert to bytes and add newline
            client_socket.close()
        except Exception as e:
            print(f"Failed to connect backend server: {str(e)}")

        # Extract parameters from request_data
        init_temp_parameters = action_parameters.get('initTemp', {})
        output_dict = {'initTemp': init_temp_parameters['value']}
        response_data = {
            "version": "2.0",
            "resultCode": "OK",
            "output": output_dict
        }
        response_data = json.dumps(response_data, indent=2)
        return response_data
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/action.aircon_turn_off', methods=['POST'])
def aircon_turn_off():
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