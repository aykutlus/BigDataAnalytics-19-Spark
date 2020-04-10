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
        .options(header='true', inferschema='true', delimiter=',')\
        .load("/home/master/Escritorio/sparkMaven/modulo8/data/airports.csv")
        
        
    airports= data_frame.filter(col("type") == "large_airport" )\
        .groupBy("iso_country") \
        .count() \
        .sort("count", ascending=False) \
    
    data_frame2= spark_session\
        .read\
        .format("csv")\
        .options(header='true', inferschema='true', delimiter=',')\
        .load("/home/master/Escritorio/sparkMaven/modulo8/data/countries.csv")
    
    countries = data_frame2.select("code","name")  
    
    output = airports.join(countries, airports.iso_country == countries.code,how='left')\
        .select("name","count")\
        .show(10)



    

    