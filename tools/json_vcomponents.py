from abc import abstractmethod
from uuid import UUID, uuid4
from enum import Enum


class PORT_TYPE(Enum):
    INPUT = 0
    OUTPUT = 1
    INOUT = 2


class VComponent:
    def __init__(self, name: str | None = None, uuid: UUID | None = None) -> None:
        self.name: str = name if isinstance(name, str) else ""
        self.uuid: UUID = uuid4() if uuid is None else uuid

    @abstractmethod
    def toDict(self) -> dict[str, str | int]:
        return {"name": self.name, "uuid": self.uuid.int}


class VInternal(VComponent):
    def __init__(
        self,
        name: str = "",
        width: int = 0,
        v_module: UUID | None = None,
        json_init: dict[str, str | int] | None = None,
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
    def toDict(self) -> dict[str, str | int]:
        return super().toDict() | {
            "width": self.width,
            "v_module": self.uuid if self.uuid is not None else 0,
        }


class VPort(VComponent):
    def __init__(
        self,
        name: str = "",
        port_width: int = 0,
        port_type: PORT_TYPE = PORT_TYPE.INPUT,
        v_module: UUID | None = None,
        port_idx: int = -1,
        json_init: dict[str, str | int] | None = None,
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

    def toDict(self) -> dict[str, str | int]:
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
        json_init: dict[str, str | int] | None = None,
    ):
        super().__init__(name=name, width=width, v_module=v_module, json_init=json_init)

    def toDict(self) -> dict[str, str | int]:
        return super().toDict()


class VWire(VInternal):
    def __init__(
        self,
        name: str = "",
        width: int = 0,
        v_module: UUID | None = None,
        json_init: dict[str, str | int] | None = None,
    ):
        super().__init__(name=name, width=width, v_module=v_module, json_init=json_init)

    def toDict(self) -> dict[str, str | int]:
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

    def toDict(self) -> dict[str, str | int]:
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
