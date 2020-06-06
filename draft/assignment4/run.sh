#!/bin/bash

DATASET=(
u1
u2
u3
u4
u5
)

for data in ${DATASET[@]}; do
    echo -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    echo "Press [Enter] key to start ${data} test..."
    echo -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    read
    ./bin/recommender ./data/${data}.base ./data/${data}.test
done

