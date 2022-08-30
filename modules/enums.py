import enum
import numpy
import math as math

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
    CallMethod = 4
    GameEnd = 5

class gameEndReasons(enum.Enum):
    Win = 0
    OutOfBounds = 1
    TurnStrikeLimitExceeded = 2
    AppleNotCollectedInLimit = 3
    SelfCollision = 4
    MovesLimitExceeded = 5

class nodeTypes(enum.Enum):
    Input = 0
    Output = 1
    Hidden = 2

class activationFunctions(enum.Enum):
    Logistic = 0
    Tanh = 1
    Identity = 2
    Step = 3
    Relu = 4
    Softsign = 5
    Sinusoid = 6
    Gaussian = 7
    BentIdentity = 8
    HardTanh = 9
    Absolute = 10
    Inverse = 11
    Selu = 12
    Bipolar = 13
    BipolarSigmoid = 14

    def Call(self, x : float, derivate : bool) -> float:
        if self is activationFunctions.Logistic:
            fx = 1 / (1 + math.exp(-x))
            if not derivate:
                return fx
            return fx * (1 - fx)
        elif self is activationFunctions.Tanh:
            if derivate:
                return 1 - math.pow(math.tanh(x), 2)
            return math.tanh(x)
        elif self is activationFunctions.Identity:
            return 1 if derivate else x
        elif self is activationFunctions.Step:
            return 0 if derivate else 1 if x > 0 else 0
        elif self is activationFunctions.Relu:
            if derivate:
                return 1 if x > 0 else 0
            return x if x > 0 else 0
        elif self is activationFunctions.Softsign:
            d = 1 + abs(x)
            if derivate:
                return x / math.pow(d, 2)
            return x / d
        elif self is activationFunctions.Sinusoid:
            if derivate:
                return math.cos(x)
            return math.sin(x)
        elif self is activationFunctions.Gaussian:
            d = math.exp(-math.pow(x, 2))
            if derivate:
                return -2 * x * d
            return d
        elif self is activationFunctions.BentIdentity:
            d = math.sqrt(math.pow(x, 2) + 1)
            if derivate:
                return x / (2 * d) + 1
            return (d - 1) / 2 + x
        elif self is activationFunctions.Bipolar:
            return 0 if derivate else 1 if x > 0 else -1
        elif self is activationFunctions.BipolarSigmoid:
            d = 2 / (1 + math.exp(-x)) - 1
            if derivate:
                return 1 / 2 * (1 + d) * (1 - d)
            return d
        elif self is activationFunctions.HardTanh:
            if derivate:
                return 1 if -1 < x < 1 else 0
            return max(-1, min(1, x))
        elif self is activationFunctions.Absolute:
            if derivate:
                return -1 if x < 0 else 1
            return abs(x)
        elif self is activationFunctions.Inverse:
            if derivate:
                return -1
            return 1 - x
        elif self is activationFunctions.Selu:
            alpha = 1.6732632423543772848170429916717
            scale = 1.0507009873554804934193349852946
            fx = x if x > 0 else alpha * math.exp(x) - alpha
            if derivate:
                return scale if x > 0 else (fx + alpha) * scale
            return fx * scale
        else:
            return 0.0

class selectionMethods(enum.Enum):
    Power = 0
    FitnessProportionate = 1
    Tournament = 2

    PowerParamPower = 4
    TournamentParamSize = 5
    TournamentParamProbability = 0.5