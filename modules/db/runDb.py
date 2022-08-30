import os

import modules.db.dbcontext as db
import pathlib

db.clearDb()
schemaSql = pathlib.Path("schema.sql").read_text()
db.execSql(schemaSql)

dataSql = pathlib.Path("data.sql").read_text()
db.execSql(dataSql)

for file in os.listdir("clients"):
    clientSql = pathlib.Path("agents/" + file).read_text()
    db.execSql(clientSql)