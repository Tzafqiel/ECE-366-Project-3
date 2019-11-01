lui $8, 0xFA19
ori $8, $8, 0xE366
addi $9, $0, 1	

addi $23, $0, 5 
addi $22, $9, 0	
addi $21, $0, 101 
addi $20, $0, 0	

loop: multu $22, $8	
mflo $10	
mfhi $11	
xor $22, $10, $11
addi $23, $23, -1 
bne $23, $0, loop 

srl $10, $22, 16
andi $11, $22, 0xFFFF
xor $22, $10, $11 
srl $10, $22, 8 
andi $11, $22, 0xFF
xor $22, $10, $11

sw $22, 0x2020($20)
addi $20, $20, 4 
addi $9, $9, 1	
addi $22, $9, 0	
addi $23, $0, 5 
bne $9, $21, loop 

addi $0, $0, 0