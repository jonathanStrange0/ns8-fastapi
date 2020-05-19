#!/bin/bash

# run this script after pulling most recent version of repo
# Only run this script on gcloud console

gcloud config set project ns8-traffic-api &&

gcloud config set compute/zone us-central1-c &&
gcloud container clusters get-credentials api-cluster-2 &&
docker build -t gcr.io/ns8-traffic-api/ns8-traffic-api:latest . &&
docker push gcr.io/ns8-traffic-api/ns8-traffic-api:latest &&
kubectl set image deployment/api-app traffic-api=gcr.io/ns8-traffic-api/ns8-traffic-api:latest
