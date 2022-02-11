# SFTP Exporter
### Something to keep an eye on SFTP
---
The code included is a small Python web server based on Flask and presents data in an easy to use manner for consumption by Prometheus.  The exporter attempts a connection to an SFTP server, generates a 5M binary file with random content and attempts to put the file on the SFTP server of your choice.  In order to run this you'll need to build the docker container and set the following environment variables when run:

* **SFTPHOST** eg. sftp.hostname.com *Required*
* **SFTPUSER** eg. mysecureuser *Required*
* **SFTPPASS** eg. mysecurepassword *Required*
* **FILENAME** eg. azure-south-central.bin *Optional*
* **WEBPORT** eg. 1985 - defaults to 9816 *Optional*


## Docker

A Dockerfile is provided for convenience if you prefer to build and analyze. You are also welcome to use the command below to pull from this GitHub registry:

```
docker run -p 9816:9816 ghcr.io/billabongrob/sftp-exporter:latest --env SFTPHOST=sftp.hostname.com --env SFTPUSER=mysecureuser --env SFTPPASS=mysecurepassword
```