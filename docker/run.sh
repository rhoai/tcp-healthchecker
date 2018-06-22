#!/bin/bash
: ${RUN_COMMAND:='healthcheck'}

export HOST_IP=$(curl http://169.254.169.254/latest/meta-data/local-ipv4)

# start the server
exec $RUN_COMMAND