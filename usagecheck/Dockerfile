FROM ghcr.io/osgeo/gdal:ubuntu-full-latest

WORKDIR /src

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    git \
    libsqlite3-dev \
    python3-pip \
    python3-venv \
    zip \
    zlib1g-dev \
    jq \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY src/* .

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]