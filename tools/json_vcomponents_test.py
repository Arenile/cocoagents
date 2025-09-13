from typing import Any
from uuid import uuid4

from pyverilog.vparser.parser import parse
import json_vcomponents
from vcomp_database import VCompDatabaseView
from vconnections import VConnection, VDesign, count_mods_in_source

if __name__ == "__main__":
    # VPort TEST ################################

    print("\n======== NOW DOING PORT TEST ========")

    testVPort = json_vcomponents.VPort(
        name="Test",
        port_width=8,
        port_type=json_vcomponents.PORT_TYPE.INPUT,
        port_idx=0,
        v_module=uuid4(),
    )

    test_port_dict = testVPort.toDict()

    print(f"---- ORIGINAL TESTPORT ----\n{test_port_dict}")

    newTestVPort = json_vcomponents.VPort(json_init=test_port_dict)

    new_test_vport_dict = newTestVPort.toDict()

    print(f"---- NEW TEST VPORT ----\n{new_test_vport_dict}")

    ##############################################

    # VModule TEST ###############################

    print("\n======== NOW DOING MODULE TEST ========")

    testModule = json_vcomponents.VModule(name="TestModule", portlist=[testVPort.uuid])

    test_mod_dict = testModule.toDict()

    print(f"---- ORIGINAL TESTMODULE ----\n{test_mod_dict}")

    newTestModule = json_vcomponents.VModule(json_init=test_mod_dict)

    new_test_mod_dict = newTestModule.toDict()

    print(f"---- NEW TESTMODULE ----\n{new_test_mod_dict}")
    ##############################################

    # VReg TEST ##################################

    print("\n======== NOW DOING REG TEST ========")

    testVReg = json_vcomponents.VReg(name="TestReg", width=1, v_module=testModule.uuid)
    test_vreg_dict = testVReg.toDict()

    print(f"---- ORIGINAL TESTREG ----\n{test_vreg_dict}")

    newTestVReg = json_vcomponents.VReg(json_init=test_vreg_dict)
    new_test_vreg_dict = newTestVReg.toDict()

    print(f"---- NEW TESTREG ----\n{new_test_vreg_dict}")
    ##############################################

    # VWire TEST #################################

    print("\n======== NOW DOING WIRE TEST ========")

    testVWire = json_vcomponents.VWire(
        name="TestWire", width=1, v_module=testModule.uuid
    )
    test_vwire_dict = testVWire.toDict()

    print(f"---- ORIGINAL TESTWIRE ----\n{test_vwire_dict}")

    newTestVWire = json_vcomponents.VWire(json_init=test_vwire_dict)
    new_test_vwire_dict = newTestVWire.toDict()

    print(f"---- NEW TESTWIRE ----\n{new_test_vwire_dict}")
    ##############################################

    # VInstance TEST #############################

    print("\n======== NOW DOING INSTANCE TEST ========")

    testVInst = json_vcomponents.VInstance(
        name="Test Instance", v_module=testModule.uuid
    )
    test_vinst_dict = testVInst.toDict()

    print(f"---- ORIGINAL TESTINST ----\n{test_vinst_dict}")

    newTestVInst = json_vcomponents.VInstance(json_init=test_vinst_dict)
    new_test_vinst_dict = newTestVInst.toDict()

    print(f"---- NEW TESTINST ----\n{new_test_vinst_dict}")

    ##############################################

    # IMPORTING MODULE TEST ######################

    print("---- TESTING MODULE IMPORT TEST ----")

    extop_ast, extop_directives = parse(["../ex_top.v"])

    vermod_list: list[json_vcomponents.VModule] = []

    for vermod_idx in range(count_mods_in_source(extop_ast)):
        vermod_list.append(json_vcomponents.VModule(extop_ast, vermod_idx))

    io_ports: dict[str, json_vcomponents.VPort] = {
        "a_port": json_vcomponents.VPort(
            "a", 8, json_vcomponents.PORT_TYPE.INPUT, None, 0
        ),
        "b_port": json_vcomponents.VPort(
            "b", 8, json_vcomponents.PORT_TYPE.INPUT, None, 1
        ),
        "c_port": json_vcomponents.VPort(
            "c", 8, json_vcomponents.PORT_TYPE.INPUT, None, 2
        ),
        "clk_port": json_vcomponents.VPort(
            "clk", 1, json_vcomponents.PORT_TYPE.INPUT, None, 3
        ),
        "rst_port": json_vcomponents.VPort(
            "reset", 1, json_vcomponents.PORT_TYPE.INPUT, None, 4
        ),
        "s_port": json_vcomponents.VPort(
            "s", 1, json_vcomponents.PORT_TYPE.INPUT, None, 5
        ),
        "out_port": json_vcomponents.VPort(
            "out", 8, json_vcomponents.PORT_TYPE.OUTPUT, None, 6
        ),
    }

    add_instance: json_vcomponents.VInstance = json_vcomponents.VInstance(
        "add1", vermod_list[0].uuid
    )
    sub_instance: json_vcomponents.VInstance = json_vcomponents.VInstance(
        "sub1", vermod_list[1].uuid
    )
    mux_instance: json_vcomponents.VInstance = json_vcomponents.VInstance(
        "mux1", vermod_list[2].uuid
    )

    vcompdbase: VCompDatabaseView = VCompDatabaseView()

    [vcompdbase.addComp(vermod) for vermod in vermod_list]

    io_connections: list[VConnection] = []
    wire_connections: list[VConnection] = []

    if (
        (add_instance.v_module is not None)
        and (sub_instance.v_module is not None)
        and (mux_instance.v_module is not None)
    ):
        add_module: Any = vcompdbase.getComp(add_instance.v_module)
        sub_module: Any = vcompdbase.getComp(sub_instance.v_module)
        mux_module: Any = vcompdbase.getComp(mux_instance.v_module)

        if (
            isinstance(add_module, json_vcomponents.VModule)
            and isinstance(sub_module, json_vcomponents.VModule)
            and isinstance(mux_module, json_vcomponents.VModule)
        ):
            io_connections: list[VConnection] = [
                VConnection(
                    {
                        "f_port": io_ports["a_port"].uuid.int,
                        "t_port": add_module.portlist[2].int,
                        "f_instance": 0,
                        "t_instance": add_instance.uuid.int,
                    }
                ),
                VConnection(
                    {
                        "f_port": io_ports["b_port"].uuid.int,
                        "t_port": add_module.portlist[3].int,
                        "f_instance": 0,
                        "t_instance": add_instance.uuid.int,
                    }
                ),
                VConnection(
                    {
                        "f_port": io_ports["clk_port"].uuid.int,
                        "t_port": add_module.portlist[0].int,
                        "f_instance": 0,
                        "t_instance": add_instance.uuid.int,
                    }
                ),
                VConnection(
                    {
                        "f_port": io_ports["rst_port"].uuid.int,
                        "t_port": add_module.portlist[1].int,
                        "f_instance": 0,
                        "t_instance": add_instance.uuid.int,
                    }
                ),
                VConnection(
                    {
                        "f_port": io_ports["a_port"].uuid.int,
                        "t_port": sub_module.portlist[2].int,
                        "f_instance": 0,
                        "t_instance": sub_instance.uuid.int,
                    }
                ),
                VConnection(
                    {
                        "f_port": io_ports["c_port"].uuid.int,
                        "t_port": sub_module.portlist[3].int,
                        "f_instance": 0,
                        "t_instance": sub_instance.uuid.int,
                    }
                ),
                VConnection(
                    {
                        "f_port": io_ports["clk_port"].uuid.int,
                        "t_port": sub_module.portlist[0].int,
                        "f_instance": 0,
                        "t_instance": sub_instance.uuid.int,
                    }
                ),
                VConnection(
                    {
                        "f_port": io_ports["rst_port"].uuid.int,
                        "t_port": sub_module.portlist[1].int,
                        "f_instance": 0,
                        "t_instance": sub_instance.uuid.int,
                    }
                ),
                VConnection(
                    {
                        "f_port": io_ports["s_port"].uuid.int,
                        "t_port": mux_module.portlist[2].int,
                        "f_instance": 0,
                        "t_instance": mux_instance.uuid.int,
                    }
                ),
                VConnection(
                    {
                        "f_port": io_ports["out_port"].uuid.int,
                        "t_port": mux_module.portlist[3].int,
                        "f_instance": 0,
                        "t_instance": mux_instance.uuid.int,
                    }
                ),
            ]

            wire_connections: list[VConnection] = [
                VConnection(
                    {
                        "f_port": add_module.portlist[4].int,
                        "t_port": mux_module.portlist[0].int,
                        "f_instance": add_instance.uuid.int,
                        "t_instance": mux_instance.uuid.int,
                    }
                ),
                VConnection(
                    {
                        "f_port": sub_module.portlist[4].int,
                        "t_port": mux_module.portlist[1].int,
                        "f_instance": sub_instance.uuid.int,
                        "t_instance": mux_instance.uuid.int,
                    }
                ),
            ]

    top_connections = io_connections + wire_connections

    v_design: VDesign = VDesign(
        [port.uuid for _, port in io_ports.items()],
        [conn.uuid for conn in top_connections],
        dbaseview=vcompdbase,
    )
