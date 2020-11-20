FROM python:3.8-slim-buster as base_image
WORKDIR /opt
# postgresql-client needed for `wait-for-db.sh` script
RUN apt update && apt install -y make build-essential postgresql-client git
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt --no-cache-dir --no-deps


FROM base_image as dev_image
RUN python -m pip install -r requirements.txt --no-cache-dir
CMD ["make", "run"]


FROM base_image as release_image
COPY . .
CMD ["python", "main.py", "runserver"]
