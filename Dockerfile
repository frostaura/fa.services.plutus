# Use the base image from Freqtrade.
FROM frostaura/freqtrade:latest

# Copy over required files.
COPY ./user_data /freqtrade/user_data