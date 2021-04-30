FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install --upgrade pip setuptools wheel -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r /code/requirements.txt || \
    pip install -r /code/requirements.txt

VOLUME /code/static
VOLUME /code/media
