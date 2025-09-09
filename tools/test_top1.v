`timescale 1ns / 1ps

module top
(
  input [7:0] b,
  output [7:0] out,
  input [7:0] c,
  input [0:0] clk,
  input [7:0] a,
  input [0:0] reset,
  input [0:0] s,
  output [7:0] mux1_b_monitor,
  output [7:0] mux1_a_monitor,
  output [0:0] mux1_s_monitor,
  output [7:0] sub1_b_monitor,
  output [7:0] add1_a_monitor,
  output [7:0] add1_b_monitor,
  output [7:0] sub1_diff_monitor,
  output [7:0] sub1_a_monitor
);

  wire [7:0] sub1_diff_to_mux1_b;

  mux
  mux1
  (
    .a(c),
    .s(s),
    .out(out),
    .b(sub1_diff_to_mux1_b)
  );


  Adder
  add1
  (
    .b(a),
    .clk(clk),
    .a(a),
    .reset_l(reset)
  );


  Subtractor
  sub1
  (
    .b(c),
    .clk(clk),
    .a(a),
    .reset_l(reset),
    .diff(sub1_diff_to_mux1_b)
  );

  assign mux1_a_monitor = c;
  assign mux1_b_monitor = sub1_diff_to_mux1_b;
  assign mux1_s_monitor = s;
  assign add1_a_monitor = a;
  assign add1_b_monitor = a;
  assign sub1_a_monitor = a;
  assign sub1_b_monitor = c;
  assign sub1_diff_monitor = sub1_diff_to_mux1_b;

endmodule
