import datetime

def sqlNow() -> str:
    now = datetime.datetime.now()

    def td(val : int):
        if len(str(val)) < 2:
            return f"0{val}"
        return str(val)

    return f"{now.year}-{td(now.month)}-{td(now.day)} {td(now.hour)}:{td(now.minute)}:{td(now.second)}"