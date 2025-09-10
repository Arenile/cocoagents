from uuid import uuid4
import json_vcomponents

if __name__ == "__main__":
    # VPort TEST ################################

    print("======== NOW DOING PORT TEST ========")

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

    print("======== NOW DOING MODULE TEST ========")

    testModule = json_vcomponents.VModule(name="TestModule", portlist=[testVPort.uuid])

    test_mod_dict = testModule.toDict()

    print(f"---- ORIGINAL TESTMODULE ----\n{test_mod_dict}")

    newTestModule = json_vcomponents.VModule(json_init=test_mod_dict)

    new_test_mod_dict = newTestModule.toDict()

    print(f"---- NEW TESTMODULE ----\n{new_test_mod_dict}")
    ##############################################

    # VReg TEST ##################################

    print("======== NOW DOING REG TEST ========")

    testVReg = json_vcomponents.VReg(name="TestReg", width=1, v_module=testModule.uuid)
    test_vreg_dict = testVReg.toDict()

    print(f"---- ORIGINAL TESTREG ----\n{test_vreg_dict}")

    newTestVReg = json_vcomponents.VReg(json_init=test_vreg_dict)
    new_test_vreg_dict = newTestVReg.toDict()

    print(f"---- NEW TESTREG ----\n{new_test_vreg_dict}")
    ##############################################

    # VWire TEST #################################

    print("======== NOW DOING WIRE TEST ========")

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

    print("======== NOW DOING INSTANCE TEST ========")

    testVInst = json_vcomponents.VInstance(
        name="Test Instance", v_module=testModule.uuid
    )
    test_vinst_dict = testVInst.toDict()

    print(f"---- ORIGINAL TESTINST ----\n{test_vinst_dict}")

    newTestVInst = json_vcomponents.VInstance(json_init=test_vinst_dict)
    new_test_vinst_dict = newTestVInst.toDict()

    print(f"---- NEW TESTINST ----\n{new_test_vinst_dict}")

    ##############################################
