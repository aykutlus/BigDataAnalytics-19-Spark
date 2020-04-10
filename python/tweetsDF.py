from pyspark.sql import SparkSession
from pyspark.sql import functions
from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import explode, split
from pyspark.sql.functions import countDistinct
from pyspark.sql.functions import col


if __name__ == '__main__':

    spark_session = SparkSession \
        .builder \
        .getOrCreate()
                      
    data_frame = spark_session\
        .read\
        .format("csv")\
        .options(header='false', inferschema='true', delimiter='\t')\
        .load("/home/master/Escritorio/sparkMaven/modulo8/data/tweets.tsv") 
        
    stop_words = ["the","RT","in","to","with","a","-","for","of","on","will","at","and","is","has","this","be",""]
        
    most_repetitive_words= data_frame.select("_c2").withColumn("_c2",explode( split("_c2"," "))) \
        .groupBy("_c2")\
        .count() \
        .sort("count", ascending=False) \
        .filter(~F.col('_c2').isin(stop_words)) \
        .select(col("_c2").alias("Word"),col("count").alias("Frequency"))\
        .show(10)

    most_active_user = data_frame.select("_c1") \
        .groupBy("_c1")\
        .count() \
        .sort("count", ascending=False) \
        .select(col("_c1").alias("Username"),col("count").alias("Number of tweets"))\
        .show(1)
    
    #i choose two because there is dublicate data
    shortest_tweet_info = data_frame.select(col("_c1"),col("_c2"),col("_c3"))\
        .withColumn('length', F.length('_c2'))\
        .sort("length", ascending=True) \
        .select(col("_c1").alias("Username"),col("length").alias("Length of tweet"), col("_c3").alias("Time and Date"))\
        .show(2)
