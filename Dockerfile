FROM google/python-runtime
ENTRYPOINT ["/env/bin/python", "/app/redirect/app.py"]
