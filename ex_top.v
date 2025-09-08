// `include "./Adder.v"
// `include "./Subtractor.v"

module Adder (
    input clk,
    input reset_l,
    input [7:0] a,
    input [7:0] b,
    output [7:0] o_sum
);

reg [7:0] sum;

always @(posedge clk, negedge reset_l) begin
    if (!reset_l) begin
        sum <= 8'b0;
    end
    else begin
        sum <= a + b;
    end
end

assign o_sum = sum;

endmodule

module Subtractor (
    input clk,
    input reset_l,
    input [7:0] a,
    input [7:0] b,
    output reg [7:0] diff
);

always @(posedge clk, negedge reset_l) begin
    if (!reset_l) begin
        diff <= 8'b0;
    end
    else begin
        diff <= a - b;
    end
end

endmodule

module mux (
    input[7:0] a, b,
    input s,
    output reg[7:0] out
);

always @(*) begin
    if (s == 1'b1) begin
        out = b;
    end else begin
        out = a;
    end
end
    
endmodule

