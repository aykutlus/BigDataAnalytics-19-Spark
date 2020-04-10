package org.spark.masterbigdata;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import scala.Tuple2;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
public class Film_Locations2 {

    public static void main(String[]args) {


        Logger.getLogger("org").setLevel(Level.OFF);

        // Step 1: Creating sparkconf

        SparkConf sparkConf = new SparkConf()
                .setAppName("SparkAirport")
                .setMaster("local[2]");

        // Step 2: creating sparkcontext

        JavaSparkContext sparkContext = new JavaSparkContext(sparkConf);

        // Step 3: Reading the csv file

        JavaRDD<String> lines = sparkContext.textFile("/home/master/Escritorio/sparkMaven/modulo8/data/Film_Locations.csv");

        // Step 4: Separating columns
        JavaRDD<String[]> fields = lines.map(line -> line.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)", -1))
                                         .map(array -> new ArrayList<>(Arrays.asList(array)).stream().map(field -> field.replaceAll("^\"(.*?)\"$", "$1")).collect(Collectors.toList()).toArray(new String[0]));


        // Step 5: Creating the tuple (in pyhton lambda (line[0],1) and pairing(by choosing the airports type array[2]
        JavaPairRDD<String, Integer> location_tuple = fields.mapToPair(array -> new Tuple2<String, Integer>(array[0], 1));

        // Step 6: Counting locations
        JavaPairRDD<String, Integer> num_locations = location_tuple.reduceByKey((a, b) -> a + b);

        // Step 7: Filtering locations which are below 20
        JavaPairRDD<String, Integer> filtered_num_locations = num_locations.filter(tup -> tup._2() >= 20);

        // Step 8: Sorting part as we did in python
        List<Tuple2<Integer, String>> location_sorted = filtered_num_locations.mapToPair(pair -> new Tuple2<>(pair._2, pair._1)).sortByKey(false).collect();

        for (Tuple2<?, ?> tuple : location_sorted) {
            System.out.println("("+ tuple._1() + "," + tuple._2()+ ")");
        }

        /// Total number of films:

        System.out.println("Total number of films:" + num_locations.count());

        /// The average of film locations per film:

        double cumulative_location = num_locations.map(tuple -> tuple._2()).reduce((a, b) -> a + b);
        double movies = num_locations.count();
        double average = cumulative_location/movies;

        System.out.println("The average of film locations per film: " + average );



    }
}

