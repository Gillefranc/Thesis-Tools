FROM debian:bookworm-slim

RUN apt-get update && \
  apt-get install -y --no-install-recommends stress-ng ca-certificates && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["stress-ng", "--cpu", "4"]
