from uuid import uuid4
import json_vcomponents

if __name__ == "__main__":
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
