#/usr/bin/env python2.7
"""
Columbia W4111 Intro to databases
By Jeremy Staub JBS2208
Sources: course server code,flask.pocoo.org,jinja.pocoo.org
"""
import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
DATABASEURI = "postgresql://jbs2208:r39w8@104.196.175.120/postgres"
engine = create_engine(DATABASEURI)
@app.before_request
def before_request():
  try:
     g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None
@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass
@app.route('/')
def index():
  # DEBUG: this is debugging code to see what request looks like
  print request.args
  # List all people in the database
  cursor = g.conn.execute("SELECT name FROM person")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()
  context = dict(data = names)
  return render_template("index.html", **context)
#billsearch
@app.route('/billsearch', methods=['POST'])
def search():
   userinput = request.form['userinput']
   #if(len(userinput)>2):
    #  @app.route('/bad')
   bills = []
   print userinput
   cursor1 = g.conn.execute('select * from bill where bill_id= any (select bill_id from supports where committee_name = any (Select committee_name from member where politician_id = (Select politician_id from politician where person_id = (Select person_id from person where name = ' + '\'' + str(userinput) +  '\''  +  '))))');
   for result1 in cursor1:
      bills.append("Bill ID:")
      bills.append(result1['bill_id'])
      bills.append("Bill Name:")
      bills.append(result1['name'])
      bills.append("Date Initialized:")
      bills.append(result1['date_init'])
      bills.append("Results Yes:")
      bills.append(result1['results_yes'])
      bills.append("Results No:")
      bills.append(result1['results_no'])
      bills.append("Subject:")
      bills.append(result1['subject'])
      cursor1.close()
      context2 = dict(billdata=bills)
   return render_template("billsearch.html",**context2)
#RepSearch
@app.route('/repsearch', methods=['POST'])
def repsearch():
  stateinput = request.form['state']
  reps = []
  cursor2 = g.conn.execute('Select name from person join politician on politician.person_id = person.person_id where state =' '\'' + str(stateinput) + '\'' );
  for results in cursor2:
     reps.append(results['name'])
  cursor2.close()
  context3 = dict(repdata = reps)
  return render_template("repsearch.html", **context3)
#Gensearch
@app.route('/gensearch',methods=['POST'])
def gensearch():
   inputgen = request.form['gen']
   inputsencon = request.form['consen']
   print inputgen
   committees = []
   cursor3 = g.conn.execute('select distinct committee_name from member where politician_id = any (select politician_id from ' + str(inputsencon) + ' where politician_id = any (select politician_id from politician where gender = ' '\'' + str(inputgen) + '\'' '))');
   for result in cursor3:
      committees.append(result['committee_name'])
   #entries3 = [dict(Name = row[0]) for row in cursor3.fetchall()]
   context4 = dict(gendata = committees)
   return render_template("gensearch.html", **context4)
#TopicStateSearch
@app.route('/topicsearch',methods=['POST'])
def topicsearch():
   inputtopic = request.form['topic']
   print inputtopic
   states = []
   cursor4 = g.conn.execute('select distinct state from politician where politician_id = any (Select politician_id from member where committee_name = any (Select committee_name from supports where bill_id = any (Select bill_id from bill where subject = ' '\'' + str(inputtopic) + '\''' )))');
   for result in cursor4:
     states.append(result['state'])
   context5 = dict(statedata = states)
   return render_template("topicsearch.html",**context5)
@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()
if __name__ == "__main__":
  import click
  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)
  run()
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
~                      
