import java.util.LinkedList;

public class stack_register extends register {
    private LinkedList<Short> value;

    public stack_register(String n_name) {
        super(n_name, 'b', null);
        value = new LinkedList<Short>();
    }

    public short get_value() {
        return value.pop();
    }
    public short set_value(short n_val) {
        value.push(n_val);

        return n_val;
    }
}