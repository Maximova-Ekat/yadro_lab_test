FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y python3 python3-pip openssh-client ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY tests/ /app/tests/
CMD ["pytest", "-v", "--maxfail=1", "--disable-warnings"]