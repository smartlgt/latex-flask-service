# -*- coding: utf-8 -*-
import os
import tempfile
import urllib.parse as urlparse

from flask import Flask, request, abort, Response
from latex import build_pdf

from raven.contrib.flask import Sentry
from raven import Client
from raven.transport import ThreadedRequestsHTTPTransport

from helper import auth

app = Flask(__name__)

SENTRY_DNS = os.environ.get('SENTRY_DNS')

if SENTRY_DNS:
    client = Client(SENTRY_DNS, transport=ThreadedRequestsHTTPTransport)
    sentry = Sentry(app, client=client)

API_KEY = os.environ.get('API_KEY')


@app.route("/", methods=['GET', 'POST'])
@auth(API_KEY)
def pdf():

    if request.method == 'POST':
        tempdirs = []
        dir = None
        try:
            dir = tempfile.TemporaryDirectory()
            for key, file in request.files.items():
                file.save(os.path.join(dir.name, file.filename))


        except Exception as e:
            sentry.client.captureException()
            dir.cleanup()
            abort(400)


        # this builds a pdf-file inside a temporary directory
        try:
            tex = os.path.join(dir.name, "main.tex")
            with open(tex, 'r', encoding="utf-8") as f:
                s = f.read()
            tempdirs.append(dir.name)
            pdf = build_pdf(s, texinputs=tempdirs)

            dir.cleanup()
            return pdf.data
        except Exception as e:
            sentry.client.captureException()
            dir.cleanup()
            #abort(422)
            abort(Response(str(e), status=422))

    abort(405)


#if __name__ == '__main__':
#    app.run(debug=False, host='0.0.0.0')
