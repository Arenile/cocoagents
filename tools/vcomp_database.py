from json_vcomponents import VComponent
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

    def __init__(self, comp_list: dict[UUID, VComponent] = {}):
        self.comp_list: dict[UUID, VComponent] = comp_list

    def getComp(self, uuid: UUID) -> VComponent:
        return self.comp_list[uuid]

    def addComp(self, new_comp: VComponent) -> UUID:
        self.comp_list[new_comp.uuid] = new_comp

        return new_comp.uuid

    def setRemote(self, api_key: str):
        self.remote_api_key: str = api_key

    def fetchRemote(self, reconcillation_strategy: RECONCILE_STRAT):
        # TODO: Implement function that fetches a remote database of NoSQL format (JSON) and fills in data for the database view based on that.
        pass

    def contructFromAST(self, ast_source: vast.Source):
        # TODO: Construct database from a Verilog source file using PyVerilog, adds all modules in that source to exisitng database
        pass
