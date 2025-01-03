import sys
import struct

MEMSIZE = 1 << 15
REGSIZE = 8

class SynacorVM():

    def __init__(self):
        self.memory = [0] * MEMSIZE
        self.reg = [0] * REGSIZE
        self.stack = []
        self.PC = 0
        self.running = True

    def load(self, filename: str):
        with open(filename, "rb") as f:
            data = f.read()

        values = struct.unpack('<' + 'H' * (len(data) // 2), data)
        self.memory = list(values) + [0] * (MEMSIZE - len(data))
        print(f"// Loaded {len(data)} words.")

    def read_pc(self) -> int:
        """
        This method needs to read the next word of memory
        and increment the program counter, then return the value
        or the value of a register.
        """
        return 0

    def read_reg(self) -> int:
        """
        This method needs to read the next word of memory
        and return the index of a register.
        """
        return 0


    def memdump(self, start: int, length: int) -> list[int]:
        return self.memory[start:start+length]

    def step(self, trace=False) -> bool:
        PC = self.PC
        instr = self.read_pc()

        # ... instructions go here !! ...
    
        print(f"[{PC}]: {instr} Invalid instruction!")
        return False

    def run(self):
        print("// ** SYSEXEC **")
        while self.step(trace=False):
            pass
        print("// ** RUNSTOP **")

vm = SynacorVM()
print(f"// Memory: {len(vm.memory)}\n// Registers: {len(vm.reg)}")
vm.load("./challenge.bin")
vm.run()
