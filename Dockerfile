FROM python:3.10

ADD client.py .

ADD comm.py .

CMD ["python", "client.py"]
