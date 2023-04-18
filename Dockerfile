FROM debian:bullseye-slim

#update image to latest version and clear apt lists
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-cryptography \
    && apt-get clean && apt-get autoremove && rm -Rf /var/lib/apt/lists/* && rm -Rf /var/cache/apt && \
    pip3 install jinja2

COPY template_py/template_py.py /usr/local/bin/template.py
RUN chmod +x /usr/local/bin/template.py
