from pyspark import SparkConf, SparkContext
import numpy as np
if __name__ == '__main__':

    spark_conf = SparkConf()
    spark_context = SparkContext(conf=spark_conf)

    logger = spark_context._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.WARN)
    
    
    data_set=  spark_context \
        .textFile("/home/master/Escritorio/sparkMaven/modulo8/data/Film_Locations.csv") \
        .map(lambda line: line.split(',')) \
    
    # for average film locations per film
    output3 =data_set\
        .map(lambda line : (line[0],1) ) \
        .reduceByKey(lambda a, b: a + b) \
        .map(lambda l: l[1])  \
        .collect()
        
    # for number of films
    output2 = data_set \
        .map(lambda line : (line[0],1) ) \
        .reduceByKey(lambda a, b: a + b) \
        .count()    
        
    # for movies and theirs location
    output = data_set \
        .map(lambda line : (line[0],1) ) \
        .reduceByKey(lambda a, b: a + b) \
        .sortBy(lambda pair: pair[1], ascending=False) \
        .filter(lambda line : line[1] >= 20) \
        .collect()
   
    spark_context.stop()
    
    for (word, count) in output:
        print("(%i, %s)" % (count, word))
        
    print("Total number of films:" , output2)

    print("The average of film locations per film:" ,np.mean(output3) )