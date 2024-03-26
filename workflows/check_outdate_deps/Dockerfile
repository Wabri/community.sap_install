FROM python:3.12-slim

COPY test.py /test.py
RUN chmod +x /test.py

RUN env

RUN pip3 install requests; \
	apt-get update; \
	apt-get install -y --no-install-recommends git

ENTRYPOINT [ "/test.py" ]
