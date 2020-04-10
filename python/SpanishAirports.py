from pyspark import SparkConf, SparkContext
    
if __name__ == '__main__':

    spark_conf = SparkConf()
    spark_context = SparkContext(conf=spark_conf)

    # Set logger WARN
    logger = spark_context._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.WARN)

    output = spark_context \
        .textFile("/home/master/Escritorio/sparkMaven/modulo8/data/airports.csv") \
        .map(lambda line: line.split(',')) \
        .filter(lambda line: line[8] == '"ES"' ) \
        .map(lambda line: (line[2],1) ) \
        .reduceByKey(lambda a, b: a + b) \
        .sortBy(lambda pair: pair[1], ascending=False) 
    
    output.saveAsTextFile("/home/master/Escritorio/task module 8/airports2")
    
    output_print= output.collect()
        
    spark_context.stop()
    
    for (word, count) in output_print:
        print("%s: %i" % (word, count))
    
    

