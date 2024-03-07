FROM python:3.11.6-slim as builder

RUN useradd -m app && mkdir /app && chown -R app /app
RUN apt update && apt install -y  \
    libpq5 \
    git \
    gcc \
    libgmp3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

FROM builder

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m venv /app/venv  \
    && /app/venv/bin/pip install --no-cache-dir -U pip \
    && /app/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
WORKDIR /app/
RUN chmod +x start.sh
RUN /app/venv/bin/pip install -e .

ENV PATH="/app/venv/bin/:${PATH}"
ENV MODULE_NAME=meet.main
ENV SERVICE_NAME=meet
ENV MAX_WORKERS=2

USER app

CMD ["./start.sh"]
