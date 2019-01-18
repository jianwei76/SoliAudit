#FROM ubuntu:16.04
FROM ubuntu:18.04


# author
LABEL version="1.0"
LABEL maintainer="jianweiliao@iii.org.tw"

# set system evn =====================================
ENV DEBIAN_FRONTEND=noninteractive

# basic utils
#   NOTE: NOT use 'apt', which not suitable for CLI
RUN apt-get update && apt-get install -y \
        software-properties-common apt-utils sudo tzdata \
        curl wget iputils-ping net-tools uuid bzip2 unzip gnupg vim make

#ENV TZ Asia/Taipei (after tzdata is installed)
RUN ln -sf /usr/share/zoneinfo/ROC /etc/localtime && \
    echo "Asia/Taipei" > /etc/timezone

# dep tools =====================================
# Anaconda for ML
#RUN curl -O "https://repo.continuum.io/archive/Anaconda3-5.3.1-Linux-x86_64.sh" && \
#    bash Anaconda3-*.sh -b && \
#    rm Anaconda3-*.sh
#RUN echo 'export PATH=~/anaconda3/bin:$PATH' >> ~/.bashrc 
#ENV PATH=/root/anaconda3/bin:$PATH
#RUN conda install -y numpy pandas matplotlib scikit-learn word2vec tensorflow keras
#RUN pip install --upgrade pip



# Ethereum solc
#RUN add-apt-repository -y ppa:ethereum/ethereum && \
#apt-get update && apt-get install -y solc
#COPY solc-0.4.24 /usr/bin/solc
RUN curl -sL https://github.com/ethereum/solidity/releases/download/v0.4.24/solc-static-linux -o /usr/bin/solc && \
    chmod +x /usr/bin/solc

# Nodejs
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get update && apt-get install -y nodejs

# setting app home ==============================
RUN apt-get install -y git

WORKDIR /root
#ganache-cli a simulated node
RUN apt-get install -y g++
RUN  npm install --save -g ganache-cli --unsafe-perm=true --allow-root

COPY data .

# build with --build-arg CACHEBUST=$(date +%s) to disable cache
ARG CACHEBUST=1

# VA
#RUN git clone --depth=1 --branch="no-rm-stopwords" "ssh://git@140.92.13.105/volume1/labma_git_repos/ethvul.git" && \
#    mv "ethvul/vul-predict" .  && \
#    rm -rf "ethvul"

# !!! DELETE Private Key !!!
RUN rm -rf ".ssh"

#Copy ContractFuzzer to container
ADD FuzzContract ./ 
WORKDIR /root
RUN npm install

# sys statup =======================================
RUN echo "node /root/server.js" >> /etc/bash.bashrc
ENTRYPOINT ["/bin/bash"]

