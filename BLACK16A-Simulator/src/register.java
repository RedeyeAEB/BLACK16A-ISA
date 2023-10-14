public class register {
    public final char access;   // May be 'r' or 'b' for both r/w. Write only doesn't exist.
    private short value;
    public register(String n_name, char rw, Short init_val) {
        access = rw;
        value = init_val;
    }

    public short get_value() {
        return value;
    }
    public short set_value(short n_val) {
        if(access == 'b') {
            value = n_val;
        }

        return value;
    }
}