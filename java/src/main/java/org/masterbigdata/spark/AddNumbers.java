package org.masterbigdata.spark;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

import java.util.Arrays;
import java.util.List;

/**
 * Program that sums a list of numbers using Apache Spark
 *
 * @author Antonio J. Nebro
 */
public class AddNumbers {
  public static void main(String[] args) {
    Logger.getLogger("org").setLevel(Level.OFF);

    // Step 1: create a SparkConf object
    SparkConf sparkConf = new SparkConf().setAppName("Add numbers").setMaster("local[4]");

    // Step 2: create a Java Spark Context
    JavaSparkContext sparkContext = new JavaSparkContext(sparkConf);

    // Step 3: initialize an array of integers
    Integer[] numbers = new Integer[] {1, 2, 3, 4, 5, 6, 7, 8};

    // Step 4: create a list of integers
    List<Integer> integerList = Arrays.asList(numbers);

    int sum = sparkContext
            .parallelize(integerList)
            .reduce((v1,v2) -> v1 v2)


    // Step 5: create a JavaRDD
    JavaRDD<Integer> distributedList = sparkContext.parallelize(integerList);

    // Step 6: sum the numbers
    int sum;
    sum = distributedList.reduce((p1, p2) -> p1 + p2);

    // Step 6: print the sum
    System.out.println("The sum is: " + sum);

    // Step 7: stop the spark context
    sparkContext.stop();
  }
}
