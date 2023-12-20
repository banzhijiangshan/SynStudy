#!/bin/bash

num_processes=16

send_requests() {
    local counter=0
    while true; do
        local name="user$1_$counter"
        local email="email$1_$counter@example.com"

        curl -X POST http://192.168.31.217:8080/register \
            -H "Content-Type: application/json" \
            -d "{\"name\":\"$name\",\"password\":\"123456\",\"email\":\"$email\"}"

        ((counter++))
        #sleep 0.1
    done
}

for i in $(seq 1 $num_processes); do
    send_requests "$i" &
done

wait
