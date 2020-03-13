FROM alpine as builder
RUN apk add --no-cache openssh-client git

COPY github_key .

RUN eval $(ssh-agent) && \
    ssh-add github_key && \
    ssh-keyscan -H github.com >> /etc/ssh/ssh_known_hosts && \
    git clone git@github.com:USDA-ARS-GBRU/predictPAM.git /opt/predictPAM

WORKDIR /opt/predictPAM



FROM ubuntu:16.04

MAINTAINER Anushka Swarup "aswarup@ufl.edu"

RUN apt-get update && apt-get install -y \
	python-pip python-dev \
	build-essential libssl-dev libffi-dev\
    libxml2-dev libxslt1-dev zlib1g-dev \
    && pip install --upgrade pip

COPY . /app

WORKDIR ./app

RUN pip install pip==9.0.3 pybind11

RUN pip install -r ./app/requirements.txt

COPY --from=builder /opt/predictPAM/ .
EXPOSE 80

ENTRYPOINT [ "python" ]

CMD [ "./app/app.py" ]







