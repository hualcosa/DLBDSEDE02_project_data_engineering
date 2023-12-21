# TLDR: execute setup.sh script and observe the stream being appended in the file sample-output.txt. Have fun :-)


#  How to setup the project manually:

1. Deploy kafka-docker:<br>
    cd into kafka docker folder and run the following command:<br>
    `docker compose -f docker-compose.yml up -d`

2. Deploy local spark cluster:<br>
    cd into spark-container folder and run the following command to create a custom spark image:<br>
    `docker build -t my-custom-spark:3.4.0 .`<br>
   
    then run the following command to deploy a local spark cluster with one master and two workers: <br>
    `docker compose -f docker-compose.yml up -d`<br>

3. Deploy coinbase-data extraction container:<br>
    cd into python-container folder and run the following command to create a custom python container that is responsible for extracting the bitcoin data from coinbase and send it to our kafka cluster:<br>
    `docker build -t data-extractor:1.0.0 .`<br>
    deploy the container using the following command:<br>
    `docker run -d --network host data-extractor:1.0.0`

4. [optional] In the next step we are going to use spark-submit command line utility to execute our spark code. If necessary,  install pyspark in your host machine environment using: `pip install pyspark`

5. Execute the pyspark code to parse the data stream:<br>
    cd into the spark-container folder and run the following command:<br>
    `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 ./apps/stream_parser.py > sample-output.txt`

6. You can now observe the stream being appended in the file sample-output.txt. Have fun :-)

# DEMO
[<img src="https://i.ytimg.com/vi/zhh3B8zDkUI/maxresdefault.jpg" width="50%">](https://www.youtube.com/watch?v=zhh3B8zDkUI "Demo video")

