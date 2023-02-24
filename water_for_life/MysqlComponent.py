#!/usr/bin/python3
# -*- coding: utf-8 -*-
# ==============================================================================
#       Filename:  MysqlComponent.py
#         Author:  Kerwin
#        Created:  2022/12/1
#    Description:  同步的Mysql操作
# ==============================================================================
from sqlalchemy.orm import Session
from sqlalchemy.engine import reflection
from sqlalchemy import create_engine, MetaData, Table

from . import DataBaseManager
from .tables.NewsTable import BASE_ORM


class MysqlManager(DataBaseManager):
    """
    pip install pymysql
    """

    def __init__(self, config):
        super(MysqlManager, self).__init__(config=config)
        self.config = config
        self.engine = self.getEngine()

    def getEngine(self):
        user = self.config.get("user", 'admin')
        password = self.config.get("password", '123456')
        host = self.config.get("host", '127.0.0.1')
        port = self.config.get("port", 3306)
        db_name = self.config.get("db_name", '')
        charset = self.config.get("charset", 'utf8')
        db_url = "mysql+pymysql://{}:{}@{}:{}/{}?charset={charset}".format(user, password, host, port, db_name, charset=charset)
        engine = create_engine(db_url)
        metadata = BASE_ORM.metadata
        metadata.create_all(engine)
        return engine

    def getTables(self):
        tables = self.engine.table_names()
        return tables

    def getSqlText(self, table_name, fields):
        db_name = self.config.get("db_name", None)
        field_sql = list()
        for field in fields:
            field_sql.append(f"`{db_name}`.`{table_name}`.`{field}`")
        sql = f"select {', '.join(field_sql)} from `{db_name}`.`{table_name}`"
        return sql

    def getTableColumns(self, table_name):
        inspector = reflection.Inspector.from_engine(self.engine)
        columns = inspector.get_columns(table_name)
        return columns

    def insert(self, table_name, record):
        metadata = MetaData(bind=self.engine)
        table = Table(table_name, metadata, autoload=True, autoload_with=self.engine)
        session = Session(self.engine)
        session.execute(table.insert(), record)
        session.commit()

    def select(self, table_name, article_url_md5):
        metadata = MetaData(bind=self.engine)
        table = Table(table_name, metadata, autoload=True, autoload_with=self.engine)
        s = table.select().filter(table.c.article_url_md5 == article_url_md5)
        rows = self.engine.execute(s).all()
        return rows
