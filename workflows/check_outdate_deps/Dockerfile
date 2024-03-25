FROM python:3.12-slim

COPY check_outdate_deps.sh /check_outdate_deps.sh
RUN chmod +x /check_outdate_deps.sh

RUN pip3 install requests; \
	apt-get update; \
	apt-get install -y --no-install-recommends git

ENTRYPOINT [ "/check_outdate_deps.sh" ]
