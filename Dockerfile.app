FROM frolvlad/alpine-glibc:alpine-3.7

ENV PROJECT_DIR /opt/kit_campus_puzzle

ADD ./src/kit_campus_puzzle ${PROJECT_DIR}

WORKDIR ${PROJECT_DIR}

RUN apk add --no-cache \
        python3 \
        python3-dev \
        tzdata \
        zlib-dev \
        libjpeg-turbo-dev \
        gcc \
        musl-dev \
        mariadb-dev && \
    pip3 install -r requirements.txt && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del --purge \
        gcc \
        tzdata && \
    rm /usr/lib/libmysqld* && \
    rm -rf /var/cache/apk/*