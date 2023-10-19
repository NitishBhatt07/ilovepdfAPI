
import requests
from config import public_key,secret_key


# Validate the user and get access token to proceed further.........
def getAuthenticationToken(public_key,secret_key):
    url = 'https://api.ilovepdf.com/v1/auth'
    auth_data = {'public_key': public_key, 'secret_key': secret_key}
    response = requests.post(url, json=auth_data)
    if response.status_code == 200:
        print("Access Granted.....")
        access_token = response.json()['token']
        return access_token
    else:
        return "Access denied....."


# get info about which server is assigned and which task we want to perfrom.....
# we are calling task name as tool name
def getServerTaskID(headers,tool_name):
    url = f'https://api.ilovepdf.com/v1/start/{tool_name}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response = response.json()
        print('successfully fetched server and task ID.')
        return response['server'], response['task']
    else:
        return 'Failed to get server and task ID.'


# upload file to server and return server filename......
def uploadFileToServer(headers,filepath,server,taskID):
    url = url = f'https://{server}/v1/upload'
    files = {'file': open(filepath,'rb')}
    payload = {'task': taskID }
    response = requests.post(url, headers=headers, data=payload, files=files)
    if response.status_code == 200:
        print('File uploaded successfully.')
        response = response.json()
        server_filename = response['server_filename']
        return server_filename
    else:
        return 'There is some error in file uploading......'

# process file....
def fileProcessing(headers,tool_name,server_filename,server,taskID):
    url = f'https://{server}/v1/process'
    files_to_process = [
        {
            'server_filename': server_filename,
            'filename': 'output_file_name1.pdf',
            'rotate': 0,
            'password': None  # Password to open the file (if any)
        }
    ]
    payload = {
        'task': taskID,
        'tool': tool_name,
        'files': files_to_process,
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return 'Files processing initiated successfully...'
    else:
        return 'Failed to initiate files processing....'


# download file...........
def downloadProcessFile(headers,taskID,server):
    url = f"https://{server}/v1/download/{taskID}"
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        filename = "compressed_output_file.pdf"
        # Save the downloaded file
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'Output files downloaded successfully. Saved as: {filename}')
    else:
        return "Failed to download output files...."


access_token = getAuthenticationToken(public_key,secret_key)
headers = {'Authorization': f'Bearer {access_token}'}

tool_name = "compress"
server, taskID = getServerTaskID(headers,tool_name)

filepath = "G:\\MyCodeprojects\\Django Projects\\iLovePdfAPI\\HR.pdf"
server_filename = uploadFileToServer(headers,filepath,server,taskID)

print(fileProcessing(headers,tool_name,server_filename,server,taskID))

print(downloadProcessFile(headers,taskID,server))

