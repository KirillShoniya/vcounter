FROM python:3.9-alpine

RUN mkdir /code
WORKDIR /code
COPY . /code
COPY ./deployment/docker/entrypoint.sh /code
COPY ./bin/run_server.py /code

RUN echo @edge https://nl.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories && \
    echo @edge https://nl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories

# install build dependencies
RUN apk add --no-cache gcc python3-dev openssl-dev

# install Python environment
RUN ls -la /code && pip3 install --upgrade pip && \
    pip3 install -r requirements.txt && \
    pip3 install /code/dist/vcounter-2021.0.1-py3-none-any.whl

# cleanup
RUN rm -rf /var/cache/* && mkdir /var/cache/apk

RUN ["chmod", "+x", "/code/entrypoint.sh"]

ENTRYPOINT ["/code/entrypoint.sh"]
