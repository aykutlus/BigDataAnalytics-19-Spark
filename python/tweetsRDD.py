import sys

from pyspark import SparkConf, SparkContext


if __name__ == "__main__":

    spark_conf = SparkConf()
    spark_context = SparkContext(conf=spark_conf)

    logger = spark_context._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.WARN)
    
    data_set = spark_context \
        .textFile("/home/master/Escritorio/sparkMaven/modulo8/data/tweets.tsv") \
        .map(lambda line: line.split('\t')) 
    
    stop_words = ("the","RT","in","to","with","a","-","for","of","on","will","at","and","is","has","this","be","")

    most_repeated_words = data_set.flatMap(lambda line: line[2].split(" ")) \
        .filter(lambda word: word not in stop_words) \
        .map(lambda line: (line,1)) \
        .reduceByKey(lambda a, b: a + b) \
        .sortBy(lambda pair: pair[1], ascending=False) \
        .take(10)
        
    for (word, count) in most_repeated_words:
        print("Word: %s, Frequency: %i" % (word, count))

    
    most_active_user = data_set.map(lambda line: (line[1],1)) \
        .reduceByKey(lambda a, b: a + b) \
        .sortBy(lambda pair: pair[1], ascending=False) \
        .take(1)
        
    for (word, count) in most_active_user:
        print("Username : %s, Number of tweets: %i" % (word, count))
        
    
    length_tweet = data_set.map(lambda line: line[2]) \
        .map(lambda line: len(line))\
        .collect()
    
    shortest_tweet_length = min(length_tweet)
    
    shortest_tweet_info = data_set \
        .filter(lambda line: len(line[2]) == shortest_tweet_length) \
        .map(lambda line: [line[1], len(line[2]), line[3]]) \
        .collect()

    for (word, length,date) in shortest_tweet_info:
        print("Username: %s, Length of tweet: %i, Time and date of the tweet: %s" % (word, length,date))
        
    spark_context.stop()
              
            