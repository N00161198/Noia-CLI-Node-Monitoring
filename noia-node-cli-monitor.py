# Title: Noia Network Node Monitoring
# Description: Send node data to webhook such as Zapier
# Written by: Ryan Shirley
# Version: 1.0

import os
import re
import subprocess
import time
import requests

# Url of your zapier webhook
endpoint = 'URL'

# Run command to get status of node
response = subprocess.Popen('systemctl -l status noia.service | grep downloaded', shell=True, stdout=subprocess.PIPE).stdout.read()

# Month
month = re.findall('^.{0,3} ', response, re.MULTILINE)
month = month.pop()[:-1]

# Day
day = re.findall('^.{0,3} \d+', response, re.MULTILINE)
day = day.pop()[4:]

# Time
time = re.findall('^.{0,3} \d+ \d+:\d+:\d+', response, re.MULTILINE)
time = time.pop()[7:]

# Downloaded in bytes
downloaded = re.findall('downloaded=\d+', response, re.MULTILINE)
downloaded = downloaded.pop().replace('downloaded=', '')

# Uploaded in bytes
uploaded = re.findall('uploaded=\d+', response, re.MULTILINE)
uploaded = uploaded.pop().replace('uploaded=', '')

# Uptime Hours
hours = re.findall('for \d+', response, re.MULTILINE)
hours = hours.pop().replace('for ', '')

# Uptime Minutes
minutes = re.findall('hours, \d+', response, re.MULTILINE)
minutes = minutes.pop().replace('hours, ', '')

# Uptime Seconds
seconds = re.findall('minutes, \d+', response, re.MULTILINE)
seconds = seconds.pop().replace('minutes, ', '')

# Create Request
headers = {
    'Content-Type': 'application/json',
}

# Data to send
data = '{ "Name":"Noia Node","Month":"'+month+'","Day":"'+day+'","Time":"'+time+'","Downloaded":"'+downloaded+'","Uploaded":"'+uploaded+'","Hours":"'+hours+'","Minutes":"'+minutes+'","Seconds":"'+seconds+'"}'

# Send Post Request
req = requests.post(endpoint, headers=headers, data=data)