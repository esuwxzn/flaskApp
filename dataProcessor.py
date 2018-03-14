#!/usr/bin/python
#coding: UTF-8

from dataClasses import taxStatisticData, processedTransactionData
from sqlOperation import sqlOperation
from sqlDatabaseConf import databaseList
import re


class dataProcessor:

    def __init__(self, inputData, start, end, remittance):
        self.inputData = inputData
        self.processedData = processedTransactionData()
        self.database = databaseList()

        self.database.transaction.inwardTable = 'inward_' + start
        self.database.transaction.outwardTable = 'outward_' + start
        self.remittance = remittance
        # print self.database.transaction.inwardTable
        # print self.database.transaction.outwardTable


    def generateQuerySQL(self, **queryInfo):

        queryType = queryInfo['queryType']

        table = queryInfo['table']

        if queryType == 'EXCHANGERATE':
            
            currency = queryInfo['currency']
            date = queryInfo['date']
            #table = self.database.exchangeRateTable
            #return 'SELECT %s FROM %s WHERE DATE = %s' % (currency, table, date)
            return 'SELECT %s FROM %s WHERE DATE = %s' %\
                    (queryInfo['currency'],\
                     queryInfo['table'],\
                     queryInfo['date'])
        
        elif queryType == 'TAXCODE':
            key = queryInfo['key']
            CIF = queryInfo['CIF']
            #return 'SELECT %s FROM %s WHERE CIF  = %s' % (key, table, CIF)
            return 'SELECT %s FROM %s WHERE CIF  = %s' %\
                    (queryInfo['key'],\
                     queryInfo['table'],\
                     queryInfo['CIF'])

        elif queryType == 'CIF':
            customer_acc_key = queryInfo['customer_acc_key']
            account_number = queryInfo['account_number']
            cif_key = queryInfo['cif_key']
            #return 'SELECT %s FROM %s WHERE %s = %s' % (cif_key, table, customer_acc_key, account_number)
            return 'SELECT %s FROM %s WHERE %s = %s' % \
                    (queryInfo['cif_key'],\
                     queryInfo['table'],\
                     queryInfo['customer_acc_key'],\
                     queryInfo['account_number'])

        elif queryType == 'CUSTOMERINFO':
            title = queryInfo['title']
            street = queryInfo['street']
            area = queryInfo['area']
            city = queryInfo['city']
            country = queryInfo['country']
            post = queryInfo['post']
            personal_number = queryInfo['id']
            org_num = queryInfo['org_num']

            return 'SELECT %s, %s, %s, %s, %s, %s, %s FROM %s WHERE %s = %s' %\
                    (queryInfo['title'],\
                     queryInfo['street'],\
                     queryInfo['area'],\
                     queryInfo['city'],\
                     queryInfo['country'],\
                     queryInfo['post'],\
                     queryInfo['id'],\
                     queryInfo['table'],\
                     queryInfo['cif_key'],\
                     queryInfo['CIF'])







    def processCustomerInfo(self, customerInfo):
        
        title = customerInfo[0][0]

        address = customerInfo[0][1] + ' ' +\
                  customerInfo[0][2] + ' ' +\
                  customerInfo[0][3] + ' ' +\
                  customerInfo[0][4] + ' ' +\
                  customerInfo[0][5]
        
#        print address
        
        return [customerInfo[0][6], customerInfo[0][6], address]




    def retrieveData(self, **info):
        
        Type = info['type']

        if Type == 'CIF':
            queryInfo = {'queryType':Type, 'customer_acc_key':'INVM_MEMB_CUST_AC', 'account_number':info['account_number'], 'cif_key':'CD03_CUSTOMER_NO', 'table':self.database.invm.invmTable}
            database = self.database.customerInfo.customerInfoDatabase

        elif Type == 'TAXCODE':
            queryInfo = {'queryType':Type, 'key':'TAX_C', 'CIF':info['CIF'], 'table':self.database.customerInfo.customerInfoTable}
            database = self.database.customerInfo.customerInfoDatabase
        
        elif Type == 'EXCHANGERATE':
            queryInfo = {'queryType':Type, 'currency':info['currency'], 'date':info['valueDate'], 'table':self.database.exchangeRate.exchangeRateTable}
            database = self.database.exchangeRate.exchangeRateDatabase
        
        elif Type == 'CUSTOMERINFO':

            #The orginization number need to be updated.
            queryInfo = {'queryType':Type, 'title':'TITLE', 'cif_key':'CIF', 'CIF':info['CIF'], 'street':'STREET', 'area':'AREA', 'city':'CITY', 'country':'COUNTRY', 'post':'POST', 'id':'ID_N', 'org_num':'XXX' , 'table':self.database.customerInfo.customerInfoTable}
            database = self.database.customerInfo.customerInfoDatabase

        else:
            print "Unsupport query type in retrieveData()..."
            exit(0)
        
        SQL = sqlOperation()

        sql = self.generateQuerySQL(**queryInfo)
        #print sql 
        SQL.run(database, sql) 
       
        if len(SQL.data) != 0 and Type != 'CUSTOMERINFO':
            return SQL.data[0][0]
        elif Type == 'CUSTOMERINFO':
            #print SQL.data
            return self.processCustomerInfo(SQL.data)
        else:
            return ''



    def retrieveReason(self, message):

        return '\n'.join(re.findall(r':70:(.+?):71', message))


    def updateRow(self, row, **updateInfo):
   
        row = list(row)
        
        Type = updateInfo['type']
        #print row

        if Type == 'INWARD':

            row.append(updateInfo['exchangeRate'])
            row.append(updateInfo['SEK'])
            row.append(updateInfo['org_number'])
            row.append(updateInfo['personal_number'])
            row.append(updateInfo['address'])
            row.append(updateInfo['tax_code'])
        
        elif Type == 'OUTWARD':

            row[5] = updateInfo['reason']
            
            #if len(updateInfo['CIF']) == 0:
            #    print row[6]
            
            #Remove the sender from the list
            del row[6]
            
            #Insert the CIF
            row.insert(6, updateInfo['CIF'])

            row.append(updateInfo['exchangeRate'])
            row.append(updateInfo['SEK'])
            row.append(updateInfo['org_number'])
            row.append(updateInfo['personal_number'])
            row.append(updateInfo['address'])
            row.append(updateInfo['tax_code'])
        
        return tuple(row)


    def insertToOutputData(self, outputData, key, value):
        if not outputData.has_key(key):
            outputData[key] = [value,]
        else:
            outputData[key].append(value)
    



    def processInwardData(self, inputData):

        for row in inputData: 
        
            retrieveInfo = {}
            updateInfo = {}            
            
            valueDate    = row[0]
            from_country = row[2]
            amount       = row[3]
            currency     = row[4]
            cif_read     = row[5]

            if len(cif_read) != 0:

                retrieveInfo = {'type':'TAXCODE', 'CIF': cif_read}
                tax_code = self.retrieveData(**retrieveInfo)

            else:
                tax_code = ''

            if currency != 'SEK' and currency != '':
                retrieveInfo = {'type':'EXCHANGERATE', 'valueDate': valueDate, 'currency':currency}
                exchangeRate = self.retrieveData(**retrieveInfo)
                SEK = float(amount) * exchangeRate

                # print amount
                # print exchangeRate
                # print SEK
            elif currency == 'SEK':
                SEK = amount
            else:
                SEK = ''


            #Customer Info:Org number, personal number or address
            if cif_read != '':
                retrieveInfo = {'type':'CUSTOMERINFO', 'CIF':cif_read}
                customerInfo = self.retrieveData(**retrieveInfo)
            else:
                customerInfo = ('', '', '')
            

            updateInfo['type'] = 'INWARD'
            updateInfo['exchangeRate'] = exchangeRate
            updateInfo['SEK'] = SEK 
            updateInfo['tax_code'] = tax_code
            updateInfo['org_number'] = customerInfo[0]
            updateInfo['personal_number'] = customerInfo[1]
            updateInfo['address'] = customerInfo[2]

            updatedRow = self.updateRow(row, **updateInfo)


            #print updatedRow
            if cif_read != '' and from_country != 'SE' and from_country != '00':
                self.insertToOutputData(self.processedData.inwardData.dataToReport, cif_read, updatedRow)
                
            else:
                self.insertToOutputData(self.processedData.inwardData.dataToManual, cif_read, updatedRow)


    def processOutwardData(self, inputData):

        for row in inputData:

            retrieveInfo = {}
            updateInfo = {} 
            

            valueDate      = row[0]
            to_country     = row[2]
            amount         = row[3]
            currency       = row[4]
            message        = row[5]
            account_number = row[7]
            exchangeRate = 0
           

            if len(account_number) != 0 and account_number != 'NEED_TO_BE_CHECKED':
                
                retrieveInfo = {'type':'CIF', 'account_number': account_number}
                cif_read = self.retrieveData(**retrieveInfo) 
                
                if len(cif_read) != 0:
                    
                    retrieveInfo = {'type':'TAXCODE', 'CIF': cif_read}
                    tax_code = self.retrieveData(**retrieveInfo)

                else:
                    tax_code = ''
            
            else:
                cif_read = ''
                tax_code = ''
            
            if currency != 'SEK' and currency != '':
                retrieveInfo = {'type':'EXCHANGERATE', 'valueDate': valueDate, 'currency':currency}
                exchangeRate = self.retrieveData(**retrieveInfo)
                SEK = float(amount) * exchangeRate
            elif currency == 'SEK':
                SEK = amount
            else:
                SEK = ''
           

            #Customer Info:Org number, personal number or address
            if cif_read != '':
                retrieveInfo = {'type':'CUSTOMERINFO', 'CIF':cif_read}
                customerInfo = self.retrieveData(**retrieveInfo)
            else:
                customerInfo = ('', '', '')
            
            reason = self.retrieveReason(message)
           

            updateInfo['type'] = 'OUTWARD'
            updateInfo['reason'] = reason
            updateInfo['CIF'] = cif_read
            updateInfo['exchangeRate'] = exchangeRate
            updateInfo['SEK'] = SEK 
            updateInfo['tax_code'] = tax_code
            updateInfo['org_number'] = customerInfo[0]
            updateInfo['personal_number'] = customerInfo[1]
            updateInfo['address'] = customerInfo[2]

            updatedRow = self.updateRow(row, **updateInfo)


            if cif_read != '' and (to_country != 'SE' or tax_code != '99'):
                self.insertToOutputData(self.processedData.outwardData.dataToReport, cif_read, updatedRow)
                
            else:
                self.insertToOutputData(self.processedData.outwardData.dataToManual, cif_read, updatedRow)



    def distributeTransaction(self):
        if self.remittance == 'inward':
            self.processInwardData(self.inputData.inwardData)

        if self.remittance == 'outward':
            self.processOutwardData(self.inputData.outwardData)
    
    
    def run(self):
        
        self.distributeTransaction()
        return self.processedData
