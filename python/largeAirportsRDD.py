from pyspark import SparkContext, SparkConf


if __name__ == "__main__":


    spark_conf = SparkConf()
    spark_context = SparkContext(conf=spark_conf)


    logger = spark_context._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.WARN)

    airport = spark_context \
        .textFile("/home/master/Escritorio/sparkMaven/modulo8/data/airports.csv")\
        .map(lambda line : line.split(","))\
        .filter(lambda line : line[2] == "\"large_airport\"") \
        .map(lambda line: (line[8], 1))\
        .reduceByKey(lambda x, y: x + y)\

    countries = spark_context\
        .textFile("/home/master/Escritorio/sparkMaven/modulo8/data/countries.csv")\
        .map(lambda line: line.split(','))\
        .map(lambda line: (line[1], line[2]))\
        .persist()

    output = airport\
        .join(countries)\
        .map(lambda pair: (pair[1][1], pair[1][0]))\
        .sortBy(lambda pair: pair[1], ascending=False)\
            
    for i in output.take(10):
        print(i)
    

