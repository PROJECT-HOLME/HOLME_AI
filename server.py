from flask import Flask, request, jsonify
import json
import random
import requests

app = Flask(__name__)
backendServerSync = 'https://53a2-211-36-146-73.ngrok-free.app/api/v1/sync/request?type=sync'
backendServerUpgr = 'http://localhost:11000/api/v1/sync/request?type=upgr'
backendServerRepl = 'http://localhost:11000/api/v1/sync/request?type=repl'

# Globally declared dictionary for storing the aircon_payload
aircon_payload = {
    'user': 'Kang',
    'connectedDevices': [],
    'payloads': [{
        "instanceType": 3,
        "payload":{
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
    }]
}

# Function to extract action.parameters(parameters required for response)
def save_action_parameters(request_data):
    parameters = {}
    action_parameters = request_data.get('action', {}).get('parameters', {})
    for key, value in action_parameters.items():
        parameters[key] = value
    return parameters

# Function for assigning proper values to aricon_payload
# For the aircon instance, this function must always be executed first
@app.route('/action.aircon_turn_on', methods=['POST'])
def aircon_turn_on():
    global aircon_payload
    try:
        # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        init_temp_parameters = action_parameters.get('initTemp', {})

        # Assign proper values
        aircon_payload["payloads"][0]["payload"]["trigger"] = True
        aircon_payload["payloads"][0]["payload"]["mode"] = "modeCooling"
        aircon_payload["payloads"][0]["payload"]["airflowDirect"] = True
        aircon_payload["payloads"][0]["payload"]["fanSpeed"] = 5
        aircon_payload["payloads"][0]["payload"]["brightnessScreen"] = 10
        aircon_payload["payloads"][0]["payload"]["objTemperature"] = init_temp_parameters["value"]
        aircon_payload["payloads"][0]["payload"]["startWakeupTimer"] = False
        aircon_payload["payloads"][0]["payload"]["startShutdownTimer"] = False
        aircon_payload["payloads"][0]["payload"]["stopWakeupTimer"] = False
        aircon_payload["payloads"][0]["payload"]["stopShutdownTimer"] = False
        aircon_payload["payloads"][0]["payload"]["wakeupTime"] = -1
        aircon_payload["payloads"][0]["payload"]["shutdownTime"] = -1

        # Send message via HTTP request to backend server
        try:
            print(aircon_payload)
            response = requests.post(backendServerSync, json=aircon_payload)
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

# Funtion that asks whether to replace the soundbar or not
@app.route('/action.ai_speaker_play_music', methods=['POST'])
def ai_speaker_play_music():
    try:
        ai_speaker_payload = {
            'user': 'Kang',
            'connectedDevices': [],
            'payloads': [{
                "instanceType": 9,
                "payload":{
                    "trigger": True,
                    "askForReplacement": True,
                    "replacement": False
                }
           }]
        }
        
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=ai_speaker_payload)
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
    
# Function to be executed when user wants replacement from AI speaker to soundbar
# Sends requests twice(once to AI speaker, another to soundbar)
@app.route('/action.ai_speaker_play_music_yes', methods=['POST'])
def ai_speaker_play_music_yes():
    try:
        play_music_payload = {
            'user': 'Kang',
            'connectedDevices': [],
            'payloads': [
                {
                    "instanceType": 9,
                    "payload":{
                        "trigger": True,
                        "askForReplacement": False,
                        "replacement": True
                    }
                },

                {
                    "instanceType": 7,
                    "payload":{
                        "trigger": True
                    }
                }
            ]
        }

        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerUpgr, json=play_music_payload)
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
    
# Function to be executed when user wants to stop the music
# Sends requests twice(once to AI speaker, another to soundbar)
@app.route('/action.ai_speaker_stop_music', methods=['POST'])
def ai_speaker_stop_music():
    try:
        ai_speaker_payload = {
            'user': 'Kang',
            'connectedDevices': [],
            'payloads': [{
                "instanceType": 9,
                "payload":{
                    "trigger": False,
                    "askForReplacement": False,
                    "replacement": False
                }
           }]
        }
        
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=ai_speaker_payload)
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
    
@app.route('/action.ai_speaker_feed_routine_hotel', methods=['POST'])
def water_dispenser_hotel():
    try:
        pet_feeder_payload = {
            'user': 'Kang',
            'connectedDevices': [],
            'payloads': [{
                "instanceType": 10,
                "payload":{
                    "trigger" : True
                }
           }]
        }

        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=pet_feeder_payload)
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

@app.route('/action.ai_speaker_feed_routine_hotel_yes', methods=['POST'])
def water_dispenser_hotel_yes():
    try:
        water_dispenser_payload = {
            'user': 'Kang',
            'connectedDevices': [],
            'payloads': [{
                "instanceType": 5,
                "payload":{
                    "triggerReminder": True,
                    "triggerWater": True
                }
           }]
        }
        
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerRepl, json=water_dispenser_payload)
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

# Function to be executed when user does not want replacement
@app.route('/action.ai_speaker_play_music_no', methods=['POST'])
@app.route('/action.ai_speaker_play_music_default', methods=['POST'])
def ai_speaker_play_music_no():
    try:
        ai_speaker_payload = {
            'user': 'Kang',
            'connectedDevices': [],
            'payloads': [{
                "instanceType": 9,
                "payload":{
                    "trigger": True,
                    "askForReplacement": False,
                    "replacement": False
                }
           }]
        }
        
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=ai_speaker_payload)
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

@app.route('/action.aircon_change_airflow_direct', methods=['POST'])
def aircon_change_airflow_direct():
    global aircon_payload
    try:
        aircon_payload["payloads"][0]["payload"]["airflowDirect"] = True
        
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=aircon_payload)
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
    global aircon_payload
    try:
        aircon_payload["payloads"][0]["payload"]["airflowDirect"] = False 
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=aircon_payload)
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
    global aircon_payload
    try:
        # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        airconMode_parameters = action_parameters.get('airconMode', {})
        
        aircon_payload["payloads"][0]["payload"]["mode"] = airconMode_parameters['value']
       
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=aircon_payload)
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
    global aircon_payload
    try:
        # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        fanSpeed_parameters = action_parameters.get('fanSpeed', {})

        aircon_payload["payloads"][0]["payload"]["fanSpeed"] = fanSpeed_parameters['value']
        
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=aircon_payload)
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
    global aircon_payload
    try:
         # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        screen_brightness_parameters = action_parameters.get('screenBrightness', {})
        
        aircon_payload["payloads"][0]["payload"]["brightnessScreen"] = screen_brightness_parameters['value']
            
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=aircon_payload)
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
    global aircon_payload
    try:
         # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        setTemp_parameters = action_parameters.get('setTemp', {})

        aircon_payload["payloads"][0]["payload"]["objTemperature"] = setTemp_parameters['value']

        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=aircon_payload)
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
    global aircon_payload
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
    global aircon_payload
    try:
        # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        shut_down_parameters = action_parameters.get('shutdownHour', {})

        aircon_payload["payloads"][0]["payload"]["startShutdownTimer"] = True
        aircon_payload["payloads"][0]["payload"]["shutdownTime"] = shut_down_parameters['value']
    
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=aircon_payload)
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
    global aircon_payload
    try:
        aircon_payload["payloads"][0]["payload"]["stopShutdownTimer"] = True
        aircon_payload["payloads"][0]["payload"]["shutdownTime"] = -1

        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=aircon_payload)
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
    global aircon_payload
    try:
        # Extract parameters from request_data
        request_data = request.get_json()
        action_parameters = save_action_parameters(request_data)
        wake_up_parameters = action_parameters.get('wakeupHour', {})

        aircon_payload["payloads"][0]["payload"]["startWakeupTimer"] = True
        aircon_payload["payloads"][0]["payload"]["wakeupTime"] = wake_up_parameters['value']

        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=aircon_payload)
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
    global aircon_payload
    try:
        aircon_payload["payloads"][0]["payload"]["stopWakeupTimer"] = True
        aircon_payload["payloads"][0]["payload"]["wakeupTime"] = -1

        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=aircon_payload)
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
    global aircon_payload
    try:
        aircon_payload["payloads"][0]["payload"]["trigger"] = False
        
        # Send message via HTTP request to backend server
        try:
            response = requests.post(backendServerSync, json=aircon_payload)
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