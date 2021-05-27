echo "Getting latest market data."
docker-compose run --rm freqtrade download-data --exchange binance --days 30 -t 1h