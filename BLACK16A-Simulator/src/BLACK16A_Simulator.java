import java.io.File;
import javax.swing.*;
import java.awt.*;

public class BLACK16A_Simulator {
    static JFrame frame;
    public static void main(String[] args) {
        create_panel();
    }


    public static void create_panel() {
        frame = new JFrame("BLACK16A Simulator");
        frame.setSize(1280, 720);
        frame.setLocation(100, 100);
        frame.setUndecorated(false);            // Make explicitly bordered
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setContentPane(new gui());
        frame.setResizable(false);
        frame.setVisible(true);
    }


}



