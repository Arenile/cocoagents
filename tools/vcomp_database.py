from json_vcomponents import (
    COMPONENT_TYPE,
    VComponent,
    VConnection,
    VInstance,
    VModule,
    VPort,
    VReg,
    VWire,
)
from uuid import UUID
from enum import Enum
import pyverilog.vparser.ast as vast


class RECONCILE_STRAT(Enum):
    OVERWRITE_REMOTE = 0
    OVERWRITE_LOCAL = 1


class VCompDatabaseView:
    """
    Implements a view on the database of Verilog Components we have to work with
    for designing a device.
    """

    def __init__(self):
        self.comp_list: dict[UUID, dict[str, str | int | list]] = {}

    def getComp(self, uuid: UUID):
        match self.comp_list[uuid]["comp_type"]:
            case COMPONENT_TYPE.REG.name:
                return VReg(json_init=self.comp_list[uuid])
            case COMPONENT_TYPE.MODULE.name:
                return VModule(json_init=self.comp_list[uuid])
            case COMPONENT_TYPE.WIRE.name:
                return VWire(json_init=self.comp_list[uuid])
            case COMPONENT_TYPE.PORT.name:
                return VPort(json_init=self.comp_list[uuid])
            case COMPONENT_TYPE.INSTANCE.name:
                return VInstance(json_init=self.comp_list[uuid])
            case COMPONENT_TYPE.CONNECTION.name:
                return VConnection(json_init=self.comp_list[uuid])
            case _:
                return VComponent()

    def addComp(self, new_comp: VComponent) -> UUID:
        self.comp_list[new_comp.uuid] = new_comp.toDict()

        return new_comp.uuid

    #    def addConnection(self, new_conn: VConnection) -> UUID:
    #        self.comp_list[new_conn.uuid] = new_conn.toDict()
    #
    #        return new_conn.uuid

    def setRemote(self, api_key: str):
        self.remote_api_key: str = api_key

    def fetchRemote(self, reconcillation_strategy: RECONCILE_STRAT):
        # TODO: Implement function that fetches a remote database of NoSQL format (JSON) and fills in data for the database view based on that.
        pass

    def contructFromAST(self, ast_source: vast.Source):
        # TODO: Construct database from a Verilog source file using PyVerilog, adds all modules in that source to exisitng database
        pass
