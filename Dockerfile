FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
#FROM selenium/standalone-chrome

# Install manually all the missing libraries
RUN apt-get update
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils
RUN apt-get install -y libappindicator3-1

# Install Chrome
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
COPY google-chrome-stable_current_amd64.deb google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install


RUN mkdir /google
COPY firebase-admin.json /google/firebase-admin.json
ENV GOOGLE_APPLICATION_CREDENTIALS='/google/firebase-admin.json'

#COPY google-requirements.txt google-requirements.txt
COPY requirements.txt requirements.txt

#RUN pip install -r google-requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app
WORKDIR /
