#!/bin/bash
TEMP_PASS=`tr -dc A-Za-z0-9 </dev/urandom | head -c 38 ; echo ''`
sed -i -e "s/POSTGRES_PASSWORD.*/POSTGRES_PASSWORD=$TEMP_PASS/" .anbot-tasks-env
TEMP_PASS=`tr -dc A-Za-z0-9 </dev/urandom | head -c 38 ; echo ''`
sed -i -e "s/ANBOT_USERNAME.*/ANBOT_USERNAME=$TEMP_PASS/" .anbot-matrix-chat-env
TEMP_PASS=`tr -dc A-Za-z0-9 </dev/urandom | head -c 38 ; echo ''`
sed -i -e "s/ANBOT_PASSWORD.*/ANBOT_PASSWORD=$TEMP_PASS/" .anbot-matrix-chat-env
sed -i -e "s/ANBOT_ROOM.*/ANBOT_ROOM=#anarchism:matrix.org/" .anbot-matrix-chat-env
docker compose build
