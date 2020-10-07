"""CPU functionality."""

import sys

LDI, PRN, HLT, PUSH, POP = 0b10000010, 0b01000111, 0b00000001, 0b01000101, 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """
        Construct a new CPU.
        """
        self.reg = [0] * 8
        self.ram = [0] * 256
        # self.reg[7] = 0xF4
        self.sp = 7
        self.reg[self.sp] = len(self.ram) - 1
        self.pc = 0
        self.running = True

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, value):
        self.ram[pc] = value

    def load(self):

        """Load a program into memory."""
        if len(sys.argv) != 2:
            print('insufficient arguments')
            sys.exit(1)

        address = 0

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line_split = line.split('#')
                    num = line_split[0].strip()
                    if num == '':
                        continue
                    try:
                        self.ram_write(address, int(num, 2))
                    except:
                        print('unable to convert string to integer')
                    address += 1
        except:
            print('file not found')
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.running:
            execute = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)

            if execute == HLT:
                self.running = False
            elif execute == LDI:
                self.reg[op_a] = op_b
                self.pc += 3
            elif execute == PRN:
                value = self.reg[op_a]
                register = self.ram_read(self.pc + 1)
                print(f"The value of R{register} is {value}.")
                self.pc += 2
            elif execute == PUSH:
                print("push")
                self.reg[self.sp] -= 1
                get_value = self.ram[self.pc + 1]
                value = self.reg[get_value]
                self.ram[self.reg[self.sp]] = value
                print(f"{value}")
                self.pc += 2
            # elif execute == POP:
            #     print("pop")
            #     self.reg[self.sp] += 1
            else:
                sys.exit(1)
