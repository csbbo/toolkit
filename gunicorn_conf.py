"""
https://docs.gunicorn.org/en/latest/run.html#commonly-used-arguments
"""
import multiprocessing

bind = "0.0.0.0:8000"
workers = (2 * multiprocessing.cpu_count()) + 1
worker_class = "gevent"
loglevel = "warning"
proc_name = "gunicorn_project"
timeout = 300
