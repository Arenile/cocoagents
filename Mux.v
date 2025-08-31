module mux (
    input[7:0] a,b,
    input s,
    output reg[7:0] out
);

always @(*) begin
    if (s == 1'b0) begin
        out = a;
    end else begin
        out = b;
    end
end
    
endmodule