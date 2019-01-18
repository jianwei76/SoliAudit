FROM ubuntu:16.04

# author
LABEL version="1.0"
LABEL maintainer="dayanuyim@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive

# install ethereum and solc by apt
RUN apt-get update && apt-get install --yes software-properties-common
RUN add-apt-repository ppa:ethereum/ethereum
RUN apt-get update && apt-get install --yes geth

# set local time
COPY ROC /etc/localtime
RUN echo "Asia/Taipei" > /etc/timezone

# create user
RUN adduser --disabled-login --gecos "" ethuser

# copy data
COPY ethdata /home/ethuser/ethdata
RUN chown -R ethuser:ethuser /home/ethuser/ethdata

# change to user env
USER ethuser
WORKDIR /home/ethuser

RUN geth init ethdata/genesis.json
RUN true && { cat ethdata/pass & cat ethdata/pass; } | geth account new

ENTRYPOINT geth --identity node2 --unlock 0 --password ethdata/pass --networkid 160230 --port=30308 --targetgaslimit 100000000 --rpc --rpcport 8545 --rpccorsdomain '*' --rpcaddr 0.0.0.0 --rpcapi=db,eth,net,web3,personal,admin console 2>> /tmp/eth.log

