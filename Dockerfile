FROM nvidia/cuda:12.2.0-base-ubuntu20.04

RUN mkdir -p /app/log/
WORKDIR /app

RUN apt update && apt upgrade -y && apt install -y python3
RUN apt install -y python3-pip

# install required python packages
COPY requirements.txt /app/requirements.txt
RUN python3 -m pip install -r requirements.txt

# download / install the model
COPY install.py /app/install.py
RUN python3 /app/install.py

# copy server runner
COPY server.py /app/server.py

# start the server
# CMD ["sleep", "5000"]
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--timeout", "120", "--threads", "1", "server:app"]
