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
        out = self.memory[self.PC]
        if out >= 32_768 and out <= 32_775:
            out = self.reg[out - 32_768]
        out = out & 0x7fff
        self.PC += 1
        return out

    def read_reg(self) -> int:
        out = self.memory[self.PC]
        if out >= 32_768 and out <= 32_775:
            out -= 32_768
        out = out & 0x7fff
        self.PC += 1
        return out


    def memdump(self, start: int, length: int) -> list[int]:
        return self.memory[start:start+length]

    def step(self, trace=False) -> bool:
        PC = self.PC
        instr = self.read_pc()

        if instr == 0:
            return False

        if instr == 1:
            a = self.read_reg()
            b = self.read_pc()
            self.reg[a] = b
            return True

        if instr == 2:
            a = self.read_pc()
            self.stack.append(a)
            return True

        if instr == 3:
            a = self.read_reg()
            if len(self.stack) == 0:
                print("// ** ENDOFSTACK **")
                return False

            self.reg[a] = self.stack.pop()
            return True

        if instr == 4:
            a = self.read_reg()
            b = self.read_pc()
            c = self.read_pc()
            self.reg[a] = 1 if b == c else 0
            return True

        if instr == 5:
            a = self.read_reg()
            b = self.read_pc()
            c = self.read_pc()
            self.reg[a] = 1 if b > c else 0
            return True

        if instr == 6:
            self.PC = self.read_pc()
            return True

        if instr == 7:
            a = self.read_pc()
            b = self.read_pc()
            if a != 0:
                self.PC = b
            return True

        if instr == 8:
            a = self.read_pc()
            b = self.read_pc()
            if a == 0:
                self.PC = b
            return True

        if instr == 9:
            a = self.read_reg()
            b = self.read_pc()
            c = self.read_pc()
            self.reg[a] = (b + c) & 0x7fff
            return True

        if instr == 10:
            a = self.read_reg()
            b = self.read_pc()
            c = self.read_pc()
            self.reg[a] = (b * c) & 0x7fff
            return True

        if instr == 11:
            a = self.read_reg()
            b = self.read_pc()
            c = self.read_pc()
            self.reg[a] = (b % c) & 0x7fff
            return True

        if instr == 12:
            a = self.read_reg()
            b = self.read_pc()
            c = self.read_pc()
            self.reg[a] = b & c
            return True

        if instr == 13:
            a = self.read_reg()
            b = self.read_pc()
            c = self.read_pc()
            self.reg[a] = b | c
            return True

        if instr == 14:
            a = self.read_reg()
            b = self.read_pc()
            self.reg[a] = ~b & 0x7fff
            return True

        if instr == 15:
            a = self.read_reg()
            b = self.read_pc()
            self.reg[a] = self.memory[b]
            return True

        if instr == 16:
            a = self.read_pc()
            b = self.read_pc()
            self.memory[a] = b
            return True

        if instr == 17:
            a = self.read_pc()
            self.stack.append(self.PC)
            self.PC = a
            return True

        if instr == 18:
            self.PC = self.stack.pop()
            return True

        if instr == 19:
            value = self.read_pc()
            print(f"{chr(value)}", end="")
            return True

        if instr == 20:
            a = self.read_reg()
            self.reg[a] = ord(sys.stdin.read(1))
            return True

        if instr == 21:
            return True

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
