from pymysql import connect
import os
import configparser

# 项目路径
rootDir = os.path.split(os.path.realpath(__file__))[0]
# config.ini文件路径
configFilePath = os.path.join(os.path.join(rootDir, 'config'), 'sql.ini')


def get_config_values(section, option):
    config = configparser.ConfigParser()
    config.read(configFilePath)
    # return config.items(section=section)
    return config.get(section=section, option=option)


class SQLTool:
    def __init__(self, is_master=True):
        self.client = connect(host="192.168.45.160", port=3306, user="root", password="casper", database="madblog")
        self.cursor = self.client.cursor()

    def query(self, sql, size="all"):
        print(sql)
        self.cursor.execute(sql)
        if size == "all":
            return self.cursor.fetchall()
        return self.cursor.fetchone()

    def insert(self, sql):
        print(sql)
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception as e:
            self.client.rollback()


SQL = SQLTool()
