
#Project 2 - Szymon
#MAKE SURE TO RUN THIS FILE AND NOT "translation.py"

from translation import main2

def twos_comp(val, bits):
    #"""compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val


def sim(program):
    finished = False      # Is the simulation finished? 
    PC = 0                # Program Counter
    register = [0] * 32   # Let's initialize 32 empty registers
    mem = [0] * 12288   # Let's initialize 0x3000 or 12288 spaces in memory. I know this is inefficient...
                          # But my machine has 16GB of RAM, its ok :)
    DIC = 0               # Dynamic Instr Count
    #Low is used as register 31
    highlow = [0] * 64
    low = 0
    high = 0
    #High is used as register 30
    while(not(finished)):
        if PC == len(program) - 4: 
            finished = True
        fetch = program[PC]
        DIC += 1
        # print('Registers $8 - $23 ', register[8:24])
        # print('High and Low Registers', high, low)
        # print('Dynamic Instr Count ', DIC)
        # print('The PC is:', PC )

        #print(hex(int(fetch,2)), PC)

        if fetch[0:6] == '000000' and fetch[21:32] == '00000011001': # MULTU
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
         
            register[s] = register[s] & 0xFFFFFFFF
            register[t] = register[t] & 0xFFFFFFFF
            highlow = register[s] * register[t]
            low = highlow & 0xFFFFFFFF
            high = (highlow >> 32) & 0xFFFFFFFF
            
            
        elif fetch[0:6] == '001000': # ADDI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            register[t] = register[s] + imm  
           
        elif fetch[0:6] == '000000' and fetch[21:32] == '00000010000': # MFHI
            PC += 4
            d = int(fetch[16:21],2)
            register[d] = high

        elif fetch[0:6] == '001101':   # ORI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            register[t] = register[s] | imm 
            

        elif fetch[0:6] == '001111': # LUI
            PC += 4
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            register[t] = imm << 16
            
          
        elif fetch[0:6] == '000000' and fetch[21:32] == '00000010010': # MFLO
            PC += 4
            d = int(fetch[16:21],2)
            register[d] = low

        elif fetch[0:6] == '000100':  # BEQ
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            if register[s] == register[t]:
                PC += imm*4
            
        elif fetch[0:6] == '000101':  # BNE
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            if register[s] != register[t]:
                PC += imm*4

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000111100': # MFLD
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)

            register[s] = register[s] & 0xFFFFFFFF
            register[t] = register[t] & 0xFFFFFFFF
            highlow = register[s] * register[t]
            low = highlow & 0xFFFFFFFF
            high = (highlow >> 32) & 0xFFFFFFFF

            register[d] = low ^ high


        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100100': # AND
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = (register[s] & register[t])

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000100000': # ADD
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = register[s] + register[t]
            
        elif fetch[0:6] == '100000': # LB
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            register[t] = mem[offset]

        elif fetch[0:6] == '101000': # SB
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            mem[offset] = register[t]
            

        elif fetch[0:6] == '000000' and fetch[26:32] == '100110': # XOR
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            register[d] = (register[s] ^ register[t])

        elif fetch[0:6] == '001100': # ANDI
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            imm = int(fetch[16:],2)
            register[t] = register[s] & imm

        elif fetch[0:6] == '000000' and fetch[26:32] == '000010': # SRL
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            h = int(fetch[21:26],2)
            register[d] = register[t] >> h

        elif fetch[0:6] == '000000' and fetch[21:32] == '00000101010': # SLT
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            d = int(fetch[16:21],2)
            if register[s] < register[t]:
                register[d] = 1
            else:
                register[d] = 0

        elif fetch[0:6] == '100011': # LW
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            register[t] = mem[offset]

        elif fetch[0:6] == '100000': # LB
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            mem[offset] = register[t] & 0x00FF
        
        elif fetch[0:6] == '100001': # LH
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            mem[offset] = register[t] & 0xFFFF

        elif fetch[0:6] == '101011':  # SW
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            mem[offset] = register[t]

        elif fetch[0:6] == '101000':  # SB
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            mem[offset] = register[t] & 0x00FF

        elif fetch[0:6] == '101001':  # SH
            PC += 4
            s = int(fetch[6:11],2)
            t = int(fetch[11:16],2)
            offset = -(65536 - int(fetch[16:],2)) if fetch[16]=='1' else int(fetch[16:],2)
            offset = offset + register[s]
            mem[offset] = register[t] & 0xFFFF

        else:
            # This is not implemented on purpose
            print('Not implemented')

    # Finished simulations. Let's print out some stats
    

    print('######## Simulation Finished ########')
    print('\n')
    print('Registers $8 - $23 ', register[8:24])
    print('High and Low Registers', hex(high), hex(low))
    print('Dynamic Instr Count ', DIC)
    print('The PC is at the end:', PC )
    print('\n')
    print("######## Memory Information ########h")

    x = range(8192, 8482, 4)
    for n in x:
        print("Memory Content:", hex(n), 'is', mem[n])




def main():
    main2()
    file = open('mc.txt')
    program = []
    for line in file:
        
        if line.count('#'):
            line = list(line)
            line[line.index('#'):-1] = ''
            line = ''.join(line)
        if line[0] == '\n':
            continue
        line = line.replace('\n','')
        instr = line[2:]
        instr = int(instr,16)
        instr = format(instr,'032b')
        program.append(instr)       # since PC increment by 4 every cycle,
        program.append(0)           # lets align the program code by every
        program.append(0)           # 4 lines
        program.append(0)

    # We SHALL start the simulation! 
    sim(program)     

if __name__ == '__main__':
    main()
