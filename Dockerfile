FROM python:3.7-slim
LABEL maintainer="Goobox <perdy@perdy.io>"

ENV LC_ALL='C.UTF-8' PYTHONIOENCODING='utf-8'
ENV APP=goobox-nodes-api
ENV BASEDIR=/srv/apps/$APP
ENV APPDIR=$BASEDIR/app
ENV LOGDIR=$BASEDIR/logs
ENV PYTHONPATH=$APPDIR:$PYTHONPATH

# Install system dependencies
ENV RUNTIME_PACKAGES supervisor nginx
RUN apt-get update && \
    apt-get install -y $RUNTIME_PACKAGES && \
    rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/*

# Create initial dirs
RUN mkdir -p $APPDIR $LOGDIR
WORKDIR $APPDIR

# Install python requirements
ENV BUILD_PACKAGES build-essential libsqlite3-dev
COPY pyproject.toml poetry.lock $APPDIR/
RUN apt-get update && \
    apt-get install -y $BUILD_PACKAGES && \
    python -m pip install --no-cache-dir --upgrade pip poetry && \
    poetry install && \
    apt-get purge -y --auto-remove $BUILD_PACKAGES && \
    apt-get clean && \
    rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/*

# Copy application
COPY . $APPDIR

ENTRYPOINT ["poetry", "run", "python", "-m", "goobox_nodes_api"]
