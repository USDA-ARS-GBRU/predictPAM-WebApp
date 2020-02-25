# this is our first build stage, it will not persist in the final image
FROM ubuntu as intermediate

# install git
RUN apt-get update
RUN apt-get install -y git

# add credentials on build
ARG SSH_PRIVATE_KEY
RUN mkdir /root/.ssh/
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa

# make sure your domain is accepted
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts

RUN git clone git@github.com:USDA-ARS-GBRU/predictPAM.git


FROM ubuntu:16.04

MAINTAINER Anushka Swarup "aswarup@ufl.edu"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    pip install --upgrade pip

COPY . /app

WORKDIR ./app

RUN pip install -r ./app/requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]

# copy the repository form the previous image
COPY --from=intermediate /your-repo /srv/your-repo
# ... actually use the repo :)






