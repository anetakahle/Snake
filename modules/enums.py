import enum

class directions(enum.Enum):
    Left = -1,
    Forward = 0,
    Right = 1

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
    PyGame = 0