FROM gcr.io/tensorflow/tensorflow:latest-gpu

RUN apt-get update
RUN apt-get install -qq build-essential libssl-dev libffi-dev python-dev curl
RUN pip install Flask azure-storage
RUN sudo apt-get install -qq python-qt4

COPY ./src /code
ADD entry.sh /code/
RUN chmod +x /code/entry.sh

EXPOSE 80

#ENTRYPOINT ["/code/entry.sh"]







