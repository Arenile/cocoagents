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
