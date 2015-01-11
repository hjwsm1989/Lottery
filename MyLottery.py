#!coding: utf-8
__author__ = 'jun'
# 需求：
# 开发一个程序，读取彩票T的所有历史开奖数据，根据数据预测下一期开奖号码
#
# 步骤：
# a、获取历史开奖数据
#      自己写程序爬取，或者直接利用已总结的历史数据
#      现有的xls表格数据不全，需要自己爬部分数据，并插入指定表格；
# b、预测算法
# -- 随机算法
# -- 根据正态分布来预测
# -- ？
# c、输出预测的下一期结果
import os
import datetime
import random
import  xlrd
import urllib2
import operator

#marco
HERE = os.path.dirname(__file__)

class Excel(object):
    """
    操作excel表格类:读取、删除、新增等操作
    """
    def __init__(self, fn):
        self.fn = fn
        self.data = xlrd.open_workbook(fn)
        self.tables = self.data.sheets()

    def read(self):
        """
        读fn指向的execel文件
        :return:
        """
        return self.data

    def get_table(self, n):
        """
        获取第n个工作表对象
        :return:
        """
        table = None
        if n < len(self.tables):
            table = self.tables[n]
        return table

    def get_rows(self, table):
        """
        获取指定表的行数
        :return:
        """
        return table.nrows

    def get_cols(self, table):
        """
        获取指定表的列数
        :param table:
        :return:
        """
        return table.ncols

class Crawler(object):
    """
    网络爬虫类：用来从彩票网站爬取数据
    """
    def __init__(self):
        pass

    def fetch_data(self, url):
        """
        爬取指定url页面的数据
        :param url:
        :return:
        """
        f = urllib2.urlopen(url)
        return f.read()

class MyLottery(object):
    """
    彩票基类：提供预测基函数等
    """
    def __init__(self, excel):
        self.excel = excel
        self.crawler = Crawler()

    def do_predict(self):
        """
        执行预测算法，输出下期彩票的号码
        """
        pass

    def get_lastest_num(self):
        """
        获取最近一期的彩票代号
        :return:
        """
        pass

    def update_data(self):
        """
        更新彩票数据
        :return:
        """
        pass

    def fetch_data(self, url):
        """
        爬虫，获取数据
        """
        return self.crawler.fetch_data(url)

    def print_number(self):
        """
        打印幸运号
        :return:
        """
        pass

class DoubleColor(MyLottery):
    """
    双色球
    """
    def __init__(self, excel):
        MyLottery.__init__(self, excel)
        self.url = "http://datachart.500.com/ssq/history/history.shtml"
        self.rules = [
            [33, 6, "红球"],
            [16, 1, "蓝球"] #33选6， 16选1
        ]
        self.my_lucky_numbers = []

    def get_lastest_num(self):
        """
        获取最近一期的彩票代号
        :return:
        """
        year,week_num,week_day = datetime.datetime.now().isocalendar()
        num_every_week = 3
        week_days = [2, 4, 7]
        count = 0 #本周第几次
        for i in week_days:
            if week_day <= i:
                count += 1
        num = (week_num - 1) * num_every_week + count #可能涉及到节假日
        return num

    def update_data(self):
        """
        更新彩票数据
        :return:
        """
        data = self.fetch_data(self.url)
        pass

    def print_number(self):
        """
        打印幸运号
        :return:
        """
        stdout = ""
        index = 0
        for i in self.rules:
            sub_ret = self.my_lucky_numbers[index:index+i[1]]
            stdout += "%s: %s " % (i[2], sub_ret)
            index = index + i[1]
        print stdout

    def alg1(self):
        """
        最简单的预测算法
        从给定的规则中随机选取满足的号码
        :return:
        """
        for sec in self.rules:
            part_lucky_numbers = []
            total_nums = sec[0]
            need_nums = sec[1]
            for i in range(need_nums):
                while 1:
                    luck_num = random.randint(1, total_nums)
                    if luck_num in part_lucky_numbers:
                        continue
                    part_lucky_numbers.append(luck_num)
                    break
            self.my_lucky_numbers.extend(part_lucky_numbers)
        self.print_number()

    def alg2(self):
        """
        2号预测算法
        :return:
        """
        lucky_numbers = []
        table = self.excel.get_table(0)
        rows = self.excel.get_rows(table)
        title_num = 2
        for i in range(rows):
            if i >= title_num:
                row_data = table.row_values(i)
                num = row_data[0]
                reds = row_data[1:7]
                bule = row_data[7]
                print "彩期:%s 红球: %s 蓝球：%s" % (num, reds, bule)
                break
        #删除不必要的数据
        return lucky_numbers

    def alg3(self):
        """
        计算出所有的可能组合情况
        将这些组合插入到数据库
        初步筛选:
        a) 去掉以前出现的中奖号码
        b）去掉6连号、5连号、4连号的号码
        :return:
        """
        def c(n, r):
            """
            计算从n个不同的数字中取r个不同的数字
            """
            return  reduce(operator.mul, range(n-r+1, n+1)) /reduce(operator.mul, range(1, r+1))
        print c(33, 6)

    def do_predict(self):
        """
        双色球预测算法
        :return:
        """
        # self.alg1()
        self.alg3()
        # print "幸运号码: 红球 %s 蓝球 %s" % (self.my_lucky_numbers[0:], self.my_lucky_numbers[7])

def main():
    """
    主函数
    :return:
    """
    #双色球
    fn = os.path.join(HERE, "data", "DoubleColor.xlsx")
    my_excel = Excel(fn)
    my_dc = DoubleColor(my_excel)
    my_dc.do_predict()
    return my_dc.my_lucky_numbers

if __name__ == "__main__":
    main()