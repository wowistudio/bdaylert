FROM python:3.11-slim-bullseye

WORKDIR "/bday"
ENV FOLDER="/bday"
ENV PATH "$FOLDER/code/local/bin:$FOLDER/venv/bin:$PATH"
ENV CODE_SRC_FOLDER "$FOLDER/code/src"
ENV PYTHONPATH "${PYTHONPATH}:$FOLDER/code/src"
ENV SERVICE_NAME "bday"
ENV FZF_DEFAULT_OPTS "--height 50% --layout=reverse --border"
ENV BOTO_DISABLE_COMMONNAME true
# enables entr with docker
ENV ENTR_INOTIFY_WORKAROUND 1

RUN apt-get update && apt-get install -y curl jq fzf vim git entr
RUN mkdir $FOLDER/entrypoints
RUN chown 1000:1000 $FOLDER/entrypoints

# add venv
ENV PYTHONPATH "${PYTHONPATH}:$FOLDER/code/src"
RUN python -mvenv $FOLDER/venv

# copy bashrc file
COPY local/.bashrc /root/.bashrc

# install deps
COPY requirements/* $FOLDER/requirements/
RUN --mount=type=cache,mode=0755,target="/bday/.cache/pip" set -eux; \
   $FOLDER/venv/bin/python -mpip install -r $FOLDER/requirements/dev.txt