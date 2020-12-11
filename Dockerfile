FROM python:3.8-slim

RUN apt-get -qqy update && apt-get install --no-install-recommends -qqy curl \
    && rm -rf /var/lib/apt/lists/*

# -- Install Poetry
ENV POETRY_VERSION=1.1.4
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH="/root/.poetry/bin:${PATH}"

RUN mkdir /app
WORKDIR /app

# -- Install python dependencies
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false --local
RUN poetry install -v --no-dev \
    && rm -rf /root/.cache \
    && find /usr/local/src/ -type d -name .git -exec rm -rf '{}' +

## Install App
COPY . ./

ENTRYPOINT ["python", "manage.py", "runserver"]
