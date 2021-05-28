!/bin/sh

while getopts e:d: flag
do
    case "${flag}" in
        e) epochs=${OPTARG};;
        # Should be '../user_data/strategies' for local testing.
        d) stratDir=${OPTARG};;
    esac
done

echo "Initialing hyperopts for all strategies with $epochs epochs."
echo "Reading strategies from $stratDir."

for FILE in "${stratDir}/*";
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
        echo "Optimizing Mark $mark"
        #docker-compose run --rm freqtrade hyperopt --config user_data/config.json -e $epochs --strategy FrostAuraM${mark}Strategy --hyperopt FrostAuraM${mark}HyperOpt --hyperopt-loss OnlyProfitHyperOptLoss -i 1h
        
        # TODO: Make the below its own script.
        #   Read latest hyperopts results
        #       Calculate daily average
        #       Get average transaction time
        #       Get new ROI, stoploss, buy and sell parameters.
        #   Persist the above to the strategy file.
    fi
done
# Push to git with a tag of 'optimized'.
