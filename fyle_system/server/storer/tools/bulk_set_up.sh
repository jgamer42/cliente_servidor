#!/bin/bash
for port_to_use in {5996..6001}
do  
    echo $port_to_use
    python main.py --port $port_to_use --host 10.253.22.100 > logs_$port_to_use.log &
done