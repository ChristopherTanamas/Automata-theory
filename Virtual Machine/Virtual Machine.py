"""
Nama Kelompok:
1. Christopher Nathaniel Tanamas // 222200153
2. Gilbert Gregorius Kirana // 222102119
3. Grace Calista Lim // 222102176
4. Jemima Alithia Sigar // 222101393
5. Samuel Revaldo Tjahyadi // 222102304
"""

from prettytable import PrettyTable

class PolishNotationEvaluator:
    def evaluate(self, data):
        result = self.parse(data)

        # Pastikan hasil tidak kosong
        if result is not None and not data:
            return result
        return "Reject"


    # Manfaatkan stack dengan recursion
    def parse(self, data):
        # Basis
        if not data:
            return None
        char = data.pop(0)

        try:
            return float(char)
        except:
            if char in ('+', '-', '*', '/', '^'):  # Operator
                # Parsing dua operand atau sub-ekspresi berikutnya
                left = self.parse(data)
                right = self.parse(data)
                # Validasi
                if left is None or right is None:
                    return None
                return self.apply_operator(char, left, right)

            # Jika pakai tanda kurung
            elif char == '(':  
                result = self.parse(data)
                # Pastikan tanda kurung tertutup dengan benar
                if data and data[0] == ')':
                    data.pop(0)  # Buang tanda kurung tutup
                    return result
                return None  # Kurung tidak seimbang atau tidak sesuai

        return None  # tidak valid


    def apply_operator(self, operator, left, right):
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left / right if right != 0 else None # Mencegah pembagian dengan 0
        elif operator == '^':
            return left ** right
        elif operator == '%':
            return left % right


class VM:
    def __init__(self):
        self.memory = []
        self.pc = 0  # Program Counter
        self.program = []  # Program yang akan dieksekusi
        self.running = False  # Status VM
        self.table = None   # Untuk output


    """ Inisiasi Tabel """
    def initiate_table(self):
        self.table = PrettyTable()
        self.table.field_names = ["Index", "Program", "Memory"]


    """Memuat program ke dalam VM."""
    def load_program(self, program):
        self.program = program


    """Mengambil instruksi saat ini berdasarkan PC."""
    def fetch_instruction(self):
        if 0 <= self.pc < len(self.program):
            instruction =  self.program[self.pc]
            data = [] # inisiasi list untuk menyimpan seluruh komponen
            data = instruction.replace('(', ' ( ').replace(')', ' ) ').split() # Simpan seluruh komponen ke dalam list 'data'.
            return data
        return None


    """ Memperluas memori (agar dinamis) """
    def expand_memory(self, value):
        if len(self.memory) < (value+1):
            inc = int(value + 1)
            self.memory = self.memory + [0] * (inc - len(self.memory))
        

    """ Evaluasi nilai dengan format polish notation """
    def parse_expression(self, expr):
        evaluator = PolishNotationEvaluator()
        result = evaluator.evaluate(expr)
        return result
    

    """ Mengeksekusi semua operasi persamaan atau pertidaksamaan """
    def if_function(self, sub_part):
        first = int(sub_part[1])
        second = int(sub_part[2])

        self.expand_memory(first)
        self.expand_memory(second)

        operator, a, b = sub_part[0], self.memory[first], self.memory[second]

        if operator == '>':
            return a > b
        elif operator == '<':
            return a < b
        elif operator == '>=':
            return a >= b
        elif operator == '<=':
            return a <= b
        elif operator == '==':
            return a == b
        elif operator == '!=':
            return a != b
        return False
    

    """ Pergi ke instruksi ke-target """
    def goto(self, target):
        self.pc = target-1
        return 
        
    
    """ Kode untuk menangani semua instruksi yang berawalan M """
    def memory_function(self, parts):
        if parts[0] == 'IF':
            sub_part_1 = parts[2:5] # ambil instruksi pertama (yang ada di dalam IF)
            if self.if_function(sub_part_1) != False:
                sub_part_2 = parts[6:]
                self.memory_function(sub_part_2)
        
        elif parts[1] == 'goto':    # pergi ke instruksi lain
            return self.goto(int(parts[2]))
        
        elif parts[0] in ('+', '-', '*', '/'):  # Evaluasi operasi
            changed_memory_index = int(parts[1]) 
            self.expand_memory(changed_memory_index)
            parts.remove(')')
            parts.remove('(')
            for i in range (len(parts)):
                try:
                    self.expand_memory(int(parts[i]))
                    parts[i] = self.memory[int(parts[i])]
                except:
                    pass
            evaluator = PolishNotationEvaluator()
            result = evaluator.evaluate(parts)
            if result != "Reject":
                self.memory[changed_memory_index] = result
            return
        
        elif parts[0] == '=':   # Memasukkan isi memori a ke memori b
            self.expand_memory(int(parts[1]))
            self.expand_memory(int(parts[3]))
            self.memory[int(parts[1])] = self.memory[int(parts[3])]
            return
        

    """Eksekusi satu instruksi """
    def execute_instruction(self, instruction):
        if instruction[1] == "end":
            self.running = False
            return

        elif instruction[0] == "(" and instruction[1] == '=':
            # Set nilai di memori
            parts = instruction[3:-1]
            mem_index = int(instruction[2])
            self.expand_memory(mem_index)
            self.memory[mem_index] = self.parse_expression(parts)
            return

        elif instruction[0] == 'M':
            parts = instruction[2:-1]
            self.memory_function(parts)
            return

        elif instruction[0] == "(" and instruction[1] == 'goto':
            return self.goto(int(instruction[2]))


    ''' Mengisi tabel '''
    def instruction_table(self, pc, memory):
        self.table.add_row([pc, self.program[pc], memory])


    ''' Running Program '''
    def run(self):
        print(f"Initial Memory: {self.memory}")
        self.initiate_table()   # inisiasi tabel output

        """ Periksa apakah diawali dengan start """
        instruction = self.fetch_instruction()  
        if instruction[1].lower() == 'start':
            self.running = True
            self.instruction_table(0, self.memory)
            self.pc += 1 

        """ Baca semua instruksi yang ada """
        while self.running:
            instruction = self.fetch_instruction()  # ambil instruksi
            if instruction:
                print(instruction)
                counter = self.pc
                self.execute_instruction(instruction)   # eksekusi perintah
                self.instruction_table(counter, self.memory)    # masukin ke tabel output
            self.pc += 1    # formal: setelah menyelesaikan 1 instruksi, lanjut ke instruksi berikutnya

            if self.running == False:
                break

        print(self.table)
        print(f"Final Memory: {self.memory}")
        self.pc = 0


class Instruction:
    def __init__(self):
        self.vm = VM()
        self.accum = 7
        self.memory_length = 0

    ''' INSTRUCTION SAMPLE '''
    def test_sample(self):
        program = [
            "(start)",                     # 0: mulai program
            "(= 0 (* 3 (+ 1 2)))",         # 1: set memory ke-0 = 9
            "(= 1 (* 3 (+ 0 2)))",         # 2: set memory ke-1 = 6
            "M(IF (> 0 1) (goto 6))",      # 3: jika m0 > 1 lompat ke 6
            "M(+ 2 (1))",                  # 4: tambah isi memory m2 dengan m1
            "(goto 7)",                    # 5: lompat ke instruksi 7
            "M(= 2 (1))",                  # 6: isi memory m2 dengan m1
            "(end)"                        # 7: akhir program
        ]

        # Jalankan program dengan VM
        self.vm.load_program(program)
        self.vm.run()
        self.vm.memory = [] # balikin memorynya

    def test_sample2(self):
        program = [
            "(start)",
            "(= 0 (* 3( + 4 2)))",
            "(= 1 (* 3( / 12 2)))",
            "M(IF (== 1 0) (goto 6))",
            "M (- 2 (1))",
            "(goto 7)",
            "M (* 2 (1))",
            "(end)"
        ]

        # Jalankan program dengan VM
        self.vm.load_program(program)
        self.vm.run()
        self.vm.memory = [] # balikin memorynya

    def test_sample3(self):
        program = [
            "(start)",                      # 0: Awal program
            "(= 0 (+ 5 3))",                # 1: Hitung 5 + 3 dan simpan di Mem[0]
            "(= 1 (* 4 0))",                # 2: Hitung 0 * 4 dan simpan di Mem[1]
            "M(IF (<= 1 20) (goto 6))",     # 3: Periksa apakah Mem[1] <= Mem[20], jika ya, lompat ke 6
            "M(+ 1 (5))",                   # 4: Tambahkan Mem[5] ke Mem[1]
            "(goto 7)",                     # 5: Lompat ke akhir
            "M(- 1 (0))",                   # 6: Kurangi Mem[0] dari Mem[1]
            "(end)"                         # 7: Akhir program
        ]

        # Jalankan program dengan VM
        self.vm.load_program(program)
        self.vm.run()
        self.vm.memory = [] # balikin memorynya

    def test_sample4(self):
        program = [
            "(start)",
            "(= 0 (0))",                 # Initialize mem[0] = 0 (loop counter)
            "(= 1 (1))",                 # mem[1] = 1 (increment value)
            "M(+ 0 (1))",     # Increment mem[0] by mem[1]
            "(goto 2)",                # Jump back to line 2, causing an endless loop
            "(end)",
        ]

        self.vm.load_program(program)
        self.vm.run()
        self.vm.memory = [] # balikin memorynya

    def SBNZ(self, a, b, c, d):
        program = [
            "(start)",                          # 0: mulai program
            f"M(= {c} ({b}))",                  # 1: set memory ke-c = isi mb
            f"M(- {c} ({a}))",                  # 2: kurangi isi m2 dengan m0
            f"M(IF (== {a} {b}) (goto {d}))",   # 3: jika m0 = m1 (dikurangi hasilnya 0), pindah ke instruksi ke 7
            "(= 4 1)",                          # 4: set isi m4 = isi 1
            "(end)"                             # 5: akhir program
        ]  

        # Jalankan program dengan VM
        self.vm.load_program(program)
        self.vm.run()

    def subleq(self, a, b, c=5):  # inisialisasi c jika tidak diisi, dia langsung ke instruksi terakhir
        tmp = self.memory_length + 1

        program = [
            "(start)",                              # 0: mulai program
            f"(= {tmp} 0)",                         # 1: set memory ke-tmp = 0
            f"M(- {b} ({a}))",                      # 2: kurangi isi mb dengan ma
            f"M(IF (<= {b} {tmp}) (goto {c}))",     # 3: jika mb <= 0, pindah ke instruksi ke c
            "(= 20 1)",                             # 4: set isi m20 = isi 1
            "(end)"                                 # 5: akhir program
        ]  

        # Jalankan program dengan VM
        self.vm.load_program(program)
        self.vm.run()

    def subleq2(self, a, b=6):
        tmp = self.memory_length
        tmp2 = self.memory_length + 1

        program = [
            "(start)",                              # 0: mulai program
            f"(= {tmp} {self.accum})",              # 1: set memory ke-tmp = accum
            f"M(- {a} ({tmp}))",                    # 2: kurangi isi ma dengan m-tmp
            f"M(= {tmp} ({a}))",                    # 3: ubah isi tmp dengan ma
            f"M(IF (<= {a} {tmp2}) (goto {b}))",    # 4: jika mb <= 0, pindah ke instruksi ke c
            "(= 20 1)",                             # 5: set isi m20 = isi 1
            "(end)"                                 # 6: akhir program
        ]
        
        # Jalankan program dengan VM
        self.vm.load_program(program)
        self.vm.run()

    def JMP(self, c):
        self.memory_length += 1
        Z = self.memory_length
        self.subleq(Z, Z, c)

    def ADD(self, a, b):
        self.memory_length += 1
        Z = self.memory_length
        self.subleq(a, Z)
        self.subleq(Z, b)
        self.subleq(Z, Z)

    def MOV(self, a, b):
        self.memory_length += 1
        Z = self.memory_length
        self.subleq(b, b)
        self.subleq(a, Z)
        self.subleq(Z, b)
        self.subleq(Z, Z)
    
    def subneg(self, a, b, c=5):  # inisialisasi c jika tidak diisi, dia langsung ke instruksi terakhir
        tmp = self.memory_length - 1

        program = [
            "(start)",                              # 0: mulai program
            f"(= {tmp} 0)",                         # 1: set memory ke-tmp = 0
            f"M(- {b} ({a}))",                      # 2: kurangi isi mb dengan ma
            f"M(IF (< {b} {tmp}) (goto {c}))",     # 3: jika mb <= 0, pindah ke instruksi ke c
            "(= 20 1)",                             # 4: set isi m20 = isi 1
            "(end)"                                 # 5: akhir program
        ]  

        # Jalankan program dengan VM
        self.vm.load_program(program)
        self.vm.run()

    def melzak(self, X, Y, Z, n, y):
        program = [
            "(start)",                              # 0: mulai program
            f"M(IF (< {X} {Y}) (goto{n}))",         # 1: if (Mem[X] < Mem[Y], goto n)
            f"M(- {X} ({Y}))",                      # 2: Mem[X] -= Mem[Y]
            f"M(+ {Z} ({Y}))",                      # 3: Mem[Z] += Mem[Y]
            f"(goto {y})",                          # 4: goto y
            "(end)"                                 # 6: akhir program
        ]
        
        # Jalankan program dengan VM
        self.vm.load_program(program)
        self.vm.run()


def main():
    instruction = Instruction()
    # instruction.test_sample()
    # instruction.test_sample2()
    # instruction.test_sample3()
    # instruction.test_sample4()

    # One instruction set
    # instruction = Instruction()
    # instruction.vm.memory = [0, 1, -2, -2, 7, 9, 11, 15, 19]
    # instruction.memory_length = len(instruction.vm.memory)

    # # instruction.SBNZ(1, 2, 5, 5)
    # instruction.subleq(0, 1, 5)
    # instruction.subleq2(2)
    # instruction.JMP(4)  # nilai m4 = 1
    # instruction.ADD(1, 4)
    # instruction.MOV(1, 3)
    # instruction.melzak(1, 2, 4, 6, 6)


if __name__ == '__main__':
    main()