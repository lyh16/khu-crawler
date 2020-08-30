#! /usr/bin/python3

import sqlite3

class DBMan:
#Crawler 테이블 최초 작성

	def __init__(self, dbname = "PATH/TO/DATABASE/khu.db"):
		self.dbname = dbname
		self.conn = sqlite3.connect(dbname, check_same_thread = False)

	def setup(self):
		stmt = "CREATE TABLE IF NOT EXISTS Gen_Pinned (notice_date text, crawl_dt text, issuer text, notice_title text, url text PRIMARY KEY DESC, msg_id int)"
		self.conn.execute(stmt)
		stmt1 = "CREATE TABLE IF NOT EXISTS Gen_Normal (notice_date text, crawl_dt text, issuer text, notice_title text, url text PRIMARY KEY DESC, msg_id int)"
		self.conn.execute(stmt1)
		stmt2 = "CREATE TABLE IF NOT EXISTS Und_Pinned (notice_date text, crawl_dt text, issuer text, notice_title text, url text PRIMARY KEY DESC, msg_id int)"
		self.conn.execute(stmt2)
		stmt3 = "CREATE TABLE IF NOT EXISTS Und_Normal (notice_date text, crawl_dt text, issuer text, notice_title text, url text PRIMARY KEY DESC, msg_id int)"
		self.conn.execute(stmt3)
		stmt4 = "CREATE TABLE IF NOT EXISTS Sch_Pinned (notice_date text, crawl_dt text, issuer text, notice_title text, url text PRIMARY KEY DESC, msg_id int)"
		self.conn.execute(stmt4)
		stmt5 = "CREATE TABLE IF NOT EXISTS Sch_Normal (notice_date text, crawl_dt text, issuer text, notice_title text, url text PRIMARY KEY DESC, msg_id int)"
		self.conn.execute(stmt5)
		stmt6 = "CREATE TABLE IF NOT EXISTS Cdx_Pinned (notice_date text, crawl_dt text, issuer text, notice_title text, url text PRIMARY KEY DESC, msg_id int)"
		self.conn.execute(stmt6)
		stmt7 = "CREATE TABLE IF NOT EXISTS Cdx_Normal (notice_date text, crawl_dt text, issuer text, notice_title text, url text PRIMARY KEY DESC, msg_id int)"
		self.conn.execute(stmt7)
		stmt8 = "CREATE TABLE IF NOT EXISTS Evt_Pinned (notice_date text, crawl_dt text, issuer text, notice_title text, url text PRIMARY KEY DESC, msg_id int)"
		self.conn.execute(stmt8)
		stmt9 = "CREATE TABLE IF NOT EXISTS Evt_Normal (notice_date text, crawl_dt text, issuer text, notice_title text, url text PRIMARY KEY DESC, msg_id int)"
		self.conn.execute(stmt9)
		self.conn.commit()

#함수 정의

	def add_notice(self, category, notice_date, crawl_dt, issuer, notice_title, url, msg_id):
		stmt = f"INSERT OR IGNORE INTO {category} VALUES (?, ?, ?, ?, ?, ?)"
		args = (notice_date, crawl_dt, issuer, notice_title, url, msg_id, )
		self.conn.execute(stmt, args)
		self.conn.commit()

	def del_notice(self, category, url):
		stmt = f"DELETE FROM {category} WHERE url = (?)"
		args = (url, )
		self.conn.execute(stmt, args)
		self.conn.commit()

	def get_notices(self, category):
		stmt = f"SELECT url FROM {category}"
		return [x[0] for x in self.conn.execute(stmt)]

	def get_notice_date(self, category, url):
		stmt = f"SELECT notice_date FROM {category} WHERE url = (?)"
		args = (url, )
		return [x[0] for x in self.conn.execute(stmt, args)][0]

	def get_msg_id(self, category, url):
		stmt = f"SELECT msg_id FROM {category} WHERE url = (?)"
		args = (url, )
		return [x[0] for x in self.conn.execute(stmt, args)][0]
