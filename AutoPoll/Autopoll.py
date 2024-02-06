from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import cx_Oracle
from flask import flash
from datetime import datetime
import pandas as pd

import socket
import struct
from pymodbus.utilities import computeCRC
#from werkzeug.security import generate_password_hash
from sqlalchemy import desc

import cx_Oracle
#from cx_Oracle import pool

############  connect database  #####################
username = "root"
password = "root"
hostname = "192.168.102.192"
port = "1521"
service_name = "orcl"

dsn = cx_Oracle.makedsn(hostname, port, service_name)
    
try:
    connection_info = {
        "user": username,
        "password": password,
        "dsn": dsn,
        "min": 1,
        "max": 5,
        "increment": 1,
        "threaded": True
    }

    connection_pool = cx_Oracle.SessionPool(**connection_info)
    connection = connection_pool.acquire()
    print("Success")
except cx_Oracle.Error as e:
    (error,) = e.args
    print("Oracle Error:", error)
    exit()


def executeSelect(text_query):
    try:
        with connection.cursor() as cursor:
            #if params:
            #    cursor.execute(query, params)
            #else:
            #    cursor.execute(query)
            cursor.execute(text_query)
            results = cursor.fetchall()
        return results
    except cx_Oracle.Error as e:
        (error,) = e.args
        print("Oracle Error:", error)
        return []
    

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect((tcp_ip, tcp_port))

if __name__ == '__main__':
    print(executeSelect("Select * from tab"))
    pass
    
    
connection_pool.release(connection)