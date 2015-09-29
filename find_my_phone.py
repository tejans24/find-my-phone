#!/usr/local/bin/python
from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException
import requests
import json
import os
import sys

#disabling warings from urllib3 for https
requests.packages.urllib3.disable_warnings()

#constants
CONFIG_FILE_NAME = 'creds.json'

def validate_config(data):
    req_attrs = {"icloud_email", "password"}
    has_valid_attrs = data.viewkeys() > req_attrs
    if(not has_valid_attrs):
        sys.exit("%s doesn't have proper attrs" % CONFIG_FILE_NAME)

def read_and_validate_json_config():
    try:
        with open(CONFIG_FILE_NAME) as data_file:
            data = json.load(data_file)
            validate_config(data)
            return data
    except IOError:
        print("Please provide a '%s' file with icloud_email \
        and password fields" % CONFIG_FILE_NAME)
        sys.exit()

def get_devices(user_creds):
    try:
        api = PyiCloudService(user_creds['icloud_email'], user_creds['password'])
        return api.devices
    except PyiCloudFailedLoginException:
        print("Invalid email/password combination.")
        sys.exit()

def print_api_devices(devices):
    max_devices = 0

    for idx, val in enumerate(devices):
      print ("%s: %s" % (idx, val.status()['name'])).encode('utf-8')
      max_devices = max_devices + 1

    return max_devices

def get_device_choice(max_devices):
    device_num = input('Which device? : ')

    while(device_num > max_devices or device_num < 0):
      device_num = input('Invalid, which device again? : ')

    return device_num

def ping_device(devices, device_choice):
    devices[device_choice].play_sound()

def main(argv):
    user_creds = read_and_validate_json_config()
    devices = get_devices(user_creds)
    max_devices = print_api_devices(devices)
    device_choice = get_device_choice(max_devices)
    ping_device(devices, device_choice)

if __name__ == "__main__":
    main(sys.argv)
