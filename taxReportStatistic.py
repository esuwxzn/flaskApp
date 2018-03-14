#!/usr/bin/pythssedTransactionData
#coding: UTF-8
from dataClasses import taxStatisticData, processedTransactionData


from sqlOperation import sqlOperation
from fileGenerator import fileGenerator
from dataProcessor import dataProcessor

from sqlDatabaseConf import databaseList


class taxReportStatistic:

    def __init__(self, start, end, remittance):
        #self.fileGenerator = fileGenerator()

        self.data = taxStatisticData()
        self.processedTransData = processedTransactionData()
        self.database = databaseList()
        self.remittance = remittance

        self.database.transaction.inwardTable = 'inward_' + start
        self.database.transaction.outwardTable = 'outward_' + start

        self.start = start
        self.end = end
        self.remittance = remittance
        print self.database.transaction.inwardTable
        print self.database.transaction.outwardTable


#    def generateQuerySQL(self, table, queryType):
    def generateQuerySQL(self, **queryInfo):
        
        queryType = queryInfo['queryType']
        table = queryInfo['table']

        if queryType == 'INWARD':

            return "SELECT DP03_VALU_DATE, CP03_EXTN_REF_NO, FROM_CON, CP03_PAY_AMT, CP03_PAY_CURR, CP03_BEN_CUS_NO FROM %s" % table

        elif queryType == 'OUTWARD':

            return "SELECT DP04_VALU_DATE, CP04_EXTN_REF_NO, TO_CON, CP04_PAY_AMT, CP04_PAY_CURR, CP04_MSG_DATA, CP04_BENF_DETL, SENDER FROM %s" % table 



    def queryData(self, queryType):
        
        database = ''
        sql = ''
        queryInfo = {}

        SQL = sqlOperation()
        
        queryInfo['queryType'] = queryType 

        if queryType == 'INWARD':
            
            database = self.database.transaction.transactionDatabase
            
            queryInfo['table'] = self.database.transaction.inwardTable

            sql = self.generateQuerySQL(**queryInfo)
        
        elif queryType == 'OUTWARD':

            database = self.database.transaction.transactionDatabase

            queryInfo['table'] = self.database.transaction.outwardTable
            
            sql = self.generateQuerySQL(**queryInfo)

            #print sql

        elif queryType == 'EXCHANGERATE':
            database = self.database.exchangeRate.exchangeRateDatabase
            sql = generateQuerySQL(self.database.exchangeRateTable, queryType)
        
        elif queryType == 'ACCOUNTINFO':
            database = self.database.exchangeRateDatabase
            sql = generateQuerySQL(self.database.customerInfoTable, queryType)
        
        elif queryType == 'ACCOUNTINFO':
            print "Query type is %s" % queryType

        else:
            print "ERROR:Unsupported query type..."
            exit(0)
        
        SQL.run(database, sql)

        return SQL.data


    def retrieveData(self):
        
        self.data.inwardData = self.queryData('INWARD')
        self.data.outwardData = self.queryData('OUTWARD')
#        self.data.exchangeRateData = self.queryData('EXCHANGEREATE')
#        self.data.accountInfoData = self.queryData('ACCOUNTINFO') 
        #self.customerInfoData = self.queryData('CUSTOMERINFO')


    def processData(self, data, start, end, remittance):
        
        dp = dataProcessor(data, start, end, remittance)
        self.processedTransData = dp.run()


    def writeDataToFile(self, data):

        fg = fileGenerator(data)
        fg.run()

    def run(self):#Start time and end time is not handled here.

        self.retrieveData()
        self.processData(self.data, self.start, self.end, self.remittance)

        if self.remittance == 'inward':
            return self.processedTransData.inwardData

        if self.remittance == 'outward':
            # print self.processedTransData.outwardData.dataToReport
            return self.processedTransData.outwardData



        # self.writeDataToFile(self.processedTransData)
