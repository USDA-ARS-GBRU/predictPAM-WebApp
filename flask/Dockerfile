FROM alpine as builder
RUN apk add --no-cache openssh-client git

ADD github_key /

RUN eval $(ssh-agent) && \
    ssh-add github_key && \
    ssh-keyscan -H github.com >> /etc/ssh/ssh_known_hosts && \
    git clone git@github.com:USDA-ARS-GBRU/predictPAM.git /opt/predictPAM


FROM continuumio/miniconda:latest

COPY . /app
WORKDIR /app

RUN chmod +x ./app/boot.sh

RUN conda env create -f ./app/environment.yml

SHELL ["conda", "run", "-n", "predictenv", "/bin/bash", "-c"]

RUN conda install -c bioconda pysam && \
	conda install flask && \
	conda install requests && \
	conda install -c anaconda libgfortran  && \
	conda install -c anaconda psutil

RUN	pip install pip==9.0.3 pybind11 && \
	pip install -U Werkzeug

RUN pip install nmslib

RUN conda install -c anaconda gunicorn && \
	conda install -c anaconda gevent

COPY --from=builder /opt/predictPAM/ .
RUN  python3 ./setup.py install

RUN echo "source activate predictenv" > ~/.bashrc
ENV PATH /opt/conda/envs/predictenv/bin:$PATH

EXPOSE 8080

ENTRYPOINT ["./app/boot.sh"]