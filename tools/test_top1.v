`timescale 1ns / 1ps

module top
(
  output [7:0] out,
  input [0:0] reset,
  input [0:0] clk,
  input [7:0] a,
  input [7:0] b,
  input [0:0] s,
  input [7:0] c,
  output [7:0] sub1_diff_monitor,
  output [7:0] add1_a_monitor,
  output [7:0] add1_b_monitor,
  output [7:0] mux1_a_monitor,
  output [7:0] mux1_b_monitor,
  output [0:0] mux1_s_monitor,
  output [7:0] sub1_a_monitor,
  output [7:0] sub1_b_monitor
);

  wire [7:0] sub1_diff_to_mux1_b;

  mux
  mux1
  (
    .a(a),
    .s(s),
    .out(out),
    .b(sub1_diff_to_mux1_b)
  );


  Subtractor
  sub1
  (
    .reset_l(reset),
    .clk(clk),
    .a(a),
    .b(c),
    .diff(sub1_diff_to_mux1_b)
  );


  Adder
  add1
  (
    .a(b),
    .reset_l(reset),
    .clk(clk),
    .b(b)
  );

  assign mux1_a_monitor = a;
  assign mux1_b_monitor = sub1_diff_to_mux1_b;
  assign mux1_s_monitor = s;
  assign sub1_a_monitor = a;
  assign sub1_b_monitor = c;
  assign sub1_diff_monitor = sub1_diff_to_mux1_b;
  assign add1_a_monitor = b;
  assign add1_b_monitor = b;

endmodule
