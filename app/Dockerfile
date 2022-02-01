FROM python:3.8

WORKDIR /home/FAngelo94/TravelTipsBackend/

COPY requirements.txt tmp/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev 

RUN pip3 install -r tmp/requirements.txt
RUN pip3 install connexion[swagger-ui]

#CMD python app/app.py
#CMD /bin/bash