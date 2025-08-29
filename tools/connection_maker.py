from typing import Annotated
import tools.v_module as vmod
from pyverilog.vparser.parser import parse 
import pyverilog.vparser.ast as vast

# Agentic LLM frontend for Verilog connection suite we've designed around PyVerilog 
def modify_connections(
    connection_list: Annotated[list[int], 
        "A list of ones and zeroes to indicate whether a particular connection is " \
        "made in the design"], 
    ver_module: Annotated[vmod.VTop, 
        "A top-level Verilog Module object to modify the connections in a given " \
        "hardware design."]
) -> vmod.VTop:
    return ver_module.setConnections(connection_list)

def print_design(
    cur_design: Annotated[vmod.VTop, "The top-level module for the design to print."]
) -> str:
    connections_string = ""
    for connection in cur_design.connection_list:
        connections_string += str(connection)
    
    return connections_string

def get_starting_design(
    
) -> vmod.VTop:
    extop_ast, extop_directives = parse(["../verilog_src/ex_top.v"])

    vermod_list: list[vmod.VModule] = []

    for vermod_idx in range(vmod.count_mods_in_source(extop_ast)):
        vermod_list.append(vmod.VModule(extop_ast, vermod_idx))

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

    top_mod = vmod.VTop(top_connections, set(io_ports.values()))

    return top_mod