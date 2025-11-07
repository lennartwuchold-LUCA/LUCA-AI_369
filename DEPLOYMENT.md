# 🚀 LUCA AI Deployment Guide

## Production Deployment Checklist

### 1. Security Hardening

#### Environment Variables
```bash
# .env production settings

# REQUIRED: Strong secret key (NOT the default!)
SECRET_KEY=<generate-strong-64-char-random-string>

# REQUIRED: Your Anthropic API key
ANTHROPIC_API_KEY=<your-api-key>

# Database (consider PostgreSQL for production)
DATABASE_URL=postgresql://user:pass@localhost/luca_db

# Server settings
HOST=0.0.0.0
PORT=8000
DEBUG=False  # IMPORTANT: Set to False!

# Admin credentials (CHANGE THESE!)
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=<strong-unique-password>

# CORS (restrict to your domain)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

#### Generate Strong Keys
```bash
# Secret key
python -c 'import secrets; print(secrets.token_hex(32))'

# Admin password
python -c 'import secrets; print(secrets.token_urlsafe(32))'
```

### 2. Database Configuration

#### SQLite (Development/Small Scale)
```bash
DATABASE_URL=sqlite:///./luca.db
```

#### PostgreSQL (Production Recommended)
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb luca_db
sudo -u postgres createuser luca_user

# Set password
sudo -u postgres psql
postgres=# ALTER USER luca_user WITH PASSWORD 'strong_password';
postgres=# GRANT ALL PRIVILEGES ON DATABASE luca_db TO luca_user;

# Update .env
DATABASE_URL=postgresql://luca_user:strong_password@localhost/luca_db

# Install Python driver
pip install psycopg2-binary
```

### 3. Web Server Setup (Nginx + Gunicorn)

#### Install Gunicorn
```bash
pip install gunicorn
```

#### Create systemd service
```bash
sudo nano /etc/systemd/system/luca.service
```

