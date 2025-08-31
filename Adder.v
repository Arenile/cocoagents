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
