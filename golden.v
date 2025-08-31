
`timescale 1ns / 1ps

module golden
(
  input [7:0] a,
  input [0:0] reset,
  input [7:0] c,
  input [0:0] clk,
  input [7:0] b,
  output [7:0] out,
  input [0:0] s,
  output [7:0] sub1_b_monitor,
  output [7:0] sub1_diff_monitor,
  output [7:0] mux1_a_monitor,
  output [7:0] add1_a_monitor,
  output [7:0] mux1_b_monitor,
  output [7:0] sub1_a_monitor,
  output [7:0] add1_o_sum_monitor,
  output [0:0] mux1_s_monitor,
  output [7:0] add1_b_monitor
);

  wire [7:0] add1_o_sum_to_mux1_a;wire [7:0] sub1_diff_to_mux1_b;

  Subtractor
  sub1
  (
    .a(a),
    .reset_l(reset),
    .b(c),
    .clk(clk),
    .diff(sub1_diff_to_mux1_b)
  );


  mux
  mux1
  (
    .s(s),
    .out(out),
    .a(add1_o_sum_to_mux1_a),
    .b(sub1_diff_to_mux1_b)
  );


  Adder
  add1
  (
    .reset_l(reset),
    .clk(clk),
    .a(a),
    .b(b),
    .o_sum(add1_o_sum_to_mux1_a)
  );

  assign sub1_a_monitor = a;
  assign sub1_b_monitor = c;
  assign sub1_diff_monitor = sub1_diff_to_mux1_b;
  assign mux1_a_monitor = add1_o_sum_to_mux1_a;
  assign mux1_b_monitor = sub1_diff_to_mux1_b;
  assign mux1_s_monitor = s;
  assign add1_a_monitor = a;
  assign add1_b_monitor = b;
  assign add1_o_sum_monitor = add1_o_sum_to_mux1_a;

endmodule
