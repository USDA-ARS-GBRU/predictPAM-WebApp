FROM alpine as builder
RUN apk add --no-cache openssh-client git

ADD github_key /

RUN eval $(ssh-agent) && \
    ssh-add github_key && \
    ssh-keyscan -H github.com >> /etc/ssh/ssh_known_hosts && \
    git clone git@github.com:USDA-ARS-GBRU/predictPAM.git /opt/predictPAM


FROM continuumio/miniconda3

COPY . /app
WORKDIR /app

# Create the environment:
RUN conda env create -f app/environment.yml

SHELL ["conda", "run", "-n", "predictenv", "/bin/bash", "-c"]

RUN conda install -c bioconda pysam
RUN conda install flask
RUN	conda install requests
RUN	conda install -c anaconda libgfortran
RUN conda install -c anaconda psutil
RUN pip install pip==9.0.3 pybind11
RUN	pip install nmslib

RUN pip install -U Werkzeug
COPY --from=builder /opt/predictPAM/ .
RUN  python3 ./setup.py install

EXPOSE 5000

ENTRYPOINT [ "conda", "run", "-n", "predictenv", "python", "./app/app.py" ]