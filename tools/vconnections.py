from typing import Any
from json_vcomponents import PORT_TYPE, VPort, VComponent, VWire
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

        for con_uuid, connection in self.connection_map.items():
            if (connection.f_instance is not None) and (
                connection.t_instance is not None
            ):
                # TODO: Make wires for these connections to put in the AST
                pass

        ast_module: vast.ModuleDef = vast.ModuleDef(
            "top", vast_paramlist, vast_portslist, vast_itemlist
        )

        return ast_module
