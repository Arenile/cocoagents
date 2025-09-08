`timescale 1ns / 1ps

module top
(
  input [7:0] c,
  output [7:0] out,
  input [7:0] a,
  input [0:0] reset,
  input [0:0] clk,
  input [7:0] b,
  input [0:0] s,
  output [7:0] mux1_b_monitor,
  output [0:0] mux1_s_monitor,
  output [7:0] sub1_a_monitor,
  output [7:0] sub1_b_monitor,
  output [7:0] sub1_diff_monitor,
  output [7:0] add1_a_monitor,
  output [7:0] add1_b_monitor,
  output [7:0] mux1_a_monitor
);

  wire [7:0] sub1_diff_to_mux1_b;

  Subtractor
  sub1
  (
    .b(c),
    .a(a),
    .reset_l(reset),
    .clk(clk),
    .diff(sub1_diff_to_mux1_b)
  );


  Adder
  add1
  (
    .reset_l(clk),
    .a(a),
    .clk(clk),
    .b(b)
  );


  mux
  mux1
  (
    .a(a),
    .s(s),
    .out(out),
    .b(sub1_diff_to_mux1_b)
  );

  assign sub1_a_monitor = a;
  assign sub1_b_monitor = c;
  assign sub1_diff_monitor = sub1_diff_to_mux1_b;
  assign add1_a_monitor = a;
  assign add1_b_monitor = b;
  assign mux1_a_monitor = a;
  assign mux1_b_monitor = sub1_diff_to_mux1_b;
  assign mux1_s_monitor = s;

endmodule
