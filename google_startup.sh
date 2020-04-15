#!/bin/bash

source venv/bin/activate
export GOOGLE_APPLICATION_CREDENTIALS="`pwd`/firebase-admin.json"

echo "GOOGLE_APPLICATION_CREDENTIALS variable set to: $GOOGLE_APPLICATION_CREDENTIALS"


uvicorn app.main:app --reload
