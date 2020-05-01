pidfile = 'app.pid'
worker_tmp_dir = '/dev/shm'
worker_class = 'gthread'
workers = 2
worker_connections = 1000
timeout = 500
keepalive = 2
threads = 4
proc_name = 'app'
bind = '0.0.0.0:8080'
backlog = 2048
accesslog = 'server.log'
errorlog = 'server.log'
loglevel = 'info'