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
    def __init__(self, is_master):
        if is_master:
            self.client = connect(
                host=get_config_values("sql_master", "host"),
                port=get_config_values("sql_master", "port"),
                user=get_config_values("sql_master", "user"),
                password=get_config_values("sql_master", "password"),
                database=get_config_values("sql_master", "database")
            )
            self.cursor = self.client.cursor()
        else:
            self.client = connect(
                host=get_config_values("sql_slave", "host"),
                port=get_config_values("sql_slave", "port"),
                user=get_config_values("sql_slave", "user"),
                password=get_config_values("sql_slave", "password"),
                database=get_config_values("sql_slave", "database")
            )
            self.cursor = self.client.cursor()

    def query(self, sql, size="all"):
        self.cursor.execute(sql)
        if size == "all":
            return self.cursor.fetchall()
        return self.cursor.fetchmany()

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
        except Exception as e:
            self.client.rollback()

    def __del__(self):
        self.cursor.close()


