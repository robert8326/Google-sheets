FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /code/

COPY . /code/

RUN chmod a+x /code/*.sh
ENTRYPOINT ["/code/entrypoint.sh"]