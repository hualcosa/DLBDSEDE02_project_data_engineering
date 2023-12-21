from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

def main():
    # Define the schema for the incoming streaming data
    json_schema = StructType([
        StructField("sequence_id", StringType()),
        StructField("product_id", StringType()),
        StructField("price", StringType()),
        StructField("time", TimestampType()),
    ])

    spark = SparkSession.builder.appName("KafkaStreamProcessor").getOrCreate()

    # Set log level to OFF to avoid anoying logging messages
    spark.sparkContext.setLogLevel("OFF")

    # Read the Kafka stream
    df = spark.readStream.format("kafka")\
        .option("kafka.bootstrap.servers", "localhost:9092")\
        .option("subscribe", "btc-usd-price")\
        .option("startingOffsets", "latest")\
        .load()

    # Parse the JSON data
    df_parsed = df.select(from_json(col("value").cast("string"), json_schema).alias("data"))
    df_parsed = df_parsed.select('data.sequence_id', 'data.product_id', 'data.price', 'data.time')

    print(df_parsed.printSchema())
    #Write the results to a Parquet file
    # query = df_parsed.writeStream\
    #     .outputMode("append")\
    #     .format("parquet")\
    #     .option('path', 's3a://project-data-engineering-1996/stream_output')\
    #     .option('path', 's3a://project-data-engineering-1996/stream_output')\
    #     .start()
    
    query = df_parsed.writeStream\
                     .format("console")\
                     .start()
    query.awaitTermination()

if __name__ == "__main__":
    main()
