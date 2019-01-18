#!/bin/bash
docker run --rm -td -p 8545:8545 --name ganache trufflesuite/ganache-cli:latest --noVMErrorsOnRPCResponse  -l99999999999999 -g10 -e 99999999999999  -a3
docker run --link ganache --rm -td --name soli-audit-fuzzer -p 2020:2020 -e host=172.16.152.103 -e port=2020 test_fuzzer


