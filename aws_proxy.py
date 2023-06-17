#!/usr/bin/env python3

# Copyright (c) 2023 Cristian Măgherușan-Stanciu <cristi@leanercloud.com>
# Licensed under the Open Software License version 3.0

from flask import Flask, request, Response, send_from_directory
from flask_cors import CORS
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth
from botocore.session import Session
from botocore.httpsession import URLLib3Session
from botocore.credentials import create_credential_resolver
import os, sys

app = Flask(__name__, static_url_path='', static_folder=os.path.join(os.getcwd(), '.well-known'))
CORS(app)  # This will enable CORS for all routes

@app.route('/.well-known/', defaults={'path': ''}, methods=['GET', 'OPTIONS'])
@app.route('/.well-known/<path:path>')
def serve_static(path):
    print(app.static_folder)
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return app.send_static_file('index.html')


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_request(path):
    try:
        aws_profile = sys.argv[1]
        session = Session(profile=aws_profile)
        creds = create_credential_resolver(session).load_credentials()
        aws_service = 'ec2'

        # Extract necessary information from the incoming request
        method = request.method
        payload = request.get_data()
        headers = dict(request.headers)
        params = dict(request.args)

        # Create a botocore AWS request
        aws_request = AWSRequest(method=method,
                                 url=f"https://ec2.amazonaws.com/{path}",
                                 data=payload,
                                 headers=headers,
                                 params=params)

        # Sign the request using SigV4Auth
        SigV4Auth(creds, aws_service, session.get_config_variable('region')).add_auth(aws_request)

        # Forward the request to EC2 API
        response = URLLib3Session().send(aws_request.prepare())

        # Create a new response and return
        return Response(response.content, response.status_code)

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(port=3000)
