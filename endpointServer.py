from flask import Flask, request, jsonify
from socket import *
import json
import random
import requests

app = Flask(__name__)
backendServer = 'http://localhost:11000/api/v1/sync/request'

# Globally declared dictionary for storing the payload of the air conditioner instance
payload = {
            "trigger": None,
            "mode": None,
            "airflowDirect": None,
            "fanSpeed": None,
            "brightnessScreen": None,
            "objTemperature": None,
            "startWakeupTimer": None,
            "startShutdownTimer": None,
            "stopWakeupTimer": None,
            "stopShutdownTimer": None,
            "wakeupTime": None,
            "shutdownTime": None
}

# Function to extract action.parameters(parameters required for response)
def save_action_parameters(request_data):
    parameters = {}
    action_parameters = request_data.get('action', {}).get('parameters', {})
    for key, value in action_parameters.items():
        parameters[key] = value
    return parameters

# Function for assigning proper values
# This function must always be executed first
@app.route('/action.aircon_turn_on', methods=['POST'])
def aircon_turn_on():
    try:
        # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        init_temp_parameters = action_parameters.get('initTemp', {})

        # Assign proper values
        payload["trigger"] = True
        payload["mode"] = "modeCooling"
        payload["airflowDirect"] = True
        payload["fanSpeed"] = 5
        payload["brightnessScreen"] = 10
        payload["objTemperature"] = 18
        payload["startWakeupTimer"] = False
        payload["startShutdownTimer"] = False
        payload["stopWakeupTimer"] = False
        payload["stopShutdownTimer"] = False
        payload["wakeupTime"] = -1
        payload["shutdownTime"] = -1
        
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServer, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect backend server: {str(e)}")
        
        # Send response back to NUGU server
        output_dict = {'initTemp': str(init_temp_parameters['value'])}
        response_data = {
            "version": "2.0",
            "resultCode": "OK",
            "output": output_dict
        }
        response_data = json.dumps(response_data, indent=2)
        return response_data
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/action.aircon_change_airflow_direct', methods=['POST'])
def aircon_change_airflow_direct():
    try:
        payload["airflowDirect"] = True
        
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServer, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
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
        payload["airflowDirect"] = False 
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServer, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
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
        # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        airconMode_parameters = action_parameters.get('airconMode', {})
        
        payload["mode"] = airconMode_parameters['value']
       
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServer, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect backend server: {str(e)}")
        
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
        # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        fanSpeed_parameters = action_parameters.get('fanSpeed', {})

        payload["fanSpeed"] = fanSpeed_parameters['value']
        
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServer, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect backend server: {str(e)}")
        
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
         # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        screen_brightness_parameters = action_parameters.get('screenBrightness', {})
        
        payload["brightnessScreen"] = screen_brightness_parameters['value']
            
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServer, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect backend server: {str(e)}")

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
         # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        setTemp_parameters = action_parameters.get('setTemp', {})

        payload["objTemperature"] = setTemp_parameters['value']

        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServer, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect backend server: {str(e)}")
       
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
        # Extract parameters from request_data
        output_dict = {'curTemp': str(round(random.uniform(18.0, 30.0), 1))} 
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
        # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        shut_down_parameters = action_parameters.get('shutdownHour', {})

        payload["startShutdownTimer"] = True
        payload["shutdownTime"] = shut_down_parameters['value']
    
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServer, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect backend server: {str(e)}")
        
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
        payload["stopShutdownTimer"] = True

            # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServer, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
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
        # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        wake_up_parameters = action_parameters.get('wakeupHour', {})

        payload["startWakeupTimer"] = True
        payload["wakeupTime"] = wake_up_parameters['value']

        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServer, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to connect backend server: {str(e)}")
       
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
        payload["stopWakeupTimer"] = True

        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServer, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
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

@app.route('/action.aircon_turn_off', methods=['POST'])
def aircon_turn_off():
    try:
        payload["trigger"] = False
        
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServer, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
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