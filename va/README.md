
1. Installation
==-============

Build Docker Image
------------------

```
cd docker-va
docker build --build-arg CACHEBUST=$(date +%s) -t dayanuyimable/soli-audit-va .
```

Run Docker Iamge
----------------

 - Run VA as command

    ```
    docker run -it --name soli-audit-va --entrypoint bash dayanuyimable/soli-audit-va
    > cd /root/vul-predict
    > python main.py --help
    ```

 - Run VA as service

    ```
    docker run -it --name soli-audit-va dayanuyimable/soli-audit-va
    ```

    Publish the port and the address if needed.

    ```
    docker run -it --name soli-audit-va \
                -p 20180:20180 \
                -e 'host=ADDR_OF_HOST_OS' \
                dayanuyimable/soli-audit-va
    ```

    Test by curl.
    ```
    curl VA-IP:20180/csf/task/status 
    curl VA_IP:20180/csf/task/upload -F taskId=123 -F sampleFile=@../vul-predict/samples/honeypot.sol
    ```

- Run UTEST Container

    (link to VA if VA container is on the same host)

    ```
    docker run -it --name utest \
        -p 80:8080 \
        --link soli-audit-va \
        dayanuyimable/utest:ether
    ```

2. Usage
========

Training
--------

 - in command line

    ```
    vul-predict/main.py train -u vuls.csv.xz -o opcodes.csv.xz
    ```
    You can specify the model to train by `-a`, run `vul-predict/main.py --help` for detail.

Predict
-------

 - in command line
    ```
    vul-predict/main.py predict -s honeypot.sol | tee result.md
    ```
    You can specify the model to predict by `-a`, run `vul-predict/main.py --help` for detail.

 - via RESTful API

    ```
    curl VA_IP:20180/csf/task/upload -F taskId=123 -F sampleFile=@../vul-predict/samples/honeypot.sol
    ```
