import v_module as vmod
import pyverilog
import pyverilog.vparser.ast as vast
from pyverilog.vparser.parser import parse
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator

extop_ast, extop_directives = parse(["../verilog_src/ex_top.v"])

# extop_ast.show()

vermod_list: list[vmod.VModule] = []

# vmod.VModule()
for vermod_idx in range(vmod.count_mods_in_source(extop_ast)):
    vermod_list.append(vmod.VModule(extop_ast, vermod_idx))

# new_mod = vmod.VModule(extop_ast) 

# test_design:vmod.VDesign = vmod.VDesign(extop_ast)

# print("--- Connections ---")
# print(test_design.connections)
# print("--- Instances ---")
# print(test_design.mod_instances)

for new_mod in vermod_list:
    print(new_mod.name)
    for port in new_mod.portlist:
        print(f"Port: {port.name}, width={port.width}, type={port.type}, parent_mod={port.v_module.name}, port_idx={port.port_idx}")
    # print("--- Connections ---")
    # for connection in new_mod:
    #     print(f"{connection.f_port} connects to {connection.t_port}")

io_ports: dict[str:vmod.VPort] = {
    "a_port": vmod.VPort("a", 8, vmod.PORT_TYPE.INPUT, None, 0), 
    "b_port": vmod.VPort("b", 8, vmod.PORT_TYPE.INPUT, None, 1), 
    "c_port": vmod.VPort("c", 8, vmod.PORT_TYPE.INPUT, None, 2), 
    "clk_port": vmod.VPort("clk", 1, vmod.PORT_TYPE.INPUT, None, 3), 
    "rst_port": vmod.VPort("reset", 1, vmod.PORT_TYPE.INPUT, None, 4),
    "s_port": vmod.VPort("s", 1, vmod.PORT_TYPE.INPUT, None, 5), 
    "out_port": vmod.VPort("out", 8, vmod.PORT_TYPE.OUTPUT, None, 6)
}

add_instance: vmod.VInstance = vmod.VInstance(
    "add1", 
    vermod_list[0]
)

sub_instance: vmod.VInstance = vmod.VInstance(
    "sub1", 
    vermod_list[1]
)

mux_instance: vmod.VInstance = vmod.VInstance(
    "mux1", 
    vermod_list[2]
)

io_connections: list[vmod.VConnection] = [
    vmod.VConnection(
        io_ports["a_port"], 
        add_instance.module.portlist[2], 
        None, 
        add_instance
    ),
    vmod.VConnection(
        io_ports["b_port"], 
        add_instance.module.portlist[3], 
        None, 
        add_instance
    ),
    vmod.VConnection(
        io_ports["clk_port"], 
        add_instance.module.portlist[0], 
        None, 
        add_instance
    ),
    vmod.VConnection(
        io_ports["rst_port"], 
        add_instance.module.portlist[1], 
        None, 
        add_instance
    ),
    vmod.VConnection(
        io_ports["a_port"], 
        sub_instance.module.portlist[2], 
        None, 
        sub_instance
    ),
    vmod.VConnection(
        io_ports["c_port"], 
        sub_instance.module.portlist[3], 
        None, 
        sub_instance
    ),
    vmod.VConnection(
        io_ports["clk_port"], 
        sub_instance.module.portlist[0], 
        None, 
        sub_instance
    ),
    vmod.VConnection(
        io_ports["rst_port"], 
        sub_instance.module.portlist[1], 
        None, 
        sub_instance
    ),
    vmod.VConnection(
        io_ports["s_port"], 
        mux_instance.module.portlist[2], 
        None, 
        mux_instance
    ),
    vmod.VConnection(
        io_ports["out_port"], 
        mux_instance.module.portlist[3], 
        None, 
        mux_instance
    ),
]

wire_connections: list[vmod.VConnection] = [
    vmod.VConnection(
        add_instance.module.portlist[4],
        mux_instance.module.portlist[0], 
        add_instance,
        mux_instance
    ), 
    vmod.VConnection(
        sub_instance.module.portlist[4],
        mux_instance.module.portlist[1], 
        sub_instance,
        mux_instance
    )
]

top_connections = io_connections + wire_connections

# bugged_cur_state = [0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,1,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0]
# bugged_new_state = [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
# bugged_new_state = bugged_cur_state.copy()
# bugged_new_state[20] = 1

top_mod = vmod.VTop(top_connections, set(io_ports.values()))
test_connect = top_mod.getPossibleConnections()
test_cur_connect = top_mod.getCurrentConnections()

old_top_ast = top_mod.writeTop()

test_cur_connect[20] = 1 - test_cur_connect[20]
test_cur_connect[10] = 1 - test_cur_connect[10]
new_top = top_mod.setConnections(test_cur_connect)
print(f"----- test_cur_connect -----\n{[str(f"{i}:{j}") for i,j in enumerate(test_cur_connect)]}")
# print(f"\nConnect {test_connect[40]} and adjacent {bugged_new_state}\n")
# test_cur_connect[41] = 1
print(f"----- test_cur_connect after -----\n{[str(f"{i}:{j}") for i,j in enumerate(test_cur_connect)]}")
# top_with_new_connections = top_mod.setConnections(top_connections)

top_ast = new_top.writeTop()

# top_ast.show()

codegen = ASTCodeGenerator()
rslt = codegen.visit(top_ast)

filename = "./test_top1.v"

with open(filename, 'w') as f:
    f.write("`timescale 1ns / 1ps\n")
    f.write(rslt)


# top_with_new_connections = top_mod.setConnections(bugged_new_state)

# top_ast = top_with_new_connections.writeTop()

# # top_ast.show()

# codegen = ASTCodeGenerator()
# rslt = codegen.visit(top_ast)

# filename = "./test_top2.v"

# with open(filename, 'w') as f:
#     f.write("`timescale 1ns / 1ps\n")
#     f.write(rslt)
# print(f"Len of all = {len(test_connect)}, len of set = {len(test_cur_connect)}")
# print(f"Original top connections = {top_mod.connection_list}")
# print(f"----- New top connections! -----\n{top_with_new_connections.connection_list}")
# print(f"----- Old top instances ------\n{top_mod.instances_set}")
# print(f"----- Old Top Modules ------\n{[i.module.name for i in top_mod.instances_set]}")
# print(f"----- Old Top Ports ------\n{[i.name for i in top_mod.port_list]}")
# print(f"----- New top instances -----\n{top_with_new_connections.instances_set}")
# print(f"----- New top modules -----\n{[i.module.name for i in top_with_new_connections.instances_set]}")
# print(f"----- New Top Ports ------\n{[i.name for i in top_with_new_connections.port_list]}")


