#!/usr/bin/env bash

while getopts d: flag
do
    case "${flag}" in
        d) baseDir=${OPTARG};;
    esac
done

echo "[OPTIMIZE][STRATEGIES][COMMITTING]"