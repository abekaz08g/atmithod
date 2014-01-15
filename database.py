#-*-coding:utf-8-*=
from pymongo import Connection
import xml.etree.ElementTree as ET

"""
atmithod のデータベース操作用ライブラリ
"""


def getServerSettings(configxml):
    """
    設定ファイルconfigxmlから，サーバーの設定を読み込み
    """
    tree = ET.parse(configxml)
    treeroot = tree.getroot()
    return treeroot


class database:
    """
    データベース操作用クラス
    """
    def __init__(self, configxml):
        """
        データベースへの接続
        """
        self.config = getServerSettings(configxml)
        dbSettings = self.config.find('database').attrib
        serverroot = dbSettings['root']
        port = int(dbSettings['port'])
        self.con = Connection(serverroot, port)
        self.db = self.con[dbSettings['dbname']]

    def getLBbase(self):
        """
        教科書コレクションを返す
        """
        return self.db[self.config.find('lbbase').attrib['name']]

    def getCDS(self):
        """
        can-do記述文コレクションを返す
        """
        return self.db[self.config.find('cds').attrib['name']]

    def getSerepo(self):
        """
        事例コレクションを返す
        """
        return self.db[self.config.find('serepo').attrib['name']]

    def close(self):
        """
        データベースとの接続を解除
        """
        self.con.close()
