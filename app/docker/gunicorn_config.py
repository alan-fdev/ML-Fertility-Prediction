"""
Gunicorn Configuration for Production
"""
import os
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "fertility-pro"

# Server mechanics
daemon = False
pidfile = "logs/gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (Uncomment when using HTTPS)
# keyfile = "/etc/ssl/private/fertility-pro.key"
# certfile = "/etc/ssl/certs/fertility-pro.crt"
# ca_certs = "/etc/ssl/certs/ca-bundle.crt"

# Application
raw_env = [
    "FLASK_ENV=production",
    "FLASK_DEBUG=False"
]

# Hook functions
def post_worker_init(worker):
    """Called after worker is initialized"""
    pass

def on_starting(server):
    """Called when Gunicorn starts"""
    pass

def on_exit(server):
    """Called when Gunicorn exits"""
    pass
