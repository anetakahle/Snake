import enum
import numpy

def getInt(enumEntry):
    if isinstance(enumEntry, numpy.int64):
        return int(enumEntry)
    if isinstance(enumEntry , int):
        return enumEntry
    if isinstance(enumEntry.value , int):
        return int(enumEntry.value)
    return int(enumEntry.value[0])

class directions(enum.Enum):
    Left = -1
    Forward = 0
    Right = 1
    Skip = 2

class directions8(enum.Enum):
    Left = 0
    ForwardLeft = 1
    Forward = 2
    ForwardRight = 3
    Right = 4
    BackRight = 5
    Back = 6
    BackLeft = 7

    def __str__(self):
        if self.value == 0:
            return "L"
        elif self.value == 1:
            return "FL"
        elif self.value == 2:
            return "F"
        elif self.value == 3:
            return "FR"
        elif self.value == 4:
            return "R"
        elif self.value == 5:
            return "BR"
        elif self.value == 6:
            return "B"
        return "BL"

class logTypes(enum.Enum):
    Info = 0
    Ok = 1
    Warn = 2
    Error = 3

class gameStates(enum.Enum):
    NotStarted = 0,
    AwaitingServer = 1,
    AwaitingClient = 2,
    Finished = 3,
    NotSet = 4

class inputModes(enum.Enum):
    PlayerNative = 0
    PlayerTrans = 1
    PreComputed = 2
    Hook = 3
    PlayerAuto = 4

class renderModes(enum.Enum):
    PyGame = 0,
    Dormant = 1

class serverModes(enum.Enum):
    Manual = 0
    Auto = 1

class gameObjects(enum.Enum):
    OutsideOfBounds = -2
    Apple = -1
    Void = 0
    Head = 1
    Neck = 2
    Body = 30

    def __str__(self):
        if self.value == -2:
            return "Mimo pole"
        elif self.value == -1:
            return "Jablko"
        elif self.value == 0:
            return "Prazdno"
        elif self.value == 1:
            return "Hlava"
        elif self.value == 2:
            return "Zacatek tela"
        return "Telo"

class weightModes(enum.Enum):
    Zero = 0
    One = 1
    Random = 2

class biasModes(enum.Enum):
    Zero = 0
    One = 1
    Random = 2

class movementModes(enum.Enum):
    Human = 0
    Ai = 1

class gameCommands(enum.Enum):
    Unknown = -1
    SpawnObject = 0
    ClientMove = 1
    DestroyObject = 2
    SetProperty = 3
    CallMethod = 4,
    GameEnd = 5