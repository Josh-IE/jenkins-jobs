from jenkinsapi.jenkins import Jenkins
import sqlite3
from datetime import datetime

### define Jenkins parameters  #####
jenkins_url = 'http://172.82.162.36:8080'
username='simplepay'
password='payadmin10'

### define Database details  #####
db_name = 'jenkins.db' ## sqlite database path

### get server instance  #####
def server_instance(jenkins_url, username, password):
	server = Jenkins(jenkins_url, username, password)
	return server
	
### connect to database  #####
def connectdb(db_name):
	conn = sqlite3.connect(db_name)
	return conn
	
### create table  ###
def create_table(db_name):
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.execute('create table IF NOT EXISTS jenkins ( id INTEGER PRIMARY KEY, job_name NOT NULL, status NOT NULL, date_checked TEXT )')
	conn.commit()
	conn.close()

def get_job_status(server, db_name):
	### create dictionary that holds the jobs name as keys and status as values ###
	dict={}
	for job_name, job_instance in server.get_jobs():
		if job_instance.is_running():
			status = 'RUNNING'
		elif job_instance.get_last_build_or_none() == None :
			status = 'NOTBUILT'
		else:
			simple_job = server.get_job(job_instance.name)
			simple_build = simple_job.get_last_build()
			status = simple_build.get_status()
		i = datetime.now()
		checked_time = i.strftime('%Y/%m/%d %H:%M:%S')
		tuple1 = (job_instance.name, status, checked_time)
		conn = connectdb(db_name)
		c = conn.cursor()
		c.execute("SELECT id FROM jenkins WHERE job_name = ?", (job_instance.name,))
		data=c.fetchone()
		if data is None:
			c.execute('INSERT INTO jenkins (job_name, status, date_checked) VALUES (?,?,?)', tuple1)
		else:
			tuple2 = (status, checked_time, job_instance.name)
			c.execute('UPDATE jenkins SET status=?, date_checked=? WHERE job_name=?', tuple2)
		### Add to dictionary ###
		dict[job_instance.name] = status
	# Save (commit) the changes
	conn.commit()
	# We can close the connection 
	conn.close()
	return dict
	
create_table()
server = server_instance(jenkins_url, username, password)
get_job_status(server, db_name)

