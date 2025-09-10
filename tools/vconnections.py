from json_vcomponents import VModule
from uuid import UUID


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


class VDesign:
    pass
