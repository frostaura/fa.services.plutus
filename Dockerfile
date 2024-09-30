# Use the base image from Freqtrade.
FROM freqtradeorg/freqtrade:2024.9

# Copy over required files.
COPY ./user_data /freqtrade/user_data
