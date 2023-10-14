import java.util.Dictionary;
import java.util.Hashtable;
import java.util.Random;
import java.util.random.*;
import java.util.LinkedList;

public class memory {
    private Dictionary<Byte, register> registers;   // Note that the byte has to be treated unsigned
    private LinkedList<tickable> tick_regs;
    public memory() {
        // Architecture doesn't guarentee a reset value for registers, so I'm gonna scramble them.
        Random random = new Random();
        // Initialize registers Dictionary, tickable registers
        registers = new Hashtable<>();

        // Initialize program counters PC, PCX

        // Initialize general purpose registers
        for(byte i = 2; i <= 2 + 15; i++) {      // Side note: intentionally using <=, 
            registers.put(i, new register("GR" + i, 'b', (short) random.nextInt(1 << 16)));
        }

        // Initialize Command Registers

        // Initialize 
    }

    public void tick() {    // Some registers (eg flag, interrupt) have properties that require to be ticked at the end of each cycle

    }
}