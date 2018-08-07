package sample;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.opencv.core.Core;

import javafx.application.Application;
import javafx.event.EventHandler;
import javafx.stage.Stage;
import javafx.stage.WindowEvent;
import javafx.scene.Scene;
import javafx.scene.layout.BorderPane;
import javafx.fxml.FXMLLoader;

import java.net.URI;

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

//        launch(args);
        Main.sample();
    }

    public static void sample()
    {
        HttpClient httpclient = new DefaultHttpClient();

        try
        {
            // NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
            //   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
            //   URL below with "westus".
            URIBuilder builder = new URIBuilder("https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze");

            builder.setParameter("visualFeatures", "Categories");
            builder.setParameter("details", "Celebrities");
            builder.setParameter("language", "en");

            URI uri = builder.build();
            HttpPost request = new HttpPost(uri);

            // Request headers.
            request.setHeader("Content-Type", "application/json");

            // NOTE: Replace the example key with a valid subscription key.
            request.setHeader("Ocp-Apim-Subscription-Key", "52b05c830201461da09688253629ecd3");

            // Request body. Replace the example URL with the URL for the JPEG image of a celebrity.
            StringEntity reqEntity = new StringEntity("{\"url\":\"http://www.telegraph.co.uk/content/dam/Travel/leadAssets/28/13/Galle-SriLanka_2813876a-xlarge.jpg\"}");
            request.setEntity(reqEntity);

            HttpResponse response = httpclient.execute(request);
            HttpEntity entity = response.getEntity();

            if (entity != null)
            {
                System.out.println(EntityUtils.toString(entity));
            }
        }
        catch (Exception e)
        {
            System.out.println(e.getMessage());
        }
    }
}
