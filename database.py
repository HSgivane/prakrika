import sqlite3



con = sqlite3.connect("users.db")
cur = con.cursor()



def db_create(cur):    
    cur.execute("CREATE TABLE IF NOT EXISTS User ( vk_id serial NOT NULL, discord varchar (55), dota_id serial, agree_reg serial );")
    cur.execute("CREATE TABLE IF NOT EXISTS tg_balans ( id serial PRIMARY KEY, tg_id serial NOT NULL, balans serial NOT NULL);")
    cur.execute("CREATE TABLE IF NOT EXISTS react ( id serial PRIMARY KEY, react_id serial NOT NULL);")

 
#РАБОТА С ВК  
def db_vkid(vk_id, cur, con):
    cur.execute("SELECT * FROM User WHERE vk_id='{vk_id}'".\
                format(vk_id=vk_id))
    
    records = cur.fetchall()
    
    if not records:
        cur.execute("INSERT INTO User (vk_id) VALUES ('{vk_id}')".\
                    format(vk_id=vk_id))
        con.commit()
    else:
        return False

def db_dotaid_check(vk_id, dota_id, cur, con):
    cur.execute("SELECT * FROM User WHERE dota_id='{dota_id}' and vk_id != '{vk_id}'".\
                format(dota_id=dota_id, vk_id=vk_id))
    
    records = cur.fetchall()
    if not records:
        
        cur.execute("SELECT * FROM User WHERE vk_id='{vk_id}' and dota_id IS NOT NULL".\
                    format(vk_id=vk_id))    
    
        records = cur.fetchall()
    
        if not records:
            return True
        else:
            return records[0][2]
    else:
        return ('Have')

def db_dotaid(vk_id, dota_id, cur, con):
    cur.execute("SELECT * FROM User WHERE vk_id='{vk_id}' and dota_id IS NOT NULL".\
                format(vk_id=vk_id))
    
    records = cur.fetchall()
    
    if not records:
        cur.execute("UPDATE User SET (dota_id)=('{dota_id}') WHERE (vk_id) = ('{vk_id}')".\
                    format(dota_id=dota_id, vk_id=vk_id))
        con.commit()
        return True
    else:
        return False

def db_dsid_check(vk_id, ds_id, cur, con):
    cur.execute("SELECT * FROM User WHERE discord='{ds_id}' and vk_id != '{vk_id}'".\
                format(ds_id=ds_id, vk_id=vk_id))
    
    records = cur.fetchall()
    if not records:
        
        cur.execute("SELECT * FROM User WHERE vk_id='{vk_id}' and discord IS NOT NULL".\
                    format(vk_id=vk_id))    
    
        records = cur.fetchall()
    
        if not records:
            return True
        else:
            return records[0][1]
    else:
        return ('Have')
    
def db_dsid(vk_id, ds_id, cur, con):
    cur.execute("SELECT * FROM User WHERE vk_id='{vk_id}' and discord IS NOT NULL".\
                format(vk_id=vk_id))    
    
    records = cur.fetchall()
    
    if not records:
        cur.execute("UPDATE User SET (discord)=('{ds_id}') WHERE (vk_id) = ('{vk_id}')".\
                    format(ds_id=ds_id, vk_id=vk_id))
        con.commit()
        
    else:
        return False    

def db_dota_id_del(vk_id, cur, con):
    cur.execute("SELECT * FROM User WHERE vk_id='{vk_id}' and agree_reg IS NOT NULL".\
                format(vk_id=vk_id))    
    
    records = cur.fetchall()
    
    if not records:
        cur.execute("UPDATE User SET (dota_id) = NULL WHERE (vk_id) = ('{vk_id}')".\
                    format(vk_id=vk_id))
      
        con.commit()
        
    else:
        return False

def db_ds_id_del(vk_id, cur, con):
    cur.execute("SELECT * FROM User WHERE vk_id='{vk_id}' and agree_reg IS NOT NULL".\
                format(vk_id=vk_id))    
    
    records = cur.fetchall()
    
    if not records:
        cur.execute("UPDATE User SET (discord) = NULL WHERE (vk_id) = ('{vk_id}')".\
                    format(vk_id=vk_id))
      
        con.commit()
        
    else:
        return False

def agree_reg(vk_id, cur, con):
    cur.execute("SELECT * FROM User WHERE vk_id='{vk_id}' and discord IS NOT NULL and dota_id IS NOT NULL".\
                format(vk_id=vk_id))
    
    records = cur.fetchall()
    
    if not records:
        return False
    else:
        cur.execute("SELECT * FROM User WHERE vk_id='{vk_id}' and discord IS NOT NULL and dota_id IS NOT NULL and agree_reg IS NOT NULL".\
                    format(vk_id=vk_id)) 
        
        records = cur.fetchall()
        
        if not records:
            cur.execute("UPDATE User SET (agree_reg) = '1' WHERE (vk_id) = ('{vk_id}')".\
                        format(vk_id=vk_id))
            con.commit()
            return('Agree')
        else:
            return('Have')

def agree_reg_check(vk_id, cur, con):
    cur.execute("SELECT * FROM User WHERE vk_id='{vk_id}' and discord IS NOT NULL and dota_id IS NOT NULL".\
                format(vk_id=vk_id))
    
    records_ag = cur.fetchall()
    
    if not records_ag:
        return False
    else:
        cur.execute("SELECT * FROM User WHERE vk_id='{vk_id}' and discord IS NOT NULL and dota_id IS NOT NULL and agree_reg IS NOT NULL".\
                    format(vk_id=vk_id)) 
        
        records = list(cur.fetchall())
        
        if not records:
            return records_ag
        else:
            return ('Have')

#РАБОТА С ДИСКОРДОМ
def react_id(cur, con, react_id):
    cur.execute("UPDATE react SET (react_id) = ('{react_id}') WHERE (id) = '1'".\
                format(react_id=react_id))
    con.commit()


def check_id(cur, con, react_id):
    cur.execute("UPDATE react SET (react_id) = ('{react_id}') WHERE (id) = '2'".\
                format(react_id=react_id))
    con.commit()
