#!/bin/bash

docker container stop mycontainer1
docker container rm mycontainer1
docker build -t fasttest .
docker run -d --name mycontainer1 -p 80:80 fasttest
docker ps -a

firefox --new-window 127.0.0.1/docs
