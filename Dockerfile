FROM python:3.9 AS builder
COPY requirements.txt .

RUN pip install --user -r requirements.txt 

FROM python:3.11.0b1-slim-buster
WORKDIR /app
COPY --from=builder /root/.local/* /app/.local/
COPY chksftp.py .

ENV PATH=/app/.local:$PATH
ENV PYTHONPATH=/app/.local/python3.9/site-packages
RUN adduser sftpuser && chown -R sftpuser /app
USER sftpuser
EXPOSE 9816
CMD [ "python", "chksftp.py"]