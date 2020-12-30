# builder image
FROM python:3-alpine as builder
COPY . /code/

WORKDIR /code

RUN python setup.py bdist_wheel --dist-dir=/tmp/dist/

# Final image
FROM python:3-alpine

ENV KANBANDASH_DATABASE_URL=

COPY --from=builder /tmp/dist/kanbandash*.whl /tmp/

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install /tmp/kanbandash*.whl --no-cache-dir && \
    apk --purge del .build-deps && \
    rm -fR /tmp/kanbandash*.whl
