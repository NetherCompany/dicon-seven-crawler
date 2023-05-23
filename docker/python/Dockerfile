##########################
## Builder Container
##########################
FROM python:3.11.3-alpine3.18 as builder

WORKDIR /dicon-seven-crawler

RUN apk update && apk add \
      build-base \
      curl \
      git \
      tzdata \
      chromium \
      chromium-chromedriver \
  && rm -rf /var/cache/apk/*

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

##########################
## Application Container
##########################
FROM python:3.11.3-alpine3.18

WORKDIR /dicon-seven-crawler

RUN apk update && \
    apk add --no-cache \
        build-base \
        curl \
        git \
        tzdata \
        chromium \
        chromium-chromedriver \
        git

COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY . .
