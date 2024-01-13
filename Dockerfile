FROM python:3.9

WORKDIR .

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./main.py .
COPY ./dataManagement/ ./dataManagement
COPY ./routers/ ./routers
COPY ./services/ ./services
COPY ./auths/ ./auths
COPY ./CountryDataCo2.db .
COPY ./.env .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
