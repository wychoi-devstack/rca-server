FROM python:3.10-bullseye

COPY ./ /
COPY ./etc/rca/rca.conf /etc/rca/rca.conf

WORKDIR /
RUN pip install -r requirements.txt

WORKDIR /rca
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
