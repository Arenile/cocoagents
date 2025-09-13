from abc import abstractmethod

# import json
from uuid import UUID, uuid4
from enum import Enum


class PORT_TYPE(Enum):
    INPUT = 0
    OUTPUT = 1
    INOUT = 2


class COMPONENT_TYPE(Enum):
    COMPONENT = 0
    PORT = 1
    REG = 2
    WIRE = 3
    INSTANCE = 4
    MODULE = 5
    CONNECTION = 6


class VComponent:
    def __init__(self, name: str | None = None, uuid: UUID | None = None) -> None:
        self.name: str = name if isinstance(name, str) else ""
        self.uuid: UUID = uuid4() if uuid is None else uuid
        self.comp_type: COMPONENT_TYPE = COMPONENT_TYPE.COMPONENT

    @abstractmethod
    def toDict(self) -> dict[str, str | int | list]:
        return {
            "uuid": self.uuid.int,
            "name": self.name,
            "comp_type": self.comp_type.name,
        }


class VInternal(VComponent):
    def __init__(
        self,
        name: str = "",
        width: int = 0,
        v_module: UUID | None = None,
        json_init: dict[str, str | int | list] | None = None,
    ):
        if json_init is None:
            super().__init__(name=name)
            self.width: int = width
            self.v_module: UUID | None = v_module
        else:
            super().__init__(
                name=json_init["name"] if isinstance(json_init["name"], str) else "",
                uuid=UUID(int=json_init["uuid"])
                if (isinstance(json_init["uuid"], int) and json_init["uuid"] != 0)
                else uuid4(),
            )
            self.width: int = (
                json_init["width"] if isinstance(json_init["width"], int) else 0
            )
            self.v_module: UUID | None = (
                UUID(int=json_init["v_module"])
                if (
                    isinstance(json_init["v_module"], int)
                    and json_init["v_module"] != 0
                )
                else None
            )

    @abstractmethod
    def toDict(self) -> dict[str, str | int | list]:
        return super().toDict() | {
            "width": self.width,
            "v_module": self.v_module.int if self.v_module is not None else 0,
        }


