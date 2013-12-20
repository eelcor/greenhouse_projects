#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2013 Ubuntu User <ubuntu@ubuntu-armhf>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from flask import Flask, render_template, request, redirect, url_for, abort, session, jsonify
from weather import weather
import thread, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logger_base import Item, Average, Base
import datetime
from dateutil import parser

app = Flask(__name__)

@app.route('/')
def home():
	return 'Hello World'

if __name__ == '__main__':
	engine = create_engine('sqlite:///logbase_read.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	app.run(host='0.0.0.0', port=2000)
