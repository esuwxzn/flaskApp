#!/usr/bin/python
#coding:UTF-8


from taxReportStatistic import taxReportStatistic

report = taxReportStatistic('201703', '201709', 'inward')

report.run()
