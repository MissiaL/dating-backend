FROM docker-proxy.tcsbank.ru/python:3.8-slim-buster as base_image
WORKDIR /app

ENV http_proxy http://proxy.tcsbank.ru:8080
ENV https_proxy http://proxy.tcsbank.ru:8080

# postgresql-client needed for `wait-for-db.sh` script
RUN apt update && apt install -y make build-essential postgresql-client git
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt -i https://registry.tcsbank.ru/repository/pypi.python.org/simple/ --trusted-host registry.tcsbank.ru --no-cache-dir
EXPOSE 4000
CMD ["python", "main.py", "runserver"]

#
#FROM base_image as dev_image
#RUN python -m pip install -r requirements.txt -i https://registry.tcsbank.ru/repository/pypi.python.org/simple/ --trusted-host registry.tcsbank.ru --no-cache-dir
#CMD ["make", "run"]
#
#
#FROM base_image as release_image
#COPY . .
#CMD ["python", "main.py", "runserver"]
