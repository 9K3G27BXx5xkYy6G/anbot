#!/bin/bash
TEMP_PASS=`tr -dc A-Za-z0-9 </dev/urandom | head -c 38 ; echo ''`
sed -i -e "s/POSTGRES_PASSWORD.*/POSTGRES_PASSWORD=$TEMP_PASS/" .anbot-matrix-chat-env
sed -i -e "s/POSTGRES_PASSWORD.*/POSTGRES_PASSWORD=$TEMP_PASS/" .anbot-tasks-env
docker compose build
