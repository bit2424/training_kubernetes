FROM python:alpine3.12
WORKDIR /app 
COPY . /app
RUN pip install -r requirements.txt
ENV PRODUCTION=true
EXPOSE 5000
CMD python ./src/launch.py

#COPY requirements.txt /app/requirements.txt
#ENTRYPOINT ["python", "./launch.py"]
