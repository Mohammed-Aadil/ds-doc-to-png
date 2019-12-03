From python:3.7-alpine
MAINTAINER Mohammed Aadil "mailtoaadilhanif@gmail.com"
RUN apk update && apk add build-base python-dev py-pip jpeg-dev zlib-dev imagemagick imagemagick-dev
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirements.txt /app/doc_to_png/

WORKDIR /app/doc_to_png
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
EXPOSE 5000
