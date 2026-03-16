# Build:  docker build -t safezip-test .
# Test:   docker run --rm safezip-test
# Env:    docker run --rm safezip-test -e py312
# Shell:  docker run --rm -it --entrypoint bash safezip-test

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Point Python's SSL module to the system CA bundle.
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

# Copy uv binary from the official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install Python versions used in the test matrix
RUN uv python install 3.10 3.11 3.12 3.13 3.14

# Install tox and tox-uv into a uv-managed tool environment
RUN uv tool install tox --with tox-uv

# Make uv tool binaries (tox) available on PATH
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app
COPY . .

ENTRYPOINT ["tox"]
CMD []
