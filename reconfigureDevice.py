import json
import requests
import netifaces

json_file = open('MBP_config.json', 'r')
mbp_config = json.load(json_file)
for key in mbp_config.keys():
    print(key)
current_vpn_ip = netifaces.ifaddresses('tun0')[netifaces.AF_INET][0]['addr']

base_url = 'http://' + mbp_config['MBP_SERVER_IP'] + ':8080/MBP/api/'

if current_vpn_ip != mbp_config['LAST_VPN_IP']:

    device_url = base_url + 'devices/' + mbp_config['DEVICE_ID']

    device = {
        "name": "Lucio's Rasp",
        "componentType": "Raspberry Pi",
        "ipAddress": current_vpn_ip,
        "username": "pi",
        "password": "ALauEhD+"
    }
    r_device = requests.put(device_url, auth=('admin', 'admin'), json=device)

    if r_device.status_code != 200 and r_device.status_code != 201:
        # DEAL WITH REQUESTS ERROR HERE. MAYBE LOG IN A ERROS FILES
        print("erro reconfigure rasp")

    # UPDATE MBP CONFIG FILES WITH NEW IP
    mbp_config['LAST_VPN_IP'] = str(current_vpn_ip)
    with open('MBP_config.json', 'w') as json_file:
        json.dump(mbp_config, json_file)

# GET ALL SENSORS TO START RECORDING AGAIN
# sensors_url = base_url + 'sensors'
# r_sensors = requests.get(sensors_url, auth=('admin', 'admin'))
# sensors = json.loads(r_sensors.content)['_embedded']['sensors']

# for sensor in sensors:
#     if sensor['_embedded']['device']['id'] == mbp_config['DEVICE_ID']:
#         start_sensor_url = base_url + 'start/sensor/' + sensor['id']
#         print(start_sensor_url)
#         r_start_sensor = requests.post(start_sensor_url,
#                                        auth=('admin', 'admin'))
#         if r_start_sensor.status_code != 200 and \
#                 r_start_sensor.status_code != 201:
#             print(r_start_sensor.content)
