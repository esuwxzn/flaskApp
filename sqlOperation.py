#!/usr/bin/python
#coding: UTF-8
import os
import MySQLdb

from dataClasses import taxStatisticData
from sqlDatabaseConf import sqlDatabaseConf

class sqlOperation:

    def __init__(self):
        self.dbConf = sqlDatabaseConf()
        self.data = taxStatisticData()
        self.cursor = ''
        self.db = ''


    def connectToDatabase(self, database):

        #Connect to MySQL    
        self.db = MySQLdb.connect(self.dbConf.host, self.dbConf.username, self.dbConf.password, database)
        self.cursor = self.db.cursor()

    def queryData(self, sql):
        
        self.cursor.execute(sql)

        self.data = self.cursor.fetchall()
#        print self.data

    def closeSQLConnection(self):

        self.db.close()


    def run(self, database, sql):

        self.connectToDatabase(database)
        self.queryData(sql)
        self.closeSQLConnection()
        
        return self.data
