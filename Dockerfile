FROM python:3.9 AS builder
COPY requirements.txt .

RUN pip install --user -r requirements.txt 

FROM python:3.9-slim
WORKDIR /app

COPY --from=builder /root/.local/* /root/.local/
COPY chksftp.py .

ENV PATH=/root/.local:$PATH
ENV PYTHONPATH=/root/.local/python3.9/site-packages
EXPOSE 9816
CMD [ "python", "./chksftp.py"]