### API Key Security

description
- sample endpoint with api key and signature security

endpoint
- http://localhost:8000/api/private 
- POST Request

header
- X-API-KEY
- X-SIGNATURE
- Content-Type

### Installation

# setup venv
```bash
cd Python_Endpoint-with-Sign-Security
python -m venv venv
venv\Scripts\activate
```

# install dependencies
```bash
pip install --no-index --find-links=Packages fastapi
pip install --no-index --find-links=Packages uvicorn
```

### How to Run

# run server
```bash
uvicorn Server:app --host [IP_ADDRESS] --port 8000 --reload
```

# run client
```bash
python Client.py
```

### Setup Linux VPS

## setup nginx
```bash
sudo apt update
sudo apt install nginx -y

sudo systemctl start nginx
sudo systemctl enable nginx
```

# setup config nginx
```bash
sudo nano /etc/nginx/sites-available/default
```

```bash
server {
    listen 80;

    server_name 103.103.23.46;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# test config
sudo nginx -t

# reload nginx
sudo systemctl reload nginx
```
## Make service
```bash
sudo nano /etc/systemd/system/fastapi.service
```
```bash
[Unit]
Description=FastAPI App
After=network.target

[Service]
User=botegar
Group=botegar
WorkingDirectory=/home/botegar/BotTrading

ExecStart=/home/botegar/BotTrading/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000

Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
# start service
sudo systemctl start fastapi

# enable service
sudo systemctl enable fastapi

# check status
sudo systemctl status fastapi
```

"# Python_Endpoint-with-Sign-Security" 
