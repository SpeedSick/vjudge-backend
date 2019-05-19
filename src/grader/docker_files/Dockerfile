FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
COPY . /src
WORKDIR /src
RUN pip install --upgrade pip && pip install -U -r requirements.txt
CMD bash -c "export FLASK_APP=app.py && python -m flask run --host=0.0.0.0 --port=5000"
