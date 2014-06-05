#!/bin/bash
# Backs up the OpenShift PostgreSQL database for this application

NOW="$(date +"%Y-%m-%d")"
FILENAME="$OPENSHIFT_DATA_DIR/$OPENSHIFT_APP_NAME.$NOW.dump"
pg_dump -Fc -t $OPENSHIFT_APP_NAME > $FILENAME