```ini
[Unit]
Description=LUCA AI Backend
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/luca
Environment="PATH=/var/www/luca/venv/bin"
ExecStart=/var/www/luca/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 127.0.0.1:8000 backend.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Start service
```bash
sudo systemctl daemon-reload
sudo systemctl enable luca
sudo systemctl start luca
sudo systemctl status luca
```

#### Install Nginx
```bash
sudo apt-get install nginx
```

#### Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/luca
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        root /var/www/luca/frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support (if needed)
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

#### Enable site
```bash
sudo ln -s /etc/nginx/sites-available/luca /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 4. SSL/HTTPS Setup (Let's Encrypt)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
# Test renewal:
sudo certbot renew --dry-run
```

### 5. Firewall Configuration

```bash
# Install UFW
sudo apt-get install ufw

# Allow SSH
sudo ufw allow ssh

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### 6. Frontend Configuration

Update API URL in frontend files:

#### frontend/login.html
```javascript
const API_URL = 'https://yourdomain.com';  // Change from localhost
```

#### frontend/chat.html
```javascript
const API_URL = 'https://yourdomain.com';  // Change from localhost
```

### 7. Monitoring and Logging

#### Setup Log Rotation
```bash
sudo nano /etc/logrotate.d/luca
```

```
/var/www/luca/logs/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

#### Monitor Service
```bash
# View logs
sudo journalctl -u luca -f

# Check status
sudo systemctl status luca

# Restart if needed
sudo systemctl restart luca
```

### 8. Backup Strategy

#### Database Backup Script
```bash
nano /var/www/luca/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/luca"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
if [ "$DATABASE_URL" == "sqlite"* ]; then
    cp /var/www/luca/luca.db $BACKUP_DIR/luca_$DATE.db
else
    pg_dump luca_db > $BACKUP_DIR/luca_$DATE.sql
fi

# Backup .env
cp /var/www/luca/.env $BACKUP_DIR/env_$DATE.backup

# Keep only last 30 days
find $BACKUP_DIR -name "luca_*.db" -mtime +30 -delete
find $BACKUP_DIR -name "luca_*.sql" -mtime +30 -delete

echo "Backup completed: $DATE"
```

```bash
chmod +x /var/www/luca/backup.sh
```

#### Schedule Daily Backups
```bash
sudo crontab -e
```

```
# Daily backup at 2 AM
0 2 * * * /var/www/luca/backup.sh >> /var/log/luca_backup.log 2>&1
```

### 9. Performance Optimization

#### Backend (config.py)
```python
# Production settings
DEBUG = False
WORKERS = 4  # Adjust based on CPU cores
WORKER_CONNECTIONS = 1000
KEEPALIVE = 5
```

#### Database Indexing
```python
# Add indexes for frequently queried fields
# Already configured in models.py
```

#### Caching (Optional)
```bash
# Install Redis
sudo apt-get install redis-server

# Python client
pip install redis

# Update requirements.txt
echo "redis==5.0.0" >> requirements.txt
```

### 10. Meshtastic Production Setup

If deploying Meshtastic gateway:

```bash
# Install Meshtastic
pip install meshtastic

# Configure for production
MESHTASTIC_ENABLED=True
MESHTASTIC_INTERFACE=serial
MESHTASTIC_PORT=/dev/ttyUSB0

# Add user to dialout group
sudo usermod -a -G dialout www-data

# Configure systemd service to access USB
# Edit /etc/systemd/system/luca.service
# Add: SupplementaryGroups=dialout
```

### 11. Health Checks

#### Setup Health Check Endpoint
Already available at: `https://yourdomain.com/health`

#### Monitor with Uptime Robot or Similar
- Create account at uptimerobot.com
- Add monitor for: https://yourdomain.com/health
- Set alert email

### 12. Rate Limiting (Optional)

#### Install slowapi
```bash
pip install slowapi
```

#### Add to backend/main.py
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add to endpoints
@app.post("/api/chat")
@limiter.limit("10/minute")  # Max 10 requests per minute
async def chat(...):
    ...
```

### 13. Cost Optimization

#### Anthropic API Usage
```python
# Monitor token usage
# Set up alerts for high usage
# Consider caching common responses
# Implement token budgets per user
```

#### Estimate Monthly Costs
```
Claude API: ~$0.003 per 1000 tokens
Average query: ~500 tokens
100 queries/day: ~$0.15/day = ~$4.50/month

Server costs:
- VPS (2GB RAM): $5-10/month
- Domain: $10-15/year
- SSL: Free (Let's Encrypt)

Total: ~$10-20/month
```

### 14. Disaster Recovery

#### Backup Restoration
```bash
# Restore database
if [ "$DATABASE_URL" == "sqlite"* ]; then
    cp /var/backups/luca/luca_YYYYMMDD.db /var/www/luca/luca.db
else
    psql luca_db < /var/backups/luca/luca_YYYYMMDD.sql
fi

# Restore .env
cp /var/backups/luca/env_YYYYMMDD.backup /var/www/luca/.env

# Restart service
sudo systemctl restart luca
```

### 15. Deployment Checklist

Before going live:

- [ ] Strong SECRET_KEY generated
- [ ] Admin password changed
- [ ] DEBUG=False
- [ ] CORS restricted to your domain
- [ ] HTTPS configured
- [ ] Firewall enabled
- [ ] Database backed up
- [ ] Logs configured
- [ ] Health checks working
- [ ] API keys secured
- [ ] Frontend API URLs updated
- [ ] Service auto-starts on boot
- [ ] Monitoring configured
- [ ] Backup script scheduled

### 16. Quick Deployment Commands

```bash
# Clone repository
git clone https://github.com/lennartwuchold-LUCA/LUCA-AI_369.git
cd LUCA-AI_369

# Setup environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.template .env
nano .env  # Edit configuration

# Initialize database
python backend/database.py

# Test locally
python -m backend.main

# Deploy to production (see sections above)
```

### 17. Docker Deployment (Alternative)

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./luca.db:/app/luca.db
    restart: unless-stopped

  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./frontend:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    restart: unless-stopped
```

```bash
# Deploy with Docker
docker-compose up -d
```

### 18. Support

For deployment issues:
- GitHub: [LUCA-AI_369](https://github.com/lennartwuchold-LUCA/LUCA-AI_369)
- Email: wucholdlennart@gmail.com

---

**Remember:**
- Security first!
- Test before deploying
- Keep backups
- Monitor everything
- Update regularly

**369! 🚀🧬⚡**
