FROM apache/airflow:2.8.0-python3.10

USER root

# Installs required for pyodbc
RUN apt-get update && apt-get install -y unixodbc unixodbc-dev
RUN apt-get upgrade -y
RUN apt-get install -y --no-install-recommends --fix-missing curl
RUN apt-get install -y --no-install-recommends --fix-missing gcc
RUN apt-get install -y --no-install-recommends --fix-missing g++
RUN apt-get install -y --no-install-recommends --fix-missing gnupg
# RUN apt-get install -y --no-install-recommends --fix-missing ffmpeg
RUN apt-get install -y --no-install-recommends --fix-missing libsm6
RUN apt-get install -y --no-install-recommends --fix-missing libxext6
RUN apt-get install -y --no-install-recommends --fix-missing unzip
RUN apt-get install -y --no-install-recommends --fix-missing groff
RUN apt-get install -y --no-install-recommends --fix-missing less
RUN apt-get install -y --no-install-recommends --fix-missing libpq-dev
RUN rm -rf /var/lib/apt/lists/*


USER airflow

# installing requirememnts
ADD requirements.txt .
RUN pip install -r requirements.txt

# Opted for mounting this directory for development, but in "production" env
# COPY /src /opt/airflow/src
# COPY /data /opt/airflow/data
COPY VERSION /opt/airflow

ENV PYTHONPATH=/opt/airflow/