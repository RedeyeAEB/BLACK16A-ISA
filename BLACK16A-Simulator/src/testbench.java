public class testbench {
    public static void main(String[] args) {
        for(short i = 0; i <= 15; i++) {
            System.out.println(to_hex((short)(0xFFF0 + i)));
        }
    }

    public static String to_hex(short val) {
        String accum = "";
        for(int i = 3; i >= 0; i--) {
            int step = (val >> (4 * i)) & 0xF;
            if(step >= 10) {
                accum += "" + (char)('A' + step - 10);
            } else {
                accum += "" + step;
            }
        }
        return accum;
    }
}