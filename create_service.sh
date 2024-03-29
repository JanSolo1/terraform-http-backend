#!/bin/sh

python3 -m venv venv
. ./venv/bin/activate
pip install -r ./requirements.txt

# Define the service content
SERVICE_CONTENT="
[Unit]
Description=Python HTTP Server
After=network.target

[Service]
Type=simple
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/venv/bin/python3 main.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
"

# Write the service content to the service file
echo "${SERVICE_CONTENT}" | sudo tee /etc/systemd/system/http_server.service

# Reload the systemd daemon to recognize the new service
sudo systemctl daemon-reload

sudo systemctl enable --now http_server.service