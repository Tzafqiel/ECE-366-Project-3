memory = [0] * 256
				#Dynamic Instruction Count
registers = {"$0": 0, "$1":0, "$2": 0, "$3":0, "$lo":0,"$hi":0}
labelIndex = []
labelName = []
pcAssign= []

#Function call for hfold
def HashAndMatch(A,B):
    for i in range(0, 5):
        tmp = A * B
        tmp= format(tmp,'016b')
        hi2=  int(tmp[:16],2)
        lo2=  int(tmp[16:],2)   
        A = hi2 ^ lo2
    A= format(A,'08b')
    C= int(A[8:16],2) ^ int(A[:8],2)
    C= format(C,'04b')
    C=  int(C[4:8],2) ^ int(C[:4],2)
   # now does pattern matachin of C
    C= format(C,'02b')
    registers["$lo"] = int(C,2)
    print ("result:" ,"$lo" ,"=", hex(int(C,2)))

def instrSimulation(instrs, DIC, pc):
   #pc = int(0)
   bcount=0
   #DIC = int(0)
   j = int(0)
   while True:
        bcount+=1

       # num= len(instrs)
        if (int(pc) >= len(instrs)):
           
            print("Dynamic Instruction Count: ",DIC)
            return DIC, pc;
        line = instrs[int(pc)]
        print("Current instruction PC =",pc)
        DIC+=1
        
        #TODO CHECK CFOLD FOR REFERENCE
        if(line[0:3] == "000"): # hfold
            rd = registers[("$" + str(int(line[3:4], 2)))]	#rd
            rt = registers[("$" + str(int(line[4:6], 2)))]	#rt
            rs = registers[("$" + str(int(line[6:8], 2)))] #rs
            instruction = "hfold" 
            ##print (instruction , ("$" + str(int(line[3:4], 2)))) ,("$" + str(int(line[4:6], 2))), ("$" + str(int(line[6:8], 2)))
            HashAndMatch(rt, rs)
            
            pc += 1# increments pc by 1 
        #TODO CHECK ADDI FOR REFERENCE
        if(line[0:3] == "001"): # addi
            rt = registers[("$" + str(int(line[3:4], 2)))]	#rt
            rs = registers[("$" + str(int(line[4:6], 2)))]	#rs
            imm = int(line[6:8], 2) #imm
            instruction = "addi" 
            print (instruction , ("$" + str(int(line[3:4], 2))) ,("$" + str(int(line[4:6], 2))), imm)
            result = rs + imm # does the addition operation
            registers[rt] = result # writes the value to the register specified
            print ("result:" ,rt ,"=",  hex(result))
            pc += 1# increments pc by 1 
        #TODO MAKE FROM SCRATCH CHECK SLL AND ORI FOR REFERENCE
        if(line[0:3] == "011"): # push
            rt = registers[("$" + str(int(line[3:4])))]	#rt
            rs = registers[("$" + str(int(line[4:6])))]	#rs
            imm = int(line[6:8]) #imm
            instruction = "push" 
            print (instruction , ("$" + str(int(line[3:4]))) ,("$" + str(int(line[4:6]))), imm)
            result = rs + imm # does the addition operation
            registers[rt]= result # writes the value to the register specified
            print ("result:" ,rt ,"=",  hex(result))
            pc += 1# increments pc by 1 
        #TODO  CHECK BNE FOR REFERENCE
        if(line[0:3] == "100"): # jneq
            rt = registers[("$" + str(int(line[3:4])))]	#rt
            rs = registers[("$" + str(int(line[4:6])))]	#rs
            imm = int(line[6:8]) #imm
            instruction = "jneq" 
            print (instruction , ("$" + str(int(line[3:4]))) ,("$" + str(int(line[4:6]))), imm)
            result = rs + imm # does the addition operation
            registers[rt]= result # writes the value to the register specified
            print ("result:" ,rt ,"=",  hex(result))
            pc += 1# increments pc by 1 
        #TODO CHECK SB FOR REFERNCE
        if(line[0:3] == "101"): # sb
            rt = registers[("$" + str(int(line[3:4])))]	#rt
            rs = registers[("$" + str(int(line[4:6])))]	#rs
            imm = int(line[6:8]) #imm
            instruction = "sb" 
            print (instruction , ("$" + str(int(line[3:4]))) ,("$" + str(int(line[4:6]))), imm)
            result = rs + imm # does the addition operation
            registers[rt]= result # writes the value to the register specified
            print ("result:" ,rt ,"=",  hex(result))
            pc += 1# increments pc by 1
        #TODO CHECK LBU FOR REFERENCE
        if(line[0:3] == "110"): # lbi
            rt = registers[("$" + str(int(line[3:4])))]	#rt
            rs = registers[("$" + str(int(line[4:6])))]	#rs
            imm = int(line[6:8]) #imm
            instruction = "lbi" 
            print (instruction , ("$" + str(int(line[3:4]))) ,("$" + str(int(line[4:6]))), imm)
            result = rs + imm # does the addition operation
            registers[rt]= result # writes the value to the register specified
            print ("result:" ,rt ,"=",  hex(result))
            pc += 1# increments pc by 1 
        #TODO CHECK JUMP FOR REFERENCE
        if(line[0:3] == "111"): # jmp
            imm = int(line[6:8]) #imm
            instruction = "jmp" 
            print (instruction , ("$" + str(int(line[3:4]))) ,("$" + str(int(line[4:6]))), imm)
            
            
            print ("result:" ,rt ,"=",  hex(result))
            pc += 1# increments pc by 1 

def saveJumpLabel(asm,labelIndex, labelName):
    lineCount = 0
    ppc= 0
    for line in asm:
        line = line.replace(" ","")
        if":" in line:
            pcAssign.append(0)
        else:
            pcAssign.append(ppc)
            ppc+=1
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index
            asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

def main():
   # f = open("mc.txt","w+")
    h = open("testcase1.txt","r")
    asm = h.readlines()
    instrs = []
    FinalDIC= 0
    FinalPC= 0
    
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')
       
    saveJumpLabel(asm,labelIndex,labelName) # Save all jump's destinations
    for line in asm:
        #line = line.replace("\t","")
        #line = line.replace('"','')
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0
        instrs.append(line)
       
    print(pcAssign)
    FinalDIC, FinalPC = instrSimulation(instrs, FinalDIC, FinalPC)
    print("All memory contents:")
    for k in range(0,1024):
        mem = 256 + (k*1)
        memlo= mem
        first = format(memory[memlo],"08b")
        memlo+=1
        second = format(memory[memlo],"08b")
        memlo+=1
        third = format(memory[memlo],"08b")
        memlo+=1
        fourth = format(memory[memlo],"08b")
        memlo+=1
        word =  fourth+ third + second+first
        word= int(word,2)
        word = format(word,"08x")
        print("memory", hex(mem)+": 0x"+ word )
    
    print("all register values:")
    proregister= str(registers)
    proregister= proregister.replace("'","")
    proregister= proregister.replace("{","")
    proregister= proregister.replace("}","")
    proregister= proregister.replace(",",";")
    #print(registers)
    print(proregister)
    print("Final PC =",FinalPC)
    print("memory contents from 0x2000 - 0x2050:")
    for l in range(0,21):
        mem = (l*1)
        memlo= mem- 8192
        first = format(memory[memlo],"08b")
        memlo+=1
        second = format(memory[memlo],"08b")
        memlo+=1
        third = format(memory[memlo],"08b")
        memlo+=1
        fourth = format(memory[memlo],"08b")
        memlo+=1
        word =  fourth+ third + second+first
        word= int(word,2)
        word = format(word,"08x")
        print("memory", hex(mem)+": 0x"+ word )
    print("Dynamic Instruction Count: ",FinalDIC)

if __name__ == "__main__":
    main()
