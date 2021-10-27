#! /usr/bin/env bash

# key file from 
# gcloud iam service-accounts keys create service_account.key.json --iam-account simple-webapp-269621@appspot.gserviceaccount.com

export GOOGLE_APPLICATION_CREDENTIALS="$HOME/Development/python/simple-webapp-gae/service_account.key.json"
