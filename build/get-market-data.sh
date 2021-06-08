#!/usr/bin/env bash

while getopts e:d: flag
do
    case "${flag}" in
        e) epochs=${OPTARG};;
        d) baseDir=${OPTARG};;
    esac
done

echo "[FETCH][MARKET_DATA][LATEST]"
docker-compose run --rm freqtrade download-data --exchange binance --days 30 -t 1h