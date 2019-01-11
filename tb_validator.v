/*
  Sequence detector validation test-bench. The TB includes the following
    1. A Clock generator defined to run at our CLK_PERIOD
    2. A task to drive the sequence detector input bus
      2.1 the task will monitor the seq. detector output for each simulation cycle
      2.2 after 12 cycles, the bus driver will check if the output is 1 or 0 and based
          on the input, the proper action will be reported to python
      2.3 the task output either "PASS" or "FAIL" to the stdout; since there is no
           way to return error codes to python. PYTHON SHOULD READ THIS OUTPUT
    3. Module instance of sequence detector assumed to be named as SEQ_DETECTOR
  
  Note the following
    1. The sequence given WILL BE GIVEN TO THE MODULE FROM THE RIGHT MOST BIT
    2. The sequence is shifted/given to the module at each clock negative edge assuming the DFF is posedge triggered
*/


// TB clock generator
module CLK_GEN #(
	parameter CLK_PERIOD = 10 
  )
  (
    output reg clk
  );
  initial begin
    clk<=0;
    forever #(CLK_PERIOD/2) clk<=~clk;
  end
endmodule


module TB;

  // TB settings and local args
  localparam CLK_PERIOD = 10;
  integer idx = 0;

  // signals driven by us
  reg reset;      // sequence detector reset signal
  reg seq;        // sequence detector 1-bit seq. input

  // signals driven by duts and bus drivers/generators
  wire out, clk;

  // student ID
  reg[0:11] tprtn = 12'b0;

  seq_23735 dut(
    out, 
    seq, 
    clk,
    reset
  );

  CLK_GEN #(.CLK_PERIOD(CLK_PERIOD)) clk_generator(
    .clk(clk)
    );

  task bus_driver;
    input[0:11] pattern;
    input is_correct;
    input rst_init;
    begin
      #(CLK_PERIOD*2) reset<=rst_init;
      #(CLK_PERIOD*2) reset<=0;

      for(idx = 0; idx < 12; idx = idx + 1) begin
        @(negedge clk) seq <= pattern[idx]; //giving the input 
        
        @(posedge clk) begin
          if (idx <= 11 && out===1) begin //testing for out=1 before the 12th cycle
            $display("FAIL: expected output==0 before 12 cycles");
          end
      end
    end
    
    @(negedge clk) begin
      if ((is_correct===1'b1 & out===1'b1) || (is_correct===1'b0 & out===1'b0)) $display("PASS"); //testing for right out after 12 cycles
      else if (is_correct===1'b1 & out!==1'b1) $display("FAIL: expected out==1 @correct sequence"); 
      else if (is_correct===1'b0 & out!==1'b0) $display("FAIL: expected out==0 @wrong sequence");
    end
    end
  endtask
                

  initial begin
    //$dumpfile("dump.vcd"); $dumpvars;
    //$display("Testing: %d", `SEQ_BCD_NUM);
    bus_driver (`SEQ_BCD_NUM<<1,  0, 1);
    bus_driver (`SEQ_BCD_NUM,     1, 0);
    bus_driver (`SEQ_BCD_NUM>>1,  0, 0);
    
    $finish;
  end
endmodule