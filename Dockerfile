FROM python:3.6-stretch
WORKDIR /backend
ADD . /backend
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
