iverilog -D SEQ_BCD_NUM="%1" tb_validator.v %2 dff.v
vvp a.out