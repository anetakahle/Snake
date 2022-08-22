from abc import ABC, abstractmethod

class ISerializable:

    # public ----------------

    @abstractmethod
    def serialize(self) -> int :
        pass