class VConnection(VComponent):
    def __init__(
        self,
        f_instance: UUID | None = None,
        t_instance: UUID | None = None,
        f_port: UUID | None = None,
        t_port: UUID | None = None,
        json_init: dict[str, int | str | list] | None = None,
    ) -> None:
        """
        Initialize with a dictionary of the form:
        {
            "f_instance": UUID,
            "t_instance": UUID,
            "f_port": UUID,
            "t_port": UUID
        }
        """
        self.comp_type: COMPONENT_TYPE = COMPONENT_TYPE.CONNECTION
        if json_init is None:
            self.f_instance: UUID | None = (
                f_instance if f_instance is not None else None
            )
            self.t_instance: UUID | None = (
                t_instance if t_instance is not None else None
            )
            self.f_port: UUID | None = f_port if f_port is not None else None
            self.t_port: UUID | None = t_port if t_port is not None else None
            self.uuid: UUID = uuid4()
        else:
            self.f_instance: UUID | None = (
                UUID(int=json_init["f_instance"])
                if (
                    isinstance(json_init["f_instance"], int)
                    and (json_init["f_instance"] != 0)
                )
                else None
            )
            self.t_instance: UUID | None = (
                UUID(int=json_init["t_instance"])
                if (
                    isinstance(json_init["t_instance"], int)
                    and (json_init["t_instance"] != 0)
                )
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
                self.uuid: UUID = (
                    UUID(int=json_init["uuid"])
                    if isinstance(json_init["uuid"], int)
                    else uuid4()
                )
            except KeyError:
                self.uuid: UUID = uuid4()

        self.name = f"{self.f_port}_to_{self.t_port}"

    def __repr__(self) -> str:
        return f"CONNECTION:{self.uuid}={self.f_instance}_{self.f_port}_to_{self.t_instance}_{self.t_port}"

    def toDict(self) -> dict[str, int | str | list]:
        return super().toDict() | {
            "f_instance": self.f_instance.int if self.f_instance is not None else 0,
            "t_instance": self.t_instance.int if self.t_instance is not None else 0,
            "f_port": self.f_port.int if self.f_port is not None else 0,
            "t_port": self.t_port.int if self.t_port is not None else 0,
        }


class VPort(VComponent):
    def __init__(
        self,
        name: str = "",
        port_width: int = 0,
        port_type: PORT_TYPE = PORT_TYPE.INPUT,
        v_module: UUID | None = None,
        port_idx: int = -1,
        json_init: dict[str, str | int | list] | None = None,
    ):
        if json_init is None:
            super().__init__(name=name)
            self.port_width: int = port_width
            self.port_type: PORT_TYPE = port_type
            self.v_module: UUID | None = v_module
            self.port_idx: int = port_idx
        else:
            super().__init__(
                name=json_init["name"] if isinstance(json_init["name"], str) else "",
                uuid=UUID(int=json_init["uuid"])
                if isinstance(json_init["uuid"], int)
                else uuid4(),
            )
            self.port_width: int = (
                json_init["port_width"]
                if isinstance(json_init["port_width"], int)
                else -1
            )

            if json_init["port_type"] == "INPUT":
                self.port_type = PORT_TYPE.INPUT
            elif json_init["port_type"] == "OUTPUT":
                self.port_type = PORT_TYPE.OUTPUT
            else:
                self.port_type = PORT_TYPE.INOUT

            self.v_module: UUID | None = (
                UUID(int=json_init["v_module"])
                if (isinstance(json_init["v_module"], int))
                and (json_init["v_module"] != 0)
                else None
            )
            self.port_idx: int = (
                json_init["port_idx"] if isinstance(json_init["port_idx"], int) else -1
            )
        self.comp_type: COMPONENT_TYPE = COMPONENT_TYPE.PORT

    def toDict(self) -> dict[str, str | int | list]:
        return super().toDict() | {
            "port_width": self.port_width,
            "port_type": self.port_type.name,
            "v_module": self.v_module.int if self.v_module is not None else 0,
            "port_idx": self.port_idx,
        }


class VReg(VInternal):
    def __init__(
        self,
        name: str = "",
        width: int = 0,
        v_module: UUID | None = None,
        json_init: dict[str, str | int | list] | None = None,
    ):
        super().__init__(name=name, width=width, v_module=v_module, json_init=json_init)
        self.comp_type: COMPONENT_TYPE = COMPONENT_TYPE.REG

    def toDict(self) -> dict[str, str | int | list]:
        return super().toDict()


class VWire(VInternal):
    def __init__(
        self,
        name: str = "",
        width: int = 0,
        v_module: UUID | None = None,
        json_init: dict[str, str | int | list] | None = None,
    ):
        super().__init__(name=name, width=width, v_module=v_module, json_init=json_init)
        self.comp_type: COMPONENT_TYPE = COMPONENT_TYPE.WIRE

    def toDict(self) -> dict[str, str | int | list]:
        return super().toDict()


class VInstance(VComponent):
    def __init__(
        self,
        name: str = "",
        v_module: UUID | None = None,
        json_init: dict | None = None,
    ):
        if json_init is None:
            super().__init__(name=name)
            if v_module is None:
                raise TypeError(
                    f"INSTANCE {self.name} MUST BE AN INSTANCE OF A NON-NONE MODULE!"
                )
            else:
                self.v_module: UUID = v_module
        else:
            super().__init__(
                name=json_init["name"] if isinstance(json_init["name"], str) else "",
                uuid=UUID(int=json_init["uuid"])
                if (isinstance(json_init["uuid"], int)) and (json_init["uuid"] != 0)
                else uuid4(),
            )
            if (not isinstance(json_init["v_module"], int)) or (json_init["uuid"] == 0):
                raise TypeError(
                    f"INSTANCE {self.name} MUST BE AN INSTANCE OF A NON-NONE MODULE!"
                )
            else:
                self.v_module = UUID(int=json_init["v_module"])
        self.comp_type: COMPONENT_TYPE = COMPONENT_TYPE.INSTANCE

    def toDict(self) -> dict[str, str | int | list]:
        return super().toDict() | {"v_module": self.v_module.int}


class VModule(VComponent):
    def __init__(
        self,
        name: str = "",
        mod_idx: int = 0,
        portlist: list[UUID] = [],
        declared_instances: list[UUID] = [],
        json_init: dict[str, str | int | list] | None = None,
    ):
        if json_init is None:
            super().__init__(name=name)
            self.mod_idx: int = mod_idx
            self.portlist: list[UUID] = portlist
            self.declared_instances: list[UUID] = declared_instances
        else:
            super().__init__(
                name=json_init["name"] if isinstance(json_init["name"], str) else "",
                uuid=UUID(int=json_init["uuid"])
                if isinstance(json_init["uuid"], int)
                else uuid4(),
            )
            self.mod_idx: int = (
                json_init["mod_idx"] if isinstance(json_init["mod_idx"], int) else 0
            )
            self.portlist: list[UUID] = []
            for value in (
                json_init["portlist"] if isinstance(json_init["portlist"], list) else []
            ):
                if isinstance(value, int):
                    if value == 0:
                        raise TypeError(
                            f"PORTLIST OF {self.name} MODULE CONTAINED INVALID ENTRY"
                        )
                    self.portlist.append(UUID(int=value))
                else:
                    raise TypeError(
                        f"PORTLIST OF {self.name} MODULE CONTAINED INVALID ENTRY"
                    )
            self.declared_instances: list[UUID] = []
            for value in (
                json_init["declared_instances"]
                if isinstance(json_init["declared_instances"], list)
                else []
            ):
                if isinstance(value, int):
                    if value == 0:
                        raise TypeError(
                            f"DECLARED INSTANCE LIST OF {self.name} MODULE CONTAINED INVALID ENTRY"
                        )
                    self.declared_instances.append(UUID(int=value))
                else:
                    raise TypeError(
                        f"DECLARED INSTANCE LIST OF {self.name} MODULE CONTAINED INVALID ENTRY"
                    )
        self.comp_type: COMPONENT_TYPE = COMPONENT_TYPE.MODULE

    def toDict(self) -> dict[str, str | int | list]:
        return super().toDict() | {
            "mod_idx": self.mod_idx,
            "portlist": [port_uuid.int for port_uuid in self.portlist],
            "declared_instances": [
                instance_uuid.int for instance_uuid in self.declared_instances
            ],
        }

    def addPort(self, p_uuid: UUID) -> int:
        """
        Adds a port UUID to the portlist for this module.

        Params:
            p_uuid: The UUID of the port to add

        Returns: The number of ports in the module after the addition of the new port.
        """
        self.portlist.append(p_uuid)
        return len(self.portlist)
