# docker build -t fastapi_referall .
# docker run -d --name fastapi_app --rm -p 8000:9000 fastapi_referall (имя образа)
# docker logs name or cash

FROM python:3.9

RUN mkdir /referral

WORKDIR /referral

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN chmod a+x /referral/docker/app.sh


CMD ["gunicorn", "app.main:app", "workers","4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]


# CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]



