# Use the base image from Freqtrade.
FROM freqtradeorg/freqtrade:2021.9

# Copy over required files.
COPY ./user_data /freqtrade/user_data

# Custom dependencies.
USER root

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y manpages-dev

USER ftuser

RUN pip install -U pip
RUN pip install -U setuptools
RUN pip install -U cython
RUN pip install -U numpy
RUN pip install -U matplotlib
RUN pip install -U arviz
RUN pip install -U pandas
RUN pip install -U scipy
RUN pip install -U pystan==2.19.1.1
RUN pip install -U prophet