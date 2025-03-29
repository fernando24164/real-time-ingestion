# Gunicorn configuration
bind = "0.0.0.0:8000"
workers = 1
loglevel = "info"
errorlog = "-"
accesslog = "-"
capture_output = True