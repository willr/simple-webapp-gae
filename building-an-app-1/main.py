# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_render_template]
import datetime
import json
from google.cloud import datastore

from flask import Flask, render_template, request

app = Flask(__name__)

# dont forget to either run in gcloud shell or set a service account (default or new)
datastore_client = datastore.Client()

def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times


@app.route('/postjson', methods = ['POST'])
def post_json_handler():
    if not request.is_json:
        return 'request must contain JSON', 400
    print (request.is_json)
    content = request.get_json()
    print (content)
    return 'JSON posted', 200


@app.route('/json', methods = ['GET'])
def json_out():
    # Store the current access time in Datastore.
    store_time(datetime.datetime.now())

    # Fetch the most recent 10 access times from Datastore.
    times = fetch_times(10)
    
    data = {}
    data['times'] = []
    for time in times:
        data['times'].append(str(time['timestamp']))

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/')
def root():
    # Store the current access time in Datastore.
    store_time(datetime.datetime.now())

    # Fetch the most recent 10 access times from Datastore.
    times = fetch_times(10)

    return render_template(
        'index.html', times=times)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [START gae_python37_render_template]
