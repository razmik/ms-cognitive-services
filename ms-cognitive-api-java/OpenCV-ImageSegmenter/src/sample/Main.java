package sample;

import org.opencv.core.Core;

import javafx.application.Application;
import javafx.event.EventHandler;
import javafx.stage.Stage;
import javafx.stage.WindowEvent;
import javafx.scene.Scene;
import javafx.scene.layout.BorderPane;
import javafx.fxml.FXMLLoader;

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) throws Exception{
        try
        {
            // load the FXML resource
            FXMLLoader loader = new FXMLLoader(getClass().getResource("sample.fxml"));
            BorderPane root = (BorderPane) loader.load();

            // set a whitesmoke background
            root.setStyle("-fx-background-color: whitesmoke;");
            // create and style a scene
            Scene scene = new Scene(root, 800, 600);

            // create the stage with the given title and the previously created
            // scene
            primaryStage.setTitle("Image Segmentation");
            primaryStage.setScene(scene);

            // show the GUI
            primaryStage.show();

            // get the controller
            Controller controller = loader.getController();
            controller.init();

            // set the proper behavior on closing the application
            primaryStage.setOnCloseRequest((new EventHandler<WindowEvent>() {
                public void handle(WindowEvent we)
                {
                    controller.setClosed();
                }
            }));
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }


    public static void main(String[] args) {
        // load the native OpenCV library
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME);

        launch(args);
    }
}