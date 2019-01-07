module dff(output reg q, input  d, input clk, input reset);

always@(posedge clk or posedge reset)
begin
  if(reset == 1)
   
  q <= 0;
  
  else
  
    q <=d;
  
end

endmodule