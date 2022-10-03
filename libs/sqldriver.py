import sqlite3 as sql
from venv import create

if __name__ == '__main__':
    print('Dont run this file directly')
else:
    def createDB(name):
        conn = sql.connect(name)
        conn.commit()
        conn.close()
    
    def createTable(bd, name):
        conn = sql.connect(bd)
        cursor = conn.cursor()
        cursor.execute(f"""CREATE TABLE '{name}' (
            name text,
            price integer
        )""")
        conn.commit()
        conn.close()
        
        
    def createTable2(bd, name):
        conn = sql.connect(bd)
        cursor = conn.cursor()
        cursor.execute(f"""CREATE TABLE '{name}' (
            datatime text,
            mensaje text
        )""")
        conn.commit()
        conn.close()

    def anyIns(bd, table, name, price):
        conn = sql.connect(bd)
        cursor = conn.cursor()
        consulta = f"INSERT INTO '{table}' VALUES ('{name}', {price})"
        cursor.execute(consulta)
        conn.commit()
        conn.close()

    def itemIns(bd, table, name, price):
        try:
            conn = sql.connect(bd)
            cursor = conn.cursor()
            consulta = f"INSERT INTO '{table}' VALUES ('{name}', {price})"
            cursor.execute(consulta)
            conn.commit()
            conn.close()
        except Exception as e:
            sendException('itenmIns func:', str(e))
            

    def itemS_all(bd, table):
        conn = sql.connect(bd)
        cursor = conn.cursor()
        consulta = f"SELECT * FROM '{table}'"
        cursor.execute(consulta)
        datos = cursor.fetchall()
        conn.commit()
        conn.close()
        return datos
    
    def itemLasttwo(bd, table):
        conn = sql.connect(bd)
        cursor = conn.cursor()
        consulta = """SELECT * from {table} LIMIT 2 ORDER BY datetime DESC LIMIT 2"""
        mensajes_list = []
        for row in cursor.execute(consulta):
            mensajes_list.append(row[2])
            
        
        if mensajes_list[0] == mensajes_list[1]:
            return
        else:
            pass
        
        conn.commit()
        conn.close()
        
        

    def itemUpdt(bd, table, name, price):
        conn = sql.connect(bd)
        cursor = conn.cursor()
        consulta = f"UPDATE '{table} SET price='{price}' WHERE name='{name}')"
        cursor.execute(consulta)
        conn.commit()
        conn.close()   
    
    def makeDB():
        createDB('items.db')
        createTable('items.db', 'items')

            
            
    def anyIns2(bd, table, mensajes):
        conn = sql.connect(bd)
        cursor = conn.cursor()
        consulta = f"INSERT INTO '{table}' VALUES ('{mensajes}')"
        cursor.execute(consulta)
        conn.commit()
        conn.close()