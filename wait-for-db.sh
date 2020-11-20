#!/bin/sh
# @See https://docs.docker.com/compose/startup-order/
set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "psql: unavailable, waiting"
  sleep 1
done

>&2 echo "psql: available, executing command"
exec $cmd
