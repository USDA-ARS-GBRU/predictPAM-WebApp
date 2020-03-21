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
RUN ls
RUN conda config --set restore_free_channel true
RUN conda env create -f app/env.yml python=3.7.3

RUN conda install -c anaconda libgfortran
RUN conda install -c anaconda appnope

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

RUN pip3 install pip==9.0.3 pybind11
RUN pip3 install -r ./app/requirements.txt

COPY --from=builder /opt/predictPAM/ .
RUN  python3 ./setup.py install

EXPOSE 5000

ENTRYPOINT [ "conda", "run", "-n", "myenv", "python", "./app/app.py" ]