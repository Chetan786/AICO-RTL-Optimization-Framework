module test(input clk, input a, input b, input c, output y);
    wire w1, w2;

    assign w1 = a & b;
    assign w2 = w1 | c;
    assign y  = w2 ^ a;

endmodule