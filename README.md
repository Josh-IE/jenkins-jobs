# jenkins-jobs
A Python script that uses the Jenkins API library to get a list of jobs and their status from a given jenkins instance.  The status for each job is stored in an sqlite database along with the time for when it was checked.

# status meanings
  SUCCESS: is returned if the last build on the job was succesfull
  FAILURE : is returnd if the last build on the job failed
  NOTBUILT : is returnd if no build has been run on the job
  RUNNING : is returned if the job is currently running its build
  
# Dependencies
This script relies on the JenkinsAPI, sqlite3 and datetime libraries/modules

# Install JenkinsAPI library
use pip or setuptools to automatically install  JenkinsAPI

pip install jenkinsapi
        or
easy_install jenkinsapi
  * In Jenkins > 1.518 you will need to disable "Prevent Cross Site Request Forgery exploits".
  * Remember to set the Jenkins Location in general settings - Jenkins' REST web-interface will not work if this is set incorrectly.
  
# Database 
db_name defines the database path
db_name = 'jenkins.db'

#Database connection is initiated 
conn = sqlite3.connect(db_name)
c = conn.cursor()

# usage
If running on a PC, pull the repository into a folder on your platform. 
Run the command 'python script.py' in a command line shell from the projects folder to execute the script named script.py. 
On execution, a dictionary (dict{}) of jobs and their status from the defined jenkins instance is created, and the status for each job is stored in the defined sqlite database along with it was checked.


#A table named 'jenkins' with fields (job_name, status, date_checked) is created
#Below is the sql statement used
c.execute('create table jenkins ( id INTEGER PRIMARY KEY, job_name NOT NULL, status NOT NULL, date_checked TEXT )')


# script config variables
jenkins_url = 'http://172.82.162.36:8080' (sets the location of the jenkins instance)
username='simplepay' (sets the username of the jenkins instance account)
password='payadmin10' (sets the password of the jenkins instance account)

NB
I installed a jenkins instance on my server at http://172.82.162.36:8080. Feel free to use my account. My username:password is simplepay:payadmin10 . (I'm aware of the security implications of sharing my credntials on a public repository)

#A dictionary dict{} is created to store the list of jobs(as key ) and their status(as value) from the jenkins instance.
dict={}

# Assumptions
  The Database table will have unique entries for the job name field. Thus
    Whenever the script is run, if the database jenkins table already has the job status stored from a previous insertion command, then     the job record is updated. Else, a new record is created(INSERT) in the jenkins table to store the job status. 

