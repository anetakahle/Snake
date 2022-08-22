import modules.db.dbcontext as db

lastId = db.insertGetId(f"""
    insert into ClientGenerations (clientId, "index") 
    values (1, 100)
""")

x = lastId