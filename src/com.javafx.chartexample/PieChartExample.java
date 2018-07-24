package com.javafx.chartexample;

public class PieChartExample extends Application{

    @Override
    public void start(Stage primaryStage) {

        //Preparing ObservbleList object
        ObservableList<PieChart.Data> pieChartData = FXCollections.observableArrayList(
                new PieChart.Data("monkey", 13),
                new PieChart.Data("cat", 25),
                new PieChart.Data("dog", 10),
                new PieChart.Data("snake", 22));



        //Creating a Pie chart
        PieChart pieChart = new PieChart(pieChartData);
        pieChart.setTitle("Pie chart demo");
        pieChart.setClockwise(true);
        pieChart.setLabelLineLength(50);
        pieChart.setLabelsVisible(true);
        pieChart.setStartAngle(180);

        //Creating a Group object
        Group root = new Group(pieChart);

        //Creating a scene object
        Scene scene = new Scene(root, 600, 400);
        stage.setTitle("Pie chart");
        stage.setScene(scene);
        stage.show();
    }

    }

    public static void main(String[] args) {
        launch(args);
    }

}