# fa.services.plutus
## Description
FrostAura Plutus is a fully automated trading system.
## Status
| Project | Status | Platform
| --- | --- | --- |
| Automatic Optimization Pipeline | ![TravisCI](https://travis-ci.org/faGH/fa.services.plutus.svg?branch=main) | TravisCI
## Docker Support
![Docker Badge](https://dockeri.co/image/frostauraconsolidated/plutus)
### Local
The project supports being run as a container and is in fact indended to. In order to run this service locally, simply run `docker-compose up` in the directory where the `docker-compose.yml` file resides. The service will now run.
### Docker Hub
Automated builds are set up for Docker Hub. To use this service without the source code running, use
- `docker pull frostauraconsolidated/plutus` or 
- Visit https://hub.docker.com/repository/docker/frostauraconsolidated/plutus.
#### Docker Compose Example
    version: "3"
        services:
            freqtrade:
                image: "frostauraconsolidated/plutus"
                volumes:
                    - "./user_data:/freqtrade/user_data"
                command: >
                    trade
                    --logfile /freqtrade/user_data/logs/freqtrade.log
                    --db-url sqlite:////freqtrade/user_data/tradesv3.sqlite
                    --config /freqtrade/user_data/config.json
                    --strategy FrostAuraM1Strategy
#### Custom Commands
##### Download Historical Market Data
Download historical market data for the configured pairs in the config.json file. This data can in turn be used to run backtesting and/or optimizations.

    docker-compose run --rm freqtrade download-data --exchange binance --days 30 -t 1h 15m
##### Initiate Backtesting
This allows for testing a given strategy against downloaded market data. See the above. NOTE: Not specifying a time range means that backtesting will run on all downloaded market data.

    docker-compose run --rm freqtrade backtesting --export trades --config user_data/config.json --strategy FrostAuraM1Strategy -i 1h
##### Initiate HyperOpt for a Given Strategy (ML Optimization)
 This allows us to run an optimization of our own design in order to determine the optimal configuration of a strategy, given the downloaded market data. NOTE: Not specifying a time range means that optimizations will run on all downloaded market data.

    docker-compose run --rm freqtrade hyperopt --config user_data/config.json -e 250 --strategy FrostAuraM1Strategy --hyperopt FrostAuraM1HyperOpt --hyperopt-loss OnlyProfitHyperOptLoss -i 1h

## How To
### Getting Started
#### Docker Requirement
- Install Docker Desktop from here: https://www.docker.com/products/docker-desktop
- After installation, ensure that if you're on windows, you switch docker from windows containers to linux containers. This can be done via the Docker icon in the system tray.
#### Configuration
- Download the repo as a zip and extract it.
- Navigate to 'user_data' directory and open up 'config.json'.
- Configure 'dryrun mode' (NOTE: If you switch between dryrun true and false, always delete the 'tradesv3.sqlite' file before restarting the bot.)
  - True = run with fake money.
  - False = run with real money. (For this, the Binance configuration is required.)
- Configure the stakes per transaction.
  - We allow 15 transactions by default for a given strategy (as seen in the config file) so you want to take your total BTC holdings and / 15 = stake
- Configure Binance
  - For this you will have to create an API key from Binance's web platform and store the key and secret in the respective fields in the config file.
- Configure Telegram (You will need a new Telegram bot for each strategy you decide to run)
    - Follow https://www.freqtrade.io/en/stable/telegram-usage/
- Strategy Configuration
  - Depending on which strategy you want to run, open up the 'docker-compose.yml' file and edit the '--strategy' property value from for example 'FrostAuraM1Strategy' to 'FrostAuraM4Strategy'.
- Running The Bot
  - Open a terminal in the directory where the 'docker-compose.yml' file exists.
  - Type 'docker-compose up -d' to run it in disconnected more OR
  - Type 'docker-compose up' to run it in the terminal window (the bot will stop running once you close this window).
- Running Multiple Strategies at Once
  - Simple Duplicate the entire folder with all the bot files (docker-compose.yml, user_data etc), for as many strategies you want to run.
  - Repeat the above configuration and running steps for each of those directories in seperate terminal windows. (Your exchange information would be the same for all bots. Your Telegram bot id should be different for all strategies).
  - Remeber to adjust your stakes according to how many strategies you will be running concurrently. (Example, We allow 15 transactions by default for a given strategy (as seen in the config file) so you want to take your total BTC holdings and / ( 15 * how many strategies you plan to run) = stake )
### Customization
#### Strategies
When creating your own strategies, follow the Freqtrade documentation to get going here: https://www.freqtrade.io/en/stable/strategy-customization/

Once you have your strategy coded, you can simply
- Move it in to 'user_data/strategies' directory.
- Edit the '--strategy' property value from for example 'FrostAuraM1Strategy' to 'YourNewStrategyName', before running the new strategy executing the 'docker-compose up' command.

## Credits
Freqtrade (https://www.freqtrade.io/) is used as the underlying trading framework so all credit to them. This repository aims to provide custom strategies for this framework and create an automated pipeline where the strategies can evolve over nightly builds by ML optimizations running on each build.

## Contribute
In order to contribute, simply fork the repository, make changes and create a pull request.

## Support
To support me in publishing and optimizing strategies, please use my referral link below it won't cost you anything but will help me lots :)

Also if you enjoy FrostAura open-source content and would like to support us in continuous delivery, please consider a donation via a platform of your choice.

| Supported Platforms | Link |
| ------------------- | ---- |
| PayPal | [Donate via Paypal](https://www.paypal.com/donate/?hosted_button_id=SVEXJC9HFBJ72) |
| Binance | [Binance Affiliate Signup](https://accounts.binance.com/en/register?ref=68898442) |

For any queries, contact dean.martin@frostaura.net.
