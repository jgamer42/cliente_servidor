#!/bin/bash

HOST="localhost"
STARTING_PORT=""
HOW_MANY=""
usage() {
  echo "Usage: $0 [--host <host>] [--starting_port <starting_port>] [--how_many <how_many>]"
  exit 1
}

# Comprobamos si se han proporcionado los parámetros necesarios
while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)
      HOST="$2"
      shift 2
      ;;
    --starting_port)
      STARTING_PORT="$2"
      shift 2
      ;;
    --how_many)
      HOW_MANY="$2"
      shift 2
      ;;
    *)
      usage
      ;;
  esac
done

# Comprobamos si se han proporcionado todos los parámetros requeridos
if [[ -z $HOST ||  -z $STARTING_PORT || -z $HOW_MANY ]]; then
  usage
fi
python main.py --host $HOST --name S1 --port $STARTING_PORT --first --logs S1.log &
PREDECESORR="$HOST:$STARTING_PORT"
STARTING_PORT=$(($STARTING_PORT+1))
# Creamos el anillo
j=1
for (( i=$STARTING_PORT; i<($STARTING_PORT+$HOW_MANY); i++ )); do
    j="$(($j+1))"
    PREDECESORR="$HOST:$(($i-1))"
    PORT=$i
    python main.py --host $HOST --name S$j --port $PORT --predecessor $PREDECESORR --logs S$j.log &
done



