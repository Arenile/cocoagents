from typing import Any
from json_vcomponents import PORT_TYPE, VInstance, VModule, VPort, VComponent, VWire
from uuid import UUID, uuid4
from vcomp_database import VCompDatabaseView
import pyverilog.vparser.ast as vast


class VConnection:
    def __init__(self, json_init: dict[str, int]) -> None:
        self.f_instance: UUID | None = (
            UUID(int=json_init["f_instance"])
            if isinstance(json_init["f_instance"], int)
            else None
        )
        self.t_instance: UUID | None = (
            UUID(int=json_init["t_instance"])
            if isinstance(json_init["t_instance"], int)
            else None
        )
        self.f_port: UUID | None = (
            UUID(int=json_init["f_port"])
            if isinstance(json_init["f_port"], int)
            else None
        )
        self.t_port: UUID | None = (
            UUID(int=json_init["t_port"])
            if isinstance(json_init["t_port"], int)
            else None
        )
        try:
            self.uuid = (
                json_init["uuid"] if isinstance(json_init["uuid"], int) else uuid4()
            )
        except KeyError:
            self.uuid = uuid4()

    def __repr__(self) -> str:
        return f"CONNECTION:{self.uuid}={self.f_instance}_{self.f_port}_to_{self.t_instance}_{self.t_port}"

    def format_connection(self, dbase: VCompDatabaseView) -> str:
        """
        Returns a connection formatted as a string from object names instead of UUIDs
        """
        connect_string = ""
        if self.f_instance is not None:
            conn_f_inst: Any = dbase.getComp(self.f_instance)
            connect_string += (
                f"{conn_f_inst.name}_" if isinstance(conn_f_inst, VInstance) else ""
            )
        if self.f_port is not None:
            conn_f_port: Any = dbase.getComp(self.f_port)
            connect_string += (
                f"{conn_f_port.name}_to" if isinstance(conn_f_port, VPort) else ""
            )
        if self.t_instance is not None:
            conn_t_inst: Any = dbase.getComp(self.t_instance)
            connect_string += (
                f"_{conn_t_inst.name}" if isinstance(conn_t_inst, VInstance) else ""
            )
        if self.t_port is not None:
            conn_t_port: Any = dbase.getComp(self.t_port)
            connect_string += (
                f"_{conn_t_port.name}" if isinstance(conn_t_port, VPort) else ""
            )

        return connect_string


class VDesign:
    def __init__(
        self,
        io_ports: list[UUID],
        connections: list[UUID],
        dbaseview: VCompDatabaseView,
    ) -> None:
        self.dbase: VCompDatabaseView = dbaseview
        self.connection_map: dict[UUID, VConnection] = {}
        for connection in connections:
            connect_obj: Any = dbaseview.getComp(uuid=connection)
            if isinstance(connect_obj, VConnection):
                self.connection_map[connection] = connect_obj

        self.io_port_map: dict[UUID, VPort] = {}
        for port in io_ports:
            port_obj: VComponent = dbaseview.getComp(uuid=port)
            if isinstance(port_obj, VPort):
                self.io_port_map[port] = port_obj

    def makeAST(self) -> vast.ModuleDef:
        vast_paramlist = []
        vast_portslist = []
        # monitor_ports: vast.Portlist | None = None
        vast_itemlist = []

        # Building a simple map of all ports in the design as objects
        w_ports: dict[UUID, VPort] = {}
        for con_uuid, connect_obj in self.connection_map.items():
            if connect_obj.f_port is not None:
                cand_fport: Any = self.dbase.getComp(connect_obj.f_port)
                if isinstance(cand_fport, VPort):
                    w_ports[connect_obj.f_port] = cand_fport
            if connect_obj.t_port is not None:
                cand_tport: Any = self.dbase.getComp(connect_obj.t_port)
                if isinstance(cand_tport, VPort):
                    w_ports[connect_obj.t_port] = cand_tport
        for p_uuid, port in self.io_port_map.items():
            w_ports[p_uuid] = port

        for uuid, port in w_ports.items():
            if port.port_type == PORT_TYPE.INPUT:
                vast_portslist.append(
                    vast.Ioport(
                        vast.Input(
                            port.name,
                            vast.Width(
                                vast.IntConst(str(port.port_width - 1)),
                                vast.IntConst("0"),
                            ),
                        )
                    )
                )
            elif port.port_type == PORT_TYPE.OUTPUT:
                vast_portslist.append(
                    vast.Ioport(
                        vast.Output(
                            port.name,
                            vast.Width(
                                vast.IntConst(str(port.port_width - 1)),
                                vast.IntConst("0"),
                            ),
                        )
                    )
                )
            else:
                vast_portslist.append(
                    vast.Ioport(
                        vast.Inout(
                            port.name,
                            vast.Width(
                                vast.IntConst(str(port.port_width - 1)),
                                vast.IntConst("0"),
                            ),
                        )
                    )
                )

        w_wires: dict[str, VWire] = {}
        w_instances: dict[UUID, VInstance] = {}
        for con_uuid, connection in self.connection_map.items():
            if connection.f_instance is not None:
                conn_f_inst: Any = self.dbase.getComp(connection.f_instance)
                if isinstance(conn_f_inst, VInstance):
                    w_instances[connection.f_instance] = conn_f_inst
            if connection.t_instance is not None:
                conn_t_inst: Any = self.dbase.getComp(connection.t_instance)
                if isinstance(conn_t_inst, VInstance):
                    w_instances[connection.t_instance] = conn_t_inst
            if (
                (connection.f_instance is None)
                and (connection.t_instance is not None)
                and (connection.f_port is not None)
                and (connection.t_port is not None)
            ):
                # TODO: The condition for a top-level I/O connection
                pass
            if (
                (connection.f_instance is not None)
                and (connection.t_instance is not None)
                and (connection.f_port is not None)
                and (connection.t_port is not None)
            ):
                conn_f_inst: Any = self.dbase.getComp(connection.f_instance)
                conn_t_inst: Any = self.dbase.getComp(connection.t_instance)
                conn_f_port: Any = self.dbase.getComp(connection.f_port)
                conn_t_port: Any = self.dbase.getComp(connection.t_port)
                if (
                    isinstance(conn_f_inst, VInstance)
                    and isinstance(conn_t_inst, VInstance)
                    and isinstance(conn_f_port, VPort)
                    and isinstance(conn_t_port, VPort)
                ):
                    wire_name: str = f"{conn_f_inst.name}_{conn_f_port.name}_to_{conn_t_inst.name}_{conn_t_port.name}"
                    w_wires[wire_name] = VWire(
                        name=wire_name, width=conn_f_port.port_width
                    )

        vast_wires: list[vast.Wire] = [
            vast.Wire(
                wire.name,
                vast.Width(vast.IntConst(str(wire.width - 1)), vast.IntConst("0")),
            )
            for _, wire in w_wires.items()
        ]

        w_instances_map: dict[VInstance, set[VConnection]] = {}
        for conn_uuid, connection in self.connection_map.items():
            if (connection.f_instance) is not None:
                conn_f_inst: Any = self.dbase.getComp(connection.f_instance)
                if isinstance(conn_f_inst, VInstance):
                    try:
                        w_instances_map[conn_f_inst].add(connection)
                    except KeyError:
                        w_instances_map[conn_f_inst] = set()
            if (connection.t_instance) is not None:
                conn_t_inst: Any = self.dbase.getComp(connection.t_instance)
                if isinstance(conn_t_inst, VInstance):
                    try:
                        w_instances_map[conn_t_inst].add(connection)
                    except KeyError:
                        w_instances_map[conn_t_inst] = set()

        vast_instances: list[vast.InstanceList] = []

        for inst, conn_list in w_instances_map.items():
            vast_inst_connect_list = []
            for connection in conn_list:
                vast_argname: str = ""
                vast_portname: str = ""
                if (connection.t_port is not None) and (connection.f_port is not None):
                    if connection.f_instance is None:
                        conn_f_port: Any = self.dbase.getComp(connection.f_port)
                        conn_t_port: Any = self.dbase.getComp(connection.t_port)
                        if isinstance(conn_f_port, VPort) and isinstance(
                            conn_t_port, VPort
                        ):
                            vast_argname = conn_f_port.name
                            vast_portname = conn_t_port.name
                    elif (
                        (connection.t_instance is not None)
                        and (connection.f_port is not None)
                        and (connection.t_port is not None)
                    ):
                        conn_f_port: Any = self.dbase.getComp(connection.f_port)
                        conn_t_port: Any = self.dbase.getComp(connection.t_port)
                        conn_f_inst: Any = self.dbase.getComp(connection.f_instance)
                        conn_t_inst: Any = self.dbase.getComp(connection.t_instance)
                        if (
                            isinstance(conn_f_inst, VInstance)
                            and isinstance(conn_t_inst, VInstance)
                            and isinstance(conn_f_port, VPort)
                            and isinstance(conn_t_port, VPort)
                        ):
                            vast_argname = connection.format_connection(self.dbase)
                            if conn_f_inst.name == inst.name:
                                vast_portname = conn_f_port.name
                            else:
                                vast_portname = conn_t_port.name
                vast_inst_connect_list.append(
                    vast.PortArg(argname=vast_argname, portname=vast_portname)
                )
            inst_module: Any = self.dbase.getComp(inst.v_module)
            vast_inst: vast.Instance = vast.Instance(
                inst_module.name if isinstance(inst_module, VModule) else None,
                inst.name,
                vast_inst_connect_list,
                None,
            )
            vast_instances.append(
                vast.InstanceList(
                    inst_module.name if isinstance(inst_module, VModule) else "",
                    [],
                    [vast_inst],
                )
            )

        vast_itemlist = vast_wires + vast_instances

        ast_module: vast.ModuleDef = vast.ModuleDef(
            "top", vast_paramlist, vast_portslist, vast_itemlist
        )

        return ast_module
