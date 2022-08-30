import modules.db.iSerializable as iSerializable
import modules.db.dbcontext as db

class AgentBase(iSerializable.ISerializable):

    # properties ---------------

    dbId : int = 0
    runtimeId : str = ''

    # ctor --------------

    def __init__(self):
        pass

    # public ----------------

    def onAppleCollected(self):
        pass

    def serialize(self) -> int:
        return db.insertGetId(f"""
            insert into ClientGenerationAgents (runtimeId, clientGenerationId) 
            values ('{self.runtimeId}', null)
        """)[0]