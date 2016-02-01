__author__ = 'hentenka'
import os, sys
import psycopg2

from base import POSTGIS_DB_NAME, POSTGIS_PORT, POSTGIS_PWD, POSTGIS_USERNAME, IP_ADDRESS

def connect_to_DB(host, db_name, username, pwd, port):
    conn_string = "host='%s' dbname='%s' user='%s' password='%s' port='%s'" % (host, db_name, username, pwd, port)
    #print(conn_string)
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    return conn, cursor

def createTTMtable14(conn, cursor, table_name):
    # Create a table [table_name]
    cursor.execute("CREATE TABLE %s (from_id integer, to_id integer, walk_t integer, walk_d integer, pt_m_tt integer, pt_m_t integer, pt_m_d integer, car_m_t integer, car_m_d integer);" % table_name)
    conn.commit()

def createTTMtable15(conn, cursor, table_name):
    # Create a table [table_name]
    cursor.execute("CREATE TABLE %s (from_id integer, to_id integer, walk_t integer, walk_d integer, pt_r_tt integer, pt_r_t integer, pt_r_d integer,  pt_m_tt integer, pt_m_t integer, pt_m_d integer, car_r_t integer, car_r_d integer, car_m_t integer, car_m_d integer);" % table_name)
    conn.commit()

def createPrimaryKey(conn, cursor, table, col_name):
    # Create a primary key to database
    sql = "ALTER TABLE %s ADD COLUMN %s SERIAL" % (table, col_name)
    print(sql)
    cursor.execute(sql)
    conn.commit()

def vacuumTable(conn, cursor, table):
    # This function only vacuums space for re-use within same table
    # (if required use FULL parameter to entirely free space to the disk
    # (notice: requires a lot of space to do this because a copy is made during the vacuum process))
    old_isolation_level = conn.isolation_level
    conn.set_isolation_level(0)
    sql = "VACUUM (VERBOSE, ANALYZE) %s;" % table
    cursor.execute(sql)
    conn.commit()
    conn.set_isolation_level(old_isolation_level)

def vacuumFullTable(conn, cursor, table):
    old_isolation_level = conn.isolation_level
    conn.set_isolation_level(0)
    sql = "VACUUM (FULL, VERBOSE, ANALYZE) %s;" % table
    cursor.execute(sql)
    print(conn.notices)
    conn.commit()
    conn.set_isolation_level(old_isolation_level)

def dropColumn(conn, cursor, table, columns_list):

    table_to_change = "ALTER TABLE %s" % (table)
    command = ""
    for column in columns_list:
        command+= "DROP COLUMN %s, " % column
    command = command[:-2]
    sql = "%s %s" % (table_to_change, command)
    print(sql)

    # Drop columns from the table
    cursor.execute(sql)
    conn.commit()

def dropIndex(conn, cursor, index):
    sql = "DROP INDEX %s" % index
    cursor.execute(sql)
    conn.commit()

def createIndex(conn, cursor, table, column, index_col):
    sql = "CREATE INDEX %s ON %s (%s);" % (index_col, table, column)
    print(sql)

    cursor.execute(sql)
    conn.commit()

def setPrimaryKeyCol(conn, cursor, table, key_column):
    sql = "ALTER TABLE %s ADD PRIMARY KEY (%s);" % (table, key_column)
    print(sql)
    cursor.execute(sql)
    conn.commit()

def renameColumns(conn, cursor, table, oldName_newName_dict):
    for old_name, new_name in oldName_newName_dict.items():
        print(old_name, "==>", new_name)
        sql = "ALTER TABLE %s RENAME COLUMN %s TO %s;" % (table, old_name, new_name)
        cursor.execute(sql)

    conn.commit()

def main():

    # Authentication to host
    db_name, host, port, username, pwd = POSTGIS_DB_NAME, IP_ADDRESS, POSTGIS_PORT, POSTGIS_USERNAME, POSTGIS_PWD
    
    # Create connection to Database
    conn, cursor = connect_to_DB(db_name=db_name, host=host, username=username, pwd=pwd, port=port)

    # Create Table for Matrix 2015
    TABLE_NAME = "matrix2014"
    createTTMtable14(conn, cursor, table_name="%s" % TABLE_NAME)
    
        
if __name__ == "__main__":
    main()


