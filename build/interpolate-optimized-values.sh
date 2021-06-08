#!/usr/bin/env bash

while getopts m:f:r:d: flag
do
    case "${flag}" in
        m) mark=${OPTARG};;
        f) filePath=${OPTARG};;
        r) response=${OPTARG};;
        d) baseDir=${OPTARG};;
    esac
done

savePath="${baseDir}/automation/optimizations/fa_m${mark}_strategy.txt"

echo "[INTERPOLATE][STRATEGIES][MARK][$mark]"
echo "[INTERPOLATE][STRATEGIES][SAVE][$savePath]"

echo "$response" | tee "$savePath"

function split_string() {
    str=$1
    delimiter=$2
    s=$str$delimiter
    array=()

    while [[ $s ]];
    do
        array+=("${s%%"$delimiter"*}");
        s=${s#*"$delimiter"};
    done;

    declare -p array
}

#       Calculate daily average
#       Get average transaction time
#       Get new ROI, stoploss, buy and sell parameters.
#       Persist the above to the strategy file.