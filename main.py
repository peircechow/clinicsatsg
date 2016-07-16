#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2
import cgi
import datetime
import calendar
import re
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
	
class Clinic(ndb.Model):
# #	#fields with multiple values will be split into array
	location = ndb.StringProperty()
	name = ndb.StringProperty()
	address = ndb.StringProperty()
	telephone = ndb.StringProperty()
	open_1 = ndb.StringProperty()
	open_2 = ndb.StringProperty()
	open_3 = ndb.StringProperty()
	open_4 = ndb.StringProperty()
	days_closed = ndb.StringProperty()

# def create_entity():
    # clinic = Clinic()
	# clinic.location = ""
	# clinic.name = "Bedok Day & Night Clinic"
	# clinic.address = "418 Bedok North Ave 2 01-85 Singapore 460418"
 
	# clinic.telephone = "64441104"
	# clinic.open_1 = "Mon, Wed & Fri:	0900 - 1230; 1330 - 1530; 1830 - 2130"
	# clinic.open_2 = "Tue & Thu:	0900 - 1230; 1530 - 1830"
	# clinic.open_3 = "Sat:	0900 - 1230"
	# clinic.open_4 = "Sun & PH:	0900 - 1230; 1830 - 2030"
	# clinic.days_closed = " 4564 "
	# clinic.opening_display = " Mon, Wed & Fri:	0900 - 1230; 1330 - 1530; 1830 - 2130 \
# Tue & Thu:	0900 - 1230; 1530 - 1830 \
# Sat:	0900 - 1230 \
# Sun & PH:	0900 - 1230; 1830 - 2030"
    # return clinic
	
# # save_model(clinic):
# #    clinic_key = clinic.put()
 #   return clinic_key
	
def Clinic_Key():
	return ndb.Key("Clinic",1)

def check_int(n):
	try:
		int(n)
		if len(str(n)) == 4:
			return True
		else:
			return False
	except ValueError:
		return False
		
def stripper(a):
	details = a.replace(';',' ')
	details = details.replace(':',' ')
	details = details.replace(',',' ')
	details = details.replace('<br>',' ')
	
	details = details.split()
	return details
	
def stripper_time(a):
	details = a.replace(';',' ')
	details = details.replace(':',' ')
	details = details.replace(',',' ')
	details = details.replace('<br>',' ')
	details = details.replace('_',' ')
	details = details.split()
	return details
	
def find_index(a,target):
	index = 0
	for day in a:
		if target == day:
			return index
		index +=1
	return -1
	
def compare(b, curr_day): #to compare whether curr_day is in 'open' , else move on to nxt value
	days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri' ,'Sat', 'Sun']
	try:
		if b[1] == '-':		
			compare_days =  days[int(find_index(days,b[0])):int(int(find_index(days,b[2]))+1)]
			for day in compare_days:
				if day == curr_day:
					return True
		for word in b:
			if word == curr_day:
				return True
		return False
	except:
		return False
	
def compare_timings(a,curr_time): #returning True will mean clnic is open, False if otherwise
	o_timings = []
	c_timings = []
	counter = 1
	for timing in a:
		if check_int(timing):
			if counter % 2 == 1:
				o_timings.append(timing)
			else:
				c_timings.append(timing)
			counter += 1
			
	try:		
		for t in range(len(o_timings)):
			if int(o_timings[t]) <= int(curr_time) <= int(c_timings[t]):
				return True
			elif int(o_timings[t])>= int(c_timings[t]) and int(o_timings[t]) <= int(curr_time):
				return True
		return False
		
	except:
		pass
	
	

