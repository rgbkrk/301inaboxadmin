import json
import os
import textwrap

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


def start():
    app.run(host='0.0.0.0', port=8080)


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
        record = dict()
        record['hostname'] = record_id
        record['url'] = recordstore[record_id]
        return json.dumps(record)
    else:
        return "No such record exists.\n"


@app.route('/api/records', methods=['POST'])
def post_records():
    """Add ALIAS record, or multiple records, to database"""
    data = request.get_json()
    if not data:
        return "Error: Invalid JSON.\n"

    addrecords = []

    if 'records' in data and type(data['records']) is list:
        addrecords.extend(data['records'])
    else:
        return "Error: Missing/Invalid field 'records'"

    response = "Records created:\n[\n"

    # Add all records to storage
    for record in addrecords:
        hostname = record['hostname']
        url = record['url']

        # Check for redirect cycle
        if _creates_cycle(hostname, url):
            response += "\tError: {0} -> {1} not added " \
                        "(would cause cycle)".format(hostname, url)
        else:
            recordstore[hostname] = url
            response += "\t{0} -> {1}\n".format(hostname, url)

    response += "]\n"
    response = textwrap.dedent(response)

    return response


@app.route('/api/records/<record_id>', methods=['PUT'])
def put_record(record_id):
    """Update ALIAS record"""
    return "This will update an ALIAS record\n"


@app.route('/api/records/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete ALIAS record from the database"""
    if record_id in recordstore:
        record = dict()
        record['hostname'] = record_id
        record['url'] = recordstore[record_id]
        del recordstore[record_id]
        return "Deleted record: {0}\n".format(json.dumps(record))
    else:
        return "No such record exists.\n"


def _creates_cycle(hostname, url):
    """
    Checks if adding a record redirecting hostname to url
    would cause a redirect cycle
    :return: True if cycle would be created, false otherwise
    """
    currname = url
    while currname in recordstore:
        if currname == hostname:
            return True
    return False

if __name__ == '__main__':
    start()
