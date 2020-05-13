#!/bin/bash
# Build docker containier for deployment
docker build -t ns8-traffic-api .
gcloud config set project ns8-traffic-api
gcloud builds submit --tag gcr.io/ns8-traffic-api/ns8-traffic-api
# gcloud beta run deploy myimage --image gcr.io/ns8-traffic-api/ns8-traffic-api --region us-central1 --platform managed