class MainHandler(webapp2.RequestHandler): #home page
	def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('home.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))

class About(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('about.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))

class Health_tips(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('health_tips.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))

class North(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('north.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))

		
class Northeast(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('northeast.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))
		
class East(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('east.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))
		
class Central(webapp2.RequestHandler):
	def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('central.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))
		
class West(webapp2.RequestHandler):	
	def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('west.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))
		
class Open_close(webapp2.RequestHandler):

	def get(self):
		#my_date = date.today()
		now = datetime.datetime.now()
		curr_day= calendar.day_name[datetime.date.today().weekday()] #may be wrong
		curr_hour = str((now.hour +8)%24) #Sg is UTC + 8
		curr_min = now.minute
		if len(str(curr_min))==1:
			curr_min = '0' + str(curr_min)
		curr_time = int(str(curr_hour)+str(curr_min))
		curr_day = curr_day[:3]
		#self.response.write(curr_time)
		
		clinic_data=[]
		o_data=[]
		c_data=[]
		
		days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri' ,'Sat', 'Sun']
		
		
		##query for location
		location = self.request.get("location") #CORRECT
		location = location.replace('_', ' ')
		self.response.write('<h1>Clinics@SG</h1>')
		self.response.write('<h3>%s</h3>'%location)
		
		clinic_query = Clinic.query()
		
		clinics = clinic_query.fetch() # get back in list
		for clinic in clinics:
			c_location = clinic.location.replace('_', ' ')
			if c_location == location:
				clinic_data.append(clinic)
		
												
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('open_close.html') #change the file to the relevant html file
		self.response.write(template.render(template_values))
		
		
		for clinic in clinic_data:
			details_1 = stripper_time(clinic.open_1)
			if compare(details_1, curr_day):
				if compare_timings(details_1 ,curr_time):
					o_data.append(clinic)
				else:
					c_data.append(clinic)
			else:
				details_2 = stripper(clinic.open_2)
				if compare(details_2,curr_day):
						#compare timings here 
					if compare_timings(details_2, curr_time):
						o_data.append(clinic)
					else: 
						c_data.append(clinic)
				else:
					details_3 = stripper(clinic.open_3)
					if compare(details_3, curr_day):
						if compare_timings(details_3, curr_time):
							o_data.append(clinic)
						else:
							c_data.append(clinic)
					else:
						details_4 = stripper(clinic.open_4)
						if compare(details_4, curr_day):
							if compare_timings(details_4, curr_time):
								o_data.append(clinic)
							else:
								c_data.append(clinic)
		#self.response.write(details_1)
		#self.response.write(details_1[0])
		#self.response.write('<br>')
		#self.response.write(o_data)
		#self.response.write(c_data)
		for data in o_data:
			a = [data.name,data.open_1,data.open_2, data.open_3, data.open_4, data.address, data.telephone]
			self.response.write('''	<div style= "background-color : #94ff93; clear: both;padding-top: 5px; margin-bottom:20px;margin-top: 10px;"> \
									<p class = "more_info" id = "open_close">Name: </p> \
									<p>%s</p> \
									<p class = "more_info" id = "open_close">Opened/Closed: OPENED </p> \
									<p class = "more_info" id = "open_close">Opening Hours: </p> \
									<p>
									%s<br> \
									%s<br> \
									%s \
									%s </p>\
									<p class = "more_info" id = "open_close">Address: </p> \
									<p>%s</p> \
									<p class = "more_info" id = "open_close">Telephone: </p> \
									<p>%s</p> \
									<br> \
									</div>''' % (a[0],a[1],a[2],a[3],a[4],a[5],a[6]))
									
		for data in c_data:
			a = [data.name,data.open_1,data.open_2, data.open_3, data.open_4, data.address, data.telephone]
			self.response.write('''	<div style= "background-color : #ffb3b4; clear: both; padding-top: 5px; margin-bottom:20px;margin-top: 10px;"> \
									<p class = "more_info" id = "open_close">Name: </p> \
									<p>%s</p> \
									<p class = "more_info" id = "open_close">Opened/Closed: CLOSED </p> \
									<p class = "more_info" id = "open_close">Opening Hours: </p> \
									<p>
									%s<br> \
									%s<br> \
									%s \
									%s </p>\
									<p class = "more_info" id = "open_close">Address: </p> \
									<p>%s</p> \
									<p class = "more_info" id = "open_close">Telephone: </p> \
									<p>%s</p> \
									<br> \
									</div>''' % (a[0],a[1],a[2],a[3],a[4],a[5],a[6]))
			

app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/about', About),
	('/health_tips', Health_tips),
	('/north', North),
	('/northeast', Northeast),
	('/east', East),
	('/central', Central),
	('/west', West),
	('/open_close', Open_close)
], debug=True)

# SAVE THE WORLD 2
# By: Yi Ting & Peirce :D