import sqlite3
import modules.root as root
import modules.utils.parse as parse

dbFileName = "/db/database.db"

def clearDb():
    open(root.dir + dbFileName, 'w').close()

def getDb() -> sqlite3.Connection:
    return sqlite3.connect(root.dir + dbFileName)

def execSql(sql : str):
    ctx = getDb()
    crs = ctx.cursor()
    crs.executescript(sql)
    return crs.fetchall()

def query(sql : str):
    ctx = getDb()
    crs = ctx.cursor()
    crs.execute(sql)
    return crs.fetchall()

def insertGetId(sql : str) -> int :
    ctx = getDb() # ctx = context = api k tabulce
    crs = ctx.cursor() # pointer na databazi
    crs.execute(sql)
    ctx.commit() # potvrzeni operace

    return parse.tryParseInt(crs.lastrowid)