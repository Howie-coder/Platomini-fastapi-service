#!/bin/bash

docker pull registry.baidubce.com/paddlepaddle/paddle:2.4.2
docker tag registry.baidubce.com/paddlepaddle/paddle:2.4.2 plato:2.4.2
docker build -t plato:1.0 .
docker-compose up
