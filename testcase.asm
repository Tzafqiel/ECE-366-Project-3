addi $8, $0, 0x2000
addi $15, $0, 1
addi $16, $0, 5
addi $17, $0, 256
addi $18, $0, 4
addi $19, $0, 0
addi $23, $0, 1

addi $20, $0, 0x2120

loop: sb $23, 0($8)
addi $8, $8, 1
addi $23, $23, 1

bne  $23, $17, loop
addi $23, $23 , -1
sb   $23, 0($8)

addi $8, $0, 0x2000
addi $23, $23, 1
add  $12, $0, $0

searching: lb $11, 0($8)
addi $9, $0, 0
addi $13, $0, 8
countOne: andi $14, $11, 1
bne $14, $15, notOne

addi $9, $9, 1
beq $9, $16, exit

notOne: srl $11, $11, 1
addi $13, $13, -1
bne $13, $0, countOne


bne $9, $18, exit
addi $19, $19, 1

exit: addi $23, $23, -1
addi $8, $8, 1
bne  $23, $0, searching

sw $19, 0($20)

addi $0, $0, 0