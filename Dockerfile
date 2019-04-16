FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
COPY src /src
WORKDIR /src
RUN pip install --upgrade pip && pip install -U -r requirements.txt
CMD bash -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
