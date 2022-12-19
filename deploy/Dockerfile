FROM python:3.9-slim-bullseye

ARG ROOT="/bday"
WORKDIR $ROOT

RUN apt-get update && apt-get install -y curl
RUN python -mvenv $ROOT/venv
ENV PATH "$ROOT/venv/bin:$PATH"
ENV PYTHONPATH "$PYTHONPATH:/$ROOT/src"
ENV PATH "$PATH:$ROOT/bin"

COPY build/requirements/* $ROOT/requirements/
RUN --mount=type=cache,mode=0755,target="/root/.cache/pip" set -eux; \
   $ROOT/venv/bin/python -mpip install -r $ROOT/requirements/base.txt

COPY build/bin/ $ROOT/bin/
COPY build/src $ROOT/src
