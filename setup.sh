#!/bin/bash

# Deploy kafka-docker
cd kafka-docker
docker compose -f docker-compose.yml up -d
cd ..

# Deploy local spark cluster
cd spark-container
docker build -t my-custom-spark:3.4.0 .
docker compose -f docker-compose.yml up -d
cd ..

# Deploy coinbase-data extraction container
cd python-container
docker build -t data-extractor:1.0.0 .
docker run -d --network host data-extractor:1.0.0
cd ..

# [optional] Install pyspark
pip install pyspark

# Execute the pyspark code to parse the data stream
cd spark-container
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 ./apps/stream_parser.py > sample-output.txt
cd ..
