from pyspark import SparkContext, SparkConf, Accumulator


def main() -> None:
    """
    Python program that uses Apache Spark to sum a list of numbers
    """
    spark_conf = SparkConf().setAppName("AddNumbers").setMaster("local[4]")
    spark_context = SparkContext(conf=spark_conf)

    logger = spark_context._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.WARN)

    data = [1, 2, 3, 4, 5, 6, 7, 8]
    distributed_data = spark_context.parallelize(data)

    accumulator = spark_context.accumulator(0)

    def sum_numbers(n1, n2):
        accumulator.add(1)
        return n1 + n2


    total = distributed_data.reduce(lambda s1, s2: sum_numbers(s1, s2))

    print("The sum is " + str(total))
    print("The number of reduce operations is: " + str(accumulator.value))


if __name__ == '__main__':
    main()