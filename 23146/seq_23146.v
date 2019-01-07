module seq_23146(output out, input seq, input clk, input clear);


not(y1a,y1);
not(y2a,y2);
not(y3a,y3);
not(y4a,y4);
not(seqa,seq);


and(out,y1,y2);

and(w1,y1,y3a,y4,seq);
and(w2,y1,y3,y4a,seq);
and(w3,y1,y3,y4,seqa);
and(w4,y2,y3,y4,seqa);
and(w5,y1,y2a,y3a,y4a,seqa);

and(w6,y1,y3,seqa);
and(w7,y2,y3a,y4,seq);
and(w8,y1a,y2,y4a,seqa);
and(w9,y1a,y2a,y3,y4,seq);

and(w10,y1,y3a,y4);
and(w11,y2,y3a,y4);
and(w12,y1,y3,y4a,seq);
and(w13,y1a,y2a,y4,seqa);
and(w14,y1a,y3,y4a,seqa);

and(w15,y4a,seqa);
and(w16,y1,y3,y4a);
and(w17,y1,y3a,seqa);
and(w18,y1a,y2a,y3,seqa);


or(f1,w1,w2,w3,w4,w5);
or(f2,w6,w7,w8,w9);
or(f3,w10,w11,w12,w13,w14);
or(f4,w15,w16,w17w,w18);

dff dff1(y1,f1,clk,clear);
dff dff2(y2,f2,clk,clear);
dff dff3(y3,f3,clk,clear);
dff dff4(y4,f4,clk,clear);



endmodule