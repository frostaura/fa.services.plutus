# Use the base image from Freqtrade.
FROM freqtradeorg/freqtrade:stable_plot

# Copy over required files.
COPY ./user_data /freqtrade/user_data