FROM debian:bullseye-slim

#update image to latest version and clear apt lists
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
    && apt-get clean && apt-get autoremove && rm -Rf /var/lib/apt/lists/* && rm -Rf /var/cache/apt && \
    pip3 install tpl.py
