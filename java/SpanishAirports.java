package org.spark.masterbigdata;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import scala.Tuple2;

import java.util.List;

public class SpanishAirports {

    public static void main(String[]args){

        Logger.getLogger("org").setLevel(Level.OFF);

        // Step 1: Creating sparkconf

        SparkConf sparkConf = new SparkConf()
                .setAppName("SparkAirport")
                .setMaster("local[2]");

        // Step 2: creating sparkcontext

        JavaSparkContext sparkContext = new JavaSparkContext(sparkConf);

        // Step 3: Reading the csv file

        JavaRDD<String> lines = sparkContext.textFile("/home/master/Escritorio/sparkMaven/modulo8/data/airports.csv");

        // Step 4: Separating columns
        JavaRDD<String[]> fields = lines.map(line -> line.split(","));

        // Step 5: Selecting spanish airports with ES code
        JavaRDD<String[]> spanishAirports = fields.filter(array -> array[8].equals("\"ES\""));

        // Step 6: Creating the tuple (in pyhton lambda (line[2],1) and pairing(by choosing the airports type array[2]
        JavaPairRDD<String, Integer> airportTypes = spanishAirports.mapToPair(array -> new Tuple2<String, Integer>(array[2], 1));

        // Step 7: Counting airports type
        JavaPairRDD<String, Integer> numAirports = airportTypes.reduceByKey((a, b) -> a + b);

        // Step 8: Sorting part as we did in python
        List<Tuple2<Integer, String>> airports_sorted = numAirports.mapToPair(pair -> new Tuple2<>(pair._2, pair._1)).sortByKey(false).collect();

        // Syep 9: Printing the results

        for (Tuple2<?, ?> tuple : airports_sorted) {
            System.out.println(tuple._2() + ": " + tuple._1());
        }

        // Step 7: stop the spark context

        sparkContext.stop();

    }
}

