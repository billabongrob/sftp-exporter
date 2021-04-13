import os, time, logging, pysftp
from prometheus_client import start_http_server, generate_latest, Gauge
from flask import Flask, send_file, request, Response

logger  = logging.getLogger(__name__)
app     = Flask(__name__)
CONTENT_TYPE_LATEST = str('text/plain; version=0.0.4; charset=utf-8')

myHostname = os.environ['SFTPHOST']
myUsername = os.environ['SFTPUSER']
myPassword = os.environ['SFTPPASS']
if 'FILENAME' in os.environ:
    randomFile = os.environ['FILENAME']
else:
    randomFile = "testfile.bin"

# Create a metric to track time spent and requests made.
AUTH_SUCCESS = Gauge('sftp_auth_success', 'Whether authentication succceeded',['sftp_host'])
TIME_TO_AUTH = Gauge('sftp_auth_seconds', 'Amount of time to authenticate',['sftp_host'])
TRANSFER_SUCCESS = Gauge('sftp_transfer_success', 'Whether transfer succceeded',['sftp_host'])
TIME_TO_TRANSFER = Gauge('sftp_transfer_seconds', 'Amount of time to transfer 5M file',['sftp_host'])

# Decorate function with metric.
def process_request():
    auth_duration = 0
    auth_success_value = 0
    file_success = 0
    file_duration_value = 0
    try:
        beginSFTP = time.time()
        # Hacky workaround to get it working in containers
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None 
        with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts, log=True) as sftp:
            endConnection = time.time()
            auth_success_value = 1
            auth_duration = endConnection-beginSFTP
            
            # Create a Random 5 MB file
            with open(randomFile, 'wb') as fout:
                fout.write(os.urandom(5242880))

            # We've established a connection, now put a file
            localFilePath = randomFile
            remoteFilePath = randomFile

            # Start Time to put a file
            startPutFile = time.time()
            if sftp.put(localFilePath, remoteFilePath):
                file_success = 1

            endPutFile = time.time()
            file_duration_value = endPutFile-startPutFile

    except:
        pass

    AUTH_SUCCESS.labels(myHostname).set(auth_success_value)
    TRANSFER_SUCCESS.labels(myHostname).set(file_success)
    TIME_TO_AUTH.labels(myHostname).set(auth_duration)
    TIME_TO_TRANSFER.labels(myHostname).set(file_duration_value)
# END process_request()

# Mini server to replicate prometheus norms
@app.route('/metrics', methods=['GET'])
def get_data():
    """Returns all data as plaintext."""
    process_request()
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/', methods=['GET'])
def show_home():
    output = """<html>
            <head><title>SFTP Exporter</title></head>
            <body>
            <h1>SFTP Exporter</h1>
            <p><a href="/metrics">Metrics</a></p>
            </body>
            </html>"""
    return Response(output)
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9816)