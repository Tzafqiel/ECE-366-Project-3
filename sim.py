#Function call for hfold

def main():
    DIC = 0
    labelIndex = []
    labelName = []
    f = open("mc.txt", "w+")
    h = open("mc4.txt", "r")
    machinecode = h.readlines()
    for item in range(machinecode.count('\n')):  # Remove all empty lines '\n'
        machinecode.remove('\n')
    print(machinecode)

    # this block of code allocates all the memory for address ranging from 0x2000 - 0x3000 if you uncomment the commented area and run it you will see
    memory = []

    g = 0
    for i in range(512):
        mem = i
        memory.append(['00000000', mem])
        g = g + 1
        print(memory[i]) if (g == 8) else print(memory[i], end=" ")
        if g == 8:
            g = 0
    # uncomenting this gives you a space to raed the out print more claerly
    print()

    # this block creates ann array for all the registers and at the same time it allocates space for lo hi and pc
    reg = []
    for i in range(5):  # lo == index 24 hi == index 25  PC == index 26
        reg.append('00000000')
        print('r', i, reg[i]) if (i < 4) else print('pc', i, reg[i])

    # this will make accessing lo, hi, pc easy to remember
    pc = 4  # reg[pc]

    location = 0
    line = machinecode[0]
    line = ''.join(str(e) for e in line)

    while location < len(machinecode):

        # this may need to go at the bottom
        location += 1
        # TODO CHECK CFOLD FOR REFERENCE
        if line[0:3] == "000":  # hfold
            rd = int(line[3:4], 2)  # rd
            rt = int(line[4:6], 2)  # rt
            rs = int(line[6:8], 2)  # rs
            instruction = "hfold"
            # print (instruction , ("$" + str(int(line[3:4], 2)))) ,("$" + str(int(line[4:6], 2))), ("$" + str(int(line[6:8], 2)))
            rt = int(reg[rt], 2)
            rs = int(reg[rs], 2)

            for i in range(0, 5):
                tmp = rs * rt
                tmp = format(tmp, '016b')
                hi2 = int(tmp[:8], 2)
                lo2 = int(tmp[8:], 2)
                rt = hi2 ^ lo2
            a = format(rt, '08b')
            c = int(a[:4], 2) ^ int(a[4:], 2)
            c = format(c, '04b')
            c = int(c[:2], 2) ^ int(c[2:], 2)
            # now does pattern matachin of C
            c = format(c, '08b')
            reg[rd] = c
            print('hfoldresult', c)

        # TODO CHECK ADDI FOR REFERENCE
        if line[0:3] == "001":  # addi
            rt = int(line[4:6], 2)  # rt
            imm = int(line[6:8], 2)  # imm

            rtresult = int(reg[rt], 2)

            instruction = "addi"
            # print(instruction, ("$" + str(int(line[3:4], 2))), ("$" + str(int(line[4:6], 2))), imm)
            result = rtresult + imm  # does the addition operation
            if result > 255:
                result = 0
            result = format(result, '08b')  # writes the value to the register specified
            reg[rt] = result
            # print("result:", rt, "=", hex(result))

        # TODO MAKE FROM SCRATCH CHECK SLL AND ORI FOR REFERENCE
        if (line[0:3] == "010"):  # push
            rt = int(line[4:6], 2)  # rt
            imm = int(line[6:8], 2)  # imm
            instruction = "push"
            # print(instruction, ("$" + str(int(line[3:4]))), ("$" + str(int(line[4:6]))), imm)
            #print('what is rt before', reg[rt], rt)
            result = int(reg[rt], 2)
            #print(rt)
            result = result << 2
            #print('rt after shift:', rt)
            result = result | imm  # does the addition operation
            #print('result 1 ord:', result)
            reg[rt] = format(result, '08b')  # writes the value to the register specified
            #print("result 2:", rt, "=", reg[rt], 'end')
            #print('----------------------------------------')
            print(' rt', reg[rt])
        # TODO  CHECK BNE FOR REFERENCE
        if (line[0:3] == "011"):  # jneq
            rt = int(line[4:6], 2)  # rt
            imm = int(line[6:8], 2)  # imm
            instruction = "jneq"
            print('you are in jump neq')
            ##print(instruction, ("$" + str(int(line[3:4]))), ("$" + str(int(line[4:6]))), imm)
            print('if this are not equal you jump',rt ,reg[rt] , imm)
            if int(reg[rt], 2) != imm:
                print('you jumped neq')
                # this might be buggy
                location = location + 3

        # TODO CHECK SB FOR REFERNCE
        if (line[0:3] == "100"):  # sb
            rd = int(line[3:4], 2)  # rd
            rt = int(line[4:6], 2)  # rt
            imm = int(line[6:8], 2)  # imm
            instruction = "sb"
            # print(instruction, ("$" + str(int(line[3:4]))), ("$" + str(int(line[4:6]))), imm)
            memlocal = imm + int(reg[rt], 2)
            #print('is this the one?', reg[rd], rd, memory[memlocal] )
            print('sb', memlocal, rd)
            memory[memlocal][0] = reg[rd]

            print(rd, reg[rd], memlocal, memory[memlocal])

        # TODO CHECK LBU FOR REFERENCE
        if (line[0:3] == "101"):  # lb
            rd = int(line[3:4], 2)  # rd
            rt = int(line[4:6], 2)  # rt
            imm = int(line[6:8], 2)  # imm
            instruction = "lb"
            # print(instruction, ("$" + str(int(line[3:4]))), ("$" + str(int(line[4:6]))), imm)
            memlocal = imm + int(reg[rt], 2)

            reg[rd] = memory[memlocal][0]
            print(rd, reg[rd],memlocal , memory[memlocal])
        # TODO CHECK JUMP FOR REFERENCE
        if (line[0:3] == "111"):  # jmpb
            imm = int(line[3:8], 2)  # imm
            instruction = "jmp"
            # print(instruction, ("$" + str(int(line[3:4]))), ("$" + str(int(line[4:6]))), imm)
            print('are we jmpb?')
            print('jmpb lcation and imm', location, imm)
            location = location - imm
            print(location)
            print(memory[0], memory[1], memory[2], memory[3])
            print('-----------------------------------------------------------------------------------')

        if (line[0:3] == "110"):  # jmpf
            imm = int(line[3:8], 2)  # imm
            instruction = "jmp"
            # print(instruction, ("$" + str(int(line[3:4]))), ("$" + str(int(line[4:6]))), imm)
            print('are we jmpf?')
            print('jmpf lcation and imm', location, imm)
            location = location + imm
            print(location)
            print(memory[0], memory[1], memory[2], memory[3])
        #print('end rt', reg[rt])

        DIC += 1
        if location < len(machinecode):
            line = machinecode[location]
            line = ''.join(str(e) for e in line)
    print('DIC is', DIC)

    reg[pc] = format(location, '08b')

    g = 0
    for i in range(259):
        g = g + 1

        if i < 10:
            #print('1')
            print(memory[i]) if (g == 8) else print(memory[i], end="   ")
        if i < 100 and i > 9:
            #print('2')
            print(memory[i]) if (g == 8) else print(memory[i], end="  ")
        if i > 99:
            #print('3')
            print(memory[i]) if (g == 8) else print(memory[i], end=" ")
        if g == 8:
            g = 0
    #f.write('\n')
    #for i in range(27):
     #   t = format(i)
      #  if (i == 0 or 7 < i < 24):
       #     f.write('$' + t + ' ' + reg[i] + '\n')
        #if (i == 24):
         #   f.write('lo' + '  ' + reg[i] + '\n')
        #if (i == 25):
         #   f.write('hi' + '  ' + reg[i] + '\n')
        #if (i == 26):
         #   f.write('pc' + '  ' + reg[i] + '\n')
    #f.write('Dynamic instruction count is:' + format(DIC + 1))
    #f.close()
    #print('DIC is:', DIC)


if __name__ == "__main__":
    main()
