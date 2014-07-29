import json
from flask import Flask, request

from redir import DataStore

appname = "app"
recordstore = DataStore()

app = Flask(appname)
app.config.from_object(appname)

app.config.update(dict(
    DEBUG=True
))

@app.route('/')
def index():
    return "Welcome to the 301-in-a-Box admin interface!\n"


@app.route('/api/records', methods=['GET'])
def get_records():
    """Get ALIAS records"""
    return json.dumps(recordstore.todict())



@app.route('/api/records', methods=['POST'])
def post_record():
    """Add ALIAS record to database"""
    data = request.get_json()
    record = data['record']
    hostname = record['hostname']
    url = record['url']

    recordstore[hostname] = url
    response = '''
        Record:
        {0}
    '''.format(recordstore[hostname])
    return response

@app.route('/api/records/<record_id>', methods=['PUT'])
def put_record(record_id):
    """Update ALIAS record"""
    return "This will update an ALIAS record\n"

@app.route('/api/records/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    """Delete ALIAS record from the database"""
    return "This will delete an ALIAS record from the database\n"

if __name__ == '__main__':
    app.run()