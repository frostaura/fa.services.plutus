!/bin/sh

while getopts e:d: flag
do
    case "${flag}" in
        e) epochs=${OPTARG};;
        # Should be '../user_data/strategies' for local testing.
        d) stratDir=${OPTARG};;
    esac
done

echo "Getting latest market data."
docker-compose run --rm freqtrade download-data --exchange binance --days 30 -t 1h
./build/optimize-strategies.sh -e $epochs -d $stratDir