FROM python:3.6-jessie
RUN apt update
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD . /app
ENV PORT 8080
ENV FLASK_APP=run.py
ENV SECRET=some-huge-sec
ENV APP_SETTINGS=development
ENV DATABASE_URL=value
ENV MONGO_URI=value
ENTRYPOINT [ "executable" ]
CMD ["python", "run.py"]