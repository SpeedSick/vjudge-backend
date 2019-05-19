FROM kenenalmat/docker_and_python
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE = core.settings
RUN mkdir /src
COPY src /src
WORKDIR /src
RUN sed -i -e 's/dl-cdn/dl-4/g' /etc/apk/repositories
RUN apk update && apk add bash && apk add sudo
RUN apk add jpeg-dev zlib-dev git openssh
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install --upgrade pip && pip3 install -U -r requirements.txt
CMD bash -c "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"
