#!/usr/bin/env bash

while getopts e:d:t: flag
do
    case "${flag}" in
        e) epochs=${OPTARG};;
        d) baseDir=${OPTARG};;
        t) token=${OPTARG};;
    esac
done

echo "[BUILD]"
eval "${baseDir}/build/get-market-data.sh -e $epochs -d \"$baseDir\""
eval "${baseDir}/build/optimize-strategies.sh -e $epochs -d \"$baseDir\""
eval "${baseDir}/build/commit-optimizations.sh -d \"$baseDir\" -t \"$token\""