from FlaskRestTest import app
from flask import request
from flask import make_response
import paramiko
import json
import requests
import store_utils



@app.route("/ssh/v1/runcommand", methods=['POST'])
def run_ssh_command():
    
    response_data = dict()
    response_data["data"] = dict()
    response_data["error"] = None
    response_data["endpoint"] = "SshModule.run_ssh_command"
    response_data["version"] = "v1"


    try:
        requestData = request.get_json(silent=True)
        if requestData is None:
            raise ValueError("Failed to parse request from json")
        else:
        
            command = requestData["command"]
            if not command.startswith("cat "):
                raise ValueError("Only cat command can be run")

            if ';' in command:
                raise ValueError("Cannot run command with ';' in it")
            host = requestData["host"]
            port = requestData["port"] or 22
            user = requestData["user"]
            passwd = requestData["passwd"]

            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.WarningPolicy())
            client.connect(host, port, user, passwd)
            (stdin, stdout, stderr) = client.exec_command(command)

            temp_dict = dict()
            temp_dict["stdout"] = stdout.readlines()
            temp_dict["stderr"] = stderr.readlines()
            
            response_data["data"] = temp_dict

            data = json.dumps(response_data)

            store_location = store_utils.store_result(data)

            # Add the location to the response data
            response_data["location"] = store_location

            # perform another dump to json
            data = json.dumps(response_data)

            response = make_response(data)
            response.headers["Content-Type"] = "application/json"
            response.headers["endpoint-name"] = "SshModule.run_ssh_command"
            response.headers["endpoint-version"] = "v1"

            return response
    except Exception as e:
        response_data["error"] = e.__class__.__name__ + ": " + e.message
        response_data["data"] = dict()
        response = make_response(json.dumps(response_data), 400)
        response.headers["Content-Type"] = "application/json"
        response.headers["endpoint-name"] = "SshModule.run_ssh_command"
        response.headers["endpoint-version"] = "v1"
        return response


        

