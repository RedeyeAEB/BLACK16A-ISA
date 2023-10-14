import javax.swing.*;
import java.awt.*;

public class gui extends JPanel {
    Insets inset;
    Font f;
    public gui() {
        inset = getInsets();
        f = new Font("Courier New", Font.PLAIN, 48);
        f = f.deriveFont(14F);

        setLayout(null);

        add_reg_sidebar();
        add_reg_panel();
        add_reg_header();
    }

    public void add_reg_header() {
        JPanel header = new JPanel();
        header.setLayout(new GridLayout(1, 4, 0, 0));
        for(int i = 0; i <= 3; i++ ) {
            Label l = new Label(i + "xH", 1);
            l.setFont(f);
            header.add(l);
        }
        add(header);

        header.setBounds(770 + inset.left, inset.top, 480, 30);
    }
    public void add_reg_sidebar() {
        JPanel sidebar = new JPanel();
        sidebar.setLayout(new GridLayout(16, 1, 0, 0));

        for(int i = 0; i <= 15; i++) {
            String v = "";
            if(i >= 10) {
                v = "" + (char)('A' + i - 10);
            } else {
                v = "" + i;
            }

            Label l = new Label(v, 2);
            l.setFont(f);
            sidebar.add(l);
        }

        add(sidebar);

        sidebar.setBounds(780 + inset.left, 30 + inset.top, 20, 690);
    }
    public void add_reg_panel() {
        JPanel reg = new JPanel();
        reg.setLayout(new GridLayout(16, 8, 0, 0));

        for(int i = 0; i <= 15; i++) {
            for(int k = 0; k < 4; k++) {
                Button b = new Button("0000");
                b.setFont(f);
                reg.add(b);
                Label l = new Label("MMMIII");
                l.setFont(f);
                reg.add(l);
            }
        }

        add(reg);

        reg.setBounds(800 + inset.left, 30 + inset.top, 480, 690);
    }
}