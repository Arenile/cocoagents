from typing import Any
from json_vcomponents import VPort, VComponent
from uuid import UUID, uuid4
from vcomp_database import VCompDatabaseView


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

    def makeAST(self):
        pass
