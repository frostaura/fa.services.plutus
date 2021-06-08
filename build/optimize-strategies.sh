#!/usr/bin/env bash

while getopts e:d: flag
do
    case "${flag}" in
        e) epochs=${OPTARG};;
        d) baseDir=${OPTARG};;
    esac
done

stratDir="${baseDir}/user_data/strategies"

echo "[OPTIMIZE][STRATEGIES][EPOCHS][$epochs]"
echo "[OPTIMIZE][STRATEGIES][LOAD][$stratDir]"

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

for FILE in `ls ${stratDir}/*`;
do 
    # Get file path name and content.
    filePath=$FILE
    content=$(cat $filePath)

    # Run regex to extract strat name.
    markPatt='FrostAuraM.+Strategy\('
    [[ $content =~ $markPatt ]]
    mark=${BASH_REMATCH[0]/Strategy\(/}
    mark=${mark/FrostAuraM/}

    # Only process optimizations for strategies that matches our strict naming standards and gracefully ignore the rest.
    if [ "$mark" ]; then
        echo "[OPTIMIZE][STRATEGIES][MARK][$mark]"

        str=$(docker-compose run --rm freqtrade hyperopt --config user_data/config.json -e $epochs --strategy FrostAuraM${mark}Strategy --hyperopt FrostAuraM${mark}HyperOpt --hyperopt-loss OnlyProfitHyperOptLoss -i 1h)
        delimiter="Best result:"
        split_string "$str" "$delimiter"
        eval "${baseDir}/build/interpolate-optimized-values.sh -m \"$mark\" -f \"$filePath\" -r \"${array[1]}\" -d \"$baseDir\""
    fi
done