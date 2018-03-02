import time
from openpyxl import Workbook
from dataClasses import excelHeader


class fileGenerator:

    def __init__(self, inputData):

        self.data = inputData
        self.header = excelHeader()
        self.wb = ''


    def writeDataToSheet(self, inputData, sheet, header):

        sheet.append(header)

        keys = inputData.keys()
        
        for key in keys:
            for row in inputData[key]:
                sheet.append(row)


    def writeDataToFile(self, fileType):

        self.wb = Workbook()

        if fileType == 'INWARD':
            titleToReport = self.header.inwardSheetTitle.toReport
            titleToManual = self.header.inwardSheetTitle.toManual
            header = self.header.inwardHeader
            #filename = 'Inward_Remittance_' + time.strftime("%Y%m%d_%X", time.localtime()) + '.xlsx'
            filename = 'Inward_Remittance_' + time.strftime("%Y%m%d", time.localtime()) + '.xlsx'

            dataToReport = self.data.inwardData.dataToReport
            dataToManual = self.data.inwardData.dataToManual

        elif fileType == 'OUTWARD':
            titleToReport = self.header.outwardSheetTitle.toReport
            titleToManual = self.header.outwardSheetTitle.toManual
            header = self.header.outwardHeader
            
            filename = 'Outward_Remittance_' + time.strftime("%Y%m%d", time.localtime()) + '.xlsx'

            dataToReport = self.data.outwardData.dataToReport
            dataToManual = self.data.outwardData.dataToManual


        index = 0
        sheet = self.wb.worksheets[index]
        sheet.title = titleToReport 
        self.writeDataToSheet(dataToReport, sheet, header)

        index += 1
        self.wb.create_sheet()
        sheet = self.wb.worksheets[index]
        sheet.title = titleToManual
        self.writeDataToSheet(dataToManual, sheet, header)

        #filename = r'./%s' % filename
        print filename
        self.wb.save(r'./%s' % filename)


    def run(self):
        self.writeDataToFile('INWARD')
        self.writeDataToFile('OUTWARD')
