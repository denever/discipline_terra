FROM python:3.8-slim
RUN apt-get update && apt-get install curl gdal-bin libgdal-dev -qqy\
    && rm -rf /var/lib/apt/lists/*

# -- Install Poetry
ENV POETRY_VERSION=1.1.4
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH="/root/.poetry/bin:${PATH}"

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN mkdir /app
WORKDIR /app

# -- Install python dependencies
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false --local
RUN poetry install -v --no-dev \
    && rm -rf /root/.cache \
    && find /usr/local/src/ -type d -name .git -exec rm -rf '{}' +

COPY . /app

ENTRYPOINT ["poetry", "run", "python", "manage.py"]
