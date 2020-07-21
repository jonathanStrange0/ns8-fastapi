#!/bin/bash

gcloud auth login && 
gcloud auth configure-docker &&
docker build -t gcr.io/traffic-generation-api/ns8-traffic-api:latest . &&
docker push gcr.io/traffic-generation-api/ns8-traffic-api:latest
