# fa.services.plutus
## Description
FrostAura Plutus is a fully automated trading system.
## Status

## Docker Support
### Local
The project supports being run as a container and is in fact indended to. In order to run this service locally, simply run `docker-compose up` in the directory where the `docker-compose.yml` file resides. The service will now run.
### Docker Hub
Automated builds are set up for Docker Hub. To use this service without the source code running, use
- `docker pull frostauraconsolidated/plutus` or 
- Visit https://hub.docker.com/repository/docker/frostauraconsolidated/plutus.
#### Docker Compose Example
    version: "3"
        services:
            plutus:
                image: "frostauraconsolidated/plutus"
                volumes:
                    - "./user_data:/freqtrade/user_data"
                command: >
                    trade
                    --logfile /freqtrade/user_data/logs/freqtrade.log
                    --db-url sqlite:////freqtrade/user_data/tradesv3.sqlite
                    --config /freqtrade/user_data/config.json
                    --strategy BBRSIStrategy
#### Custom Commands
##### Download Historical Market Data
docker-compose run --rm freqtrade download-data --exchange binance --days 15 -t 1h
##### Initiate Backtesting
docker-compose run --rm freqtrade backtesting --export trades --config user_data/config.json --strategy BBRSIStrategy --timerange 20210120-20210127 -i 1h
##### Create HTML Plot File for a Given Strategy's Performance
docker-compose run --rm freqtrade plot-dataframe -s BBRSIStrategy -p LINK/BTC --indicators1 bb_lowerband,bb_middleband,bb_upperband --indicators2 rsi
##### Initiate HyperOpt for a Given Strategy
docker-compose run --rm freqtrade hyperopt --config user_data/config.json -e 3000 --strategy BBRSIStrategy --hyperopt SampleHyperOpt --hyperopt-loss SharpeHyperOptLossDaily

## How To
### Getting Familiar

### Customization

#### Strategies

## Credits
Freqtrade (https://www.freqtrade.io/) is used as the underlying trading framework so all credit to them. This repository aims to provide custom strategies for this framework and create an automated pipeling where the strategies can evolve over nightly builds by ML optimizations running on each build.

## Contribute
In order to contribute, simply fork the repository, make changes and create a pull request.

## Support
For any queries, contact dean.martin@frostaura.net.
