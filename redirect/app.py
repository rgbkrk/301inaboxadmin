import json
import os
from flask import Flask, request

from redir import DataStore
from redir import RedisDataStore

appname = "app"
if (os.environ.get('REDIS_PORT_6379_TCP_ADDR') and
    os.environ.get('REDIS_PORT_6379_TCP_PORT')):
    recordstore = RedisDataStore()
else:
    recordstore = DataStore()

app = Flask(appname)
app.config.from_object(appname)

app.config.update(dict(
    DEBUG=True,
))

@app.route('/')
def index():
    return "Welcome to the 301-in-a-Box admin interface!\n"


@app.route('/api/records', methods=['GET'])
def get_records():
    """Get ALIAS records"""
    return json.dumps(recordstore.todict())

@app.route('/api/records/<record_id>', methods=['GET'])
def get_record(record_id):
    if record_id and record_id in recordstore:
        record = {}
        record[record_id] = recordstore[record_id]
        return json.dumps(record)
    else:
        return "No such record exists.\n"


@app.route('/api/records', methods=['POST'])
def post_record():
    """Add ALIAS record to database"""
    data = request.get_json()
    if not data:
        return "Error: Invalid JSON.\n"
    record = data['record']
    hostname = record['hostname']
    url = record['url']

    recordstore[hostname] = url
    response = '''
        Record created:
        {0} -> {1}
    '''.format(hostname, recordstore[hostname])
    return response


@app.route('/api/records/<record_id>', methods=['PUT'])
def put_record(record_id):
    """Update ALIAS record"""
    return "This will update an ALIAS record\n"


@app.route('/api/records/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete ALIAS record from the database"""
    if record_id in recordstore:
        record = {}
        record[record_id] = recordstore[record_id]
        del recordstore[record_id]
        return "Deleted record: {0}\n".format(json.dumps(record))
    else:
        return "No such record exists.\n"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
