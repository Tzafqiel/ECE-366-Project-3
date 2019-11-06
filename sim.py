#Function call for hfold
def HashAndfold(rt, rs, rd):
    for i in range(0, 5):
        tmp = rt * rs
        tmp = format(tmp, '016b')
        hi2 = int(tmp[:8], 2)
        lo2 = int(tmp[8:], 2)
        a = hi2 ^ lo2
    a = format(a, '08b')
    c = int(a[:4], 2) ^ int(a[4:], 2)
    c = format(c, '04b')
    c = int(c[:2], 2) ^ int(c[2:], 2)
   # now does pattern matachin of C
    c = format(c, '02b')
    reg[rd] = c


def main():
    DIC = 0
    labelIndex = []
    labelName = []
    f = open("mc.txt", "w+")
    h = open("testcase1.txt", "r")
    machinecode = h.readlines()
    for item in range(machinecode.count('\n')):  # Remove all empty lines '\n'
        machinecode.remove('\n')
    print(machinecode)

    # this block of code allocates all the memory for address ranging from 0x2000 - 0x3000 if you uncomment the commented area and run it you will see
    memory = []

    g = 0
    for i in range(256):
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
            rs = int(line[4:6], 2)  # rt
            rt = int(line[6:8], 2)  # rs
            instruction = "hfold"
            ##print (instruction , ("$" + str(int(line[3:4], 2)))) ,("$" + str(int(line[4:6], 2))), ("$" + str(int(line[6:8], 2)))
            for i in range(0, 5):
                tmp = rt * rs
                tmp = format(tmp, '016b')
                hi2 = int(tmp[:8], 2)
                lo2 = int(tmp[8:], 2)
                a = hi2 ^ lo2
            a = format(a, '08b')
            c = int(a[:4], 2) ^ int(a[4:], 2)
            c = format(c, '04b')
            c = int(c[:2], 2) ^ int(c[2:], 2)
            # now does pattern matachin of C
            c = format(c, '02b')
            reg[rd] = c
            print('hfoldresult', c)

        # TODO CHECK ADDI FOR REFERENCE
        if line[0:3] == "001":  # addi
            rs = int(line[3:4], 2)  # rt
            rt = int(line[4:6], 2)  # rs
            imm = int(line[6:8], 2)  # imm

            instruction = "addi"
            ##print(instruction, ("$" + str(int(line[3:4], 2))), ("$" + str(int(line[4:6], 2))), imm)
            result = rs + imm  # does the addition operation
            reg[rt] = format(result, '02b')  # writes the value to the register specified
            #print("result:", rt, "=", hex(result))

        # TODO MAKE FROM SCRATCH CHECK SLL AND ORI FOR REFERENCE
        if (line[0:3] == "011"):  # push
            rs = int(line[3:4], 2)  # rt
            rt = int(line[4:6], 2)  # rs
            imm = int(line[6:8], 2)  # imm
            instruction = "push"
            #print(instruction, ("$" + str(int(line[3:4]))), ("$" + str(int(line[4:6]))), imm)
            rs = rs <<2
            result = rs ^ imm  # does the addition operation
            reg[rt] = format(result, '02b')  # writes the value to the register specified
            #print("result:", rt, "=", hex(result))
        # TODO  CHECK BNE FOR REFERENCE
        if (line[0:3] == "100"):  # jneq
            rs = int(line[3:4], 2)  # rt
            rt = int(line[4:6], 2)  # rs
            imm = int(line[6:8], 2)  # imm
            instruction = "jneq"
            ##print(instruction, ("$" + str(int(line[3:4]))), ("$" + str(int(line[4:6]))), imm)
            if int(reg[rt]) != int(imm):
                #this might be buggy
                location = location + 3

        # TODO CHECK SB FOR REFERNCE
        if (line[0:3] == "101"):  # sb
            rd = int(line[3:4], 2)  # rt
            rt = int(line[4:6], 2)  # rs
            imm = int(line[6:8], 2)  # imm
            instruction = "sb"
            #print(instruction, ("$" + str(int(line[3:4]))), ("$" + str(int(line[4:6]))), imm)
            memlocal = imm + int(reg[rt], 2)

            reg[rd] = mem[memlocal]

            #print("result:", rt, "=", hex(result))

        # TODO CHECK LBU FOR REFERENCE
        if (line[0:3] == "110"):  # lbi
            rd = int(line[3:4], 2)  # rt
            rt = int(line[4:6], 2)  # rs
            imm = int(line[6:8], 2)  # imm
            instruction = "lbi"
            #print(instruction, ("$" + str(int(line[3:4]))), ("$" + str(int(line[4:6]))), imm)

            print("result:", rt, "=", hex(result))
            pc += 1  # increments pc by 1
        # TODO CHECK JUMP FOR REFERENCE
        if (line[0:3] == "111"):  # jmp
            imm = int(line[6:8])  # imm
            instruction = "jmp"
            print(instruction, ("$" + str(int(line[3:4]))), ("$" + str(int(line[4:6]))), imm)

            print("result:", rt, "=", hex(result))
            pc += 1  # increments pc by 1

        if location != len(machinecode):
            line = machinecode[location]
            line = ''.join(str(e) for e in line)


        ##if j == 8:
        ##  location = 10
        ##line = asm[location]
        ##line = ''.join(str(e) for e in line)

        location += 1
        line = line.replace("\n", "")  # Removes extra chars
        line = line.replace("$", "")
        line = line.replace(" ", "")
        line = line.replace("zero", "0")  # assembly can also use both $zero and $0
        # print(line)
        # print(j, line)

        if (line[0:9] == "origamisb"):
            print('are we haere')
            line = line.replace("origamisb", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            if line[1][0:2] == "0x" or line[1][0:3] == "-0x":
                line[1] = line[1].replace("0x", "")
                imm = int(line[1], 16)
                # reg[rt] = 'ffe3'
            else:
                imm = int(line[1], 10)
            # print(line[0])
            rt = int(line[0])
            rs = int(line[2])
            fold = int(reg[rt], 16)
            rs = int(reg[rs], 16)

            ##print(rs, imm)
            address = rs + imm - 8192
            ##print(address)
            index = address // 4
            remain = address % 4
            #first fold
            lower = fold & 2**16 - 1
            upper = fold >> 16
            firstfold = lower ^ upper
            print('1', [firstfold])
            # second fold
            lower = firstfold & 2**8 - 1
            upper = firstfold >> 8
            finalfold = lower ^ upper
            print('2', [finalfold])
            ## print(remain)

            ##print(format(rt, '08x'))
            memory[index][remain] = format(finalfold, '02x')
            ##print('what did this do')
            print(memory[index])
            DIC = DIC + 1
            # print(int(DIC), "DIC")



        if (line[0:4] == "addi"):  # ADDI
            line = line.replace("addi", "")
            line = line.split(",")

            if line[2][0:2] == "0x" or line[2][0:3] == "-0x":
                line[2] = line[2].replace("0x", "")
                imm = int(line[2], 16)
            else:
                imm = int(line[2], 10)
            rs = int(line[1])
            rt = int(line[0])
            rs = int(reg[rs], 16)

            if rs > 2 ** 31 - 1:
                rs = rs - 2 ** 32

            if rt != 0:
                reg[rt] = rs + imm
                if reg[rt] < 0:
                    reg[rt] = reg[rt] + 2 ** 32
                # print(reg[rt])
                reg[rt] = format(reg[rt], '08x')
            # print(reg[rt], 'index', rt)
            DIC = DIC + 1
            # print(int(DIC), "DIC")

        if (line[0:3] == "add"):  # ADD
            line = line.replace("add", "")
            line = line.split(",")
            rd = int(line[0], 10)
            rs = int(line[1], 10)
            rt = int(line[2], 10)
            rs = int(reg[rs], 16)
            rt = int(reg[rt], 16)

            if rs > 2 ** 31 - 1:
                rs = rs - 2 ** 32

            if rt > 2 ** 31 - 1:
                rt = rt - 2 ** 32
            result = rt + rs
            if result < 0:
                result = result + 2 ** 32
            if rd != 0:
                reg[rd] = format(result, '08x')
            # print(reg[rd])
            DIC = DIC + 1
            # print(int(DIC), "DIC")

        if (line[0:3] == "lui"):  # LUI
            line = line.replace("lui", "")
            line = line.split(",")
            if line[1][0:2] == "0x" or line[1][0:3] == "-0x":
                line[1] = line[1].replace("0x", "")
                imm = int(line[1], 16)
            else:
                imm = int(line[1], 10)
            rt = int(line[0])
            if rt != 0:
                reg[rt] = format(imm * (16 ** 4), '08x')
            # print(reg[rt])

            DIC = DIC + 1
            # print(int(DIC), "DIC")

        if (line[0:3] == "ori"):  # ORI
            line = line.replace("ori", "")
            line = line.split(",")
            print(line)
            if line[2][0:2] == "0x" or line[2][0:3] == "-0x":
                line[2] = line[2].replace("0x", "")
                imm = int(line[2], 16)
            else:
                imm = int(line[2], 10)
            rs = int(line[1])
            print('1',rs, reg[rs])
            rt = int(line[0])
            rs = int(reg[rs], 16)


            if rt != 0:
                reg[rt] = rs | imm
                print('2', rs, imm)
                if reg[rt] < 0:
                    reg[rt] = reg[rt] + 2 ** 32
                reg[rt] = format(reg[rt], '08x')
            if rt == 13 or rt == 14:
                print('3', reg[rt] , line[2])
            DIC = DIC + 1
            # print(int(DIC), "DIC")

        if (line[0:4] == "andi"):  # ANDI
            line = line.replace("andi", "")
            line = line.split(",")

            if line[2][0:2] == "0x" or line[2][0:3] == "-0x":
                line[2] = line[2].replace("0x", "")
                imm = int(line[2], 16)
            else:
                imm = int(line[2], 10)
            rs = int(line[1])
            rt = int(line[0])
            print(reg[rs], rs)
            rs = int(reg[rs], 16)


            if rt != 0:
                reg[rt] = rs & imm
                if reg[rt] < 0:
                    reg[rt] = reg[rt] + 2 ** 32
                reg[rt] = format(reg[rt], '08x')
            # print(reg[rt])
            DIC = DIC + 1
            # print(int(DIC), "DIC")

        if (line[0:3] == "xor"):  # XOR
            print(line)
            line = line.replace("xor", "")
            line = line.split(",")
            rd = int(line[0], 10)
            rs = int(line[1], 10)
            rt = int(line[2], 10)
            rs = int(reg[rs], 16)
            rt = int(reg[rt], 16)
            ##print(reg[rs])
            if rd != 0:
                reg[rd] = format(rs ^ rt, '08x')
            # print(reg[rd], "xor")
            DIC = DIC + 1
            # print(int(DIC), "DIC")
            #print(reg[12], reg[15])

        if (line[0:3] == "and"):  # AND
            print(line, ' ')
            line = line.replace("and", "")
            line = line.split(",")
            rd = int(line[0], 10)
            rs = int(line[1], 10)
            rt = int(line[2], 10)
            rs = int(reg[rs], 16)
            rt = int(reg[rt], 16)
            # print(reg[rs])
            if rd != 0:
                reg[rd] = format(rs & rt, '08x')
            # print(reg[rd])
            DIC = DIC + 1
            #if( rd == 15):
                #print(reg[rd],reg[13],reg[12])
            # print(int(DIC), "DIC")


        if (line[0:2] == "sh"):  # SH
            line = line.replace("sh", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            if line[1][0:2] == "0x" or line[1][0:3] == "-0x":
                line[1] = line[1].replace("0x", "")
                imm = int(line[1], 16)
            else:
                imm = int(line[1], 10)
            rt = int(line[0])
            rs = int(line[2])
            rt = int(reg[rt], 16)
            rs = int(reg[rs], 16)

            ##print(rs, imm)
            address = rs + imm - 8192
            ##print(address)
            index = address // 4
            remain = address % 4
            if remain == 0 or remain == 2:
                ##print(format(rt, '08x'))
                byte2 = rt & 255
                rt = rt >> 8
                byte1 = rt & 255
                memory[index][remain] = format(byte2, '02x')
                memory[index][remain + 1] = format(byte1, '02x')
                ##print(memory[index])

            DIC = DIC + 1
            # print(int(DIC), "DIC")
            if index > 7:
                print(memory[index][remain + 1], memory[index][remain], memory[index][4], "sh---------")

        if (line[0:3] == "lbu"):  # LW
            line = line.replace("lbu", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            if line[1][0:2] == "0x" or line[1][0:3] == "-0x":
                line[1] = line[1].replace("0x", "")
                imm = int(line[1], 16)
            else:
                imm = int(line[1], 10)
            rt = int(line[0])
            rs = int(line[2])
            rs = int(reg[rs], 16)

            ##print(rs, imm)
            address = rs + imm - 8192
            ##print(address)
            index = address // 4
            remain = address % 4
            reg[rt] = '000000' + memory[index][remain]
            ##print(reg[rt])

            DIC = DIC + 1
            # print(int(DIC), "DIC")

        if (line[0:2] == "sb"):  # SB
            line = line.replace("sb", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            if line[1][0:2] == "0x" or line[1][0:3] == "-0x":
                line[1] = line[1].replace("0x", "")
                imm = int(line[1], 16)
                # reg[rt] = 'ffe3'
            else:
                imm = int(line[1], 10)
            # print(line[0])
            rt = int(line[0])
            rs = int(line[2])
            rt = int(reg[rt], 16)
            rs = int(reg[rs], 16)

            ##print(rs, imm)
            address = rs + imm - 8192
            ##print(address)
            index = address // 4
            remain = address % 4

            ##print(remain)

            ##print(format(rt, '08x'))
            byte1 = rt & 255
            memory[index][remain] = format(byte1, '02x')
            ##print('what did this do')
            # print(memory[index])
            DIC = DIC + 1
            # print(int(DIC), "DIC")

        if (line[0:2] == "lb"):  # LB
            line = line.replace("lb", "")
            line = line.replace("(", ",")
            line = line.replace(")", "")
            line = line.split(",")
            if line[1][0:2] == "0x" or line[1][0:3] == "-0x":
                line[1] = line[1].replace("0x", "")
                imm = int(line[1], 16)
            else:
                imm = int(line[1], 10)
            rt = int(line[0])
            rs = int(line[2])
            rs = int(reg[rs], 16)
            # print(rs, imm)
            address = rs + imm - 8192
            # print(address)
            index = address // 4
            remain = address % 4
            mem = int(memory[index][remain], 16)

            if mem > 2 ** 7 - 1:
                reg[rt] = 'ffffff' + format(mem, '02x')
            else:
                reg[rt] = format(mem, '08x')
            # print(reg[rt])
            DIC = DIC + 1
            # print(int(DIC), "DIC")

        if (line[0:4] == "sltu"):  # SLTU
            line = line.replace("sltu", "")
            line = line.split(",")
            rd = int(line[0], 10)
            rs = int(line[1], 10)
            rt = int(line[2], 10)
            rs = int(reg[rs], 16)
            rt = int(reg[rt], 16)
            # print(reg[rs])

            if rs < rt:
                reg[rd] = '00000001'
            else:
                reg[rd] = '00000000'
            # print(reg[rd], "sltu")
            DIC = DIC + 1
            # print(int(DIC), "DIC")
        if (line[0:3] == "srl"):  # SRL
            print(line)
            line = line.replace("srl", "")
            line = line.split(",")
            if line[2][0:2] == "0x" or line[2][0:3] == "-0x":
                line[2] = line[2].replace("0x", "")
                imm = int(line[2], 16)
            else:
                imm = int(line[2], 10)
            rd = int(line[0], 10)
            rt = int(line[1], 10)
            rt = int(reg[rt], 16)
            # (imm)
            reg[rd] = format(rt >> imm, '08x')
            #if( rd == 12):
                #print(reg[rd])
            DIC = DIC + 1




            # print(reg[rd], "srl")

        if (line[0:5] == "multu"):  # MULTU
            # print('multu')
            line = line.replace("multu", "")
            line = line.split(",")
            rs = int(line[0], 10)
            rt = int(line[1], 10)
            rs = int(reg[rs], 16)
            rt = int(reg[rt], 16)
            # print(reg[10], reg[11])

            result = rs * rt

            if result < 0:
                result = result + 2 ** 64

            low = result & 2 ** 32 - 1
            result = result >> 32
            high = result & 2 ** 32 - 1
            reg[lo] = format(low, '08x')
            reg[hi] = format(high, '08x')
            # print(reg[hi], reg[lo])

            # print(reg[rt], "multu")
            DIC = DIC + 1
            # print(int(DIC), "DIC")

        if (line[0:4] == "mflo"):  # MFLO
            line = line.replace("mflo", "")
            line = line.split(",")
            rd = int(line[0], 10)

            if rd != 0:
                reg[rd] = reg[lo]
            # print(reg[rd], "mflo")
            DIC = DIC + 1
            # print(int(DIC), "DIC")

        if (line[0:4] == "mfhi"):  # MFHI
            line = line.replace("mfhi", "")
            line = line.split(",")
            rd = int(line[0], 10)

            if rd != 0:
                reg[rd] = reg[hi]
            # print(reg[rd], "mfhi")
            DIC = DIC + 1
            # print(int(DIC), "DIC")

        if line[0:3] == "beq":  # BEQ
            line = line.replace("beq", "")
            line = line.split(",")
            for i in range(len(labelName)):
                if labelName[i] == line[2]:
                    labellocation = labelIndex[i]

            offset = labellocation - location + 1
            rt = int(line[1])
            rs = int(line[0])
            rs = int(reg[rs], 16)
            rt = int(reg[rt], 16)
            if rs == rt:
                for i in range(len(labelName)):
                    if labelName[i] == line[2]:
                        labellocation = labelIndex[i]

                location = labellocation
                line = asm[location]
                line = ''.join(str(e) for e in line)

            DIC = DIC + 1
            # print(int(DIC), "DIC")

        if line[0:3] == "bne":  # BNE
            line = line.replace("bne", "")
            line = line.split(",")
            rt = int(line[1])
            rs = int(line[0])
            rs = int(reg[rs], 16)
            # print(rt)
            rt = int(reg[rt], 16)

            # print(rs, rt)
            if rs != rt:
                for i in range(len(labelName)):
                    if labelName[i] == line[2]:
                        labellocation = labelIndex[i]

                location = labellocation
                line = asm[location]
                line = ''.join(str(e) for e in line)
            # print('bne')
            DIC = DIC + 1
            # print(int(DIC), "DIC")


    # print(location)
    #reg[pc] = format(location * 4, '08x')
    # print(reg[pc])
    g = 0
    ##for i in range(64):
      #  f.write(memory[i][4] + ' ' + memory[i][3] + memory[i][2] + memory[i][1] + memory[i][0] + ' ') if (
       #             g != 9) else f.write(
        #    memory[i][4] + ' ' + memory[i][3] + memory[i][2] + memory[i][1] + memory[i][0] + '\n')
        #g = g + 1

        #if g == 8:
         #   f.write('\n')
          #  g = 0
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