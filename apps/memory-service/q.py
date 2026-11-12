import sqlite3;con=sqlite3.connect("memory.db");[print(r[0][:160]) for r in con.execute("select text from documents where text like ?",("%苔藓%",))]
