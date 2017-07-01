from flask import Flask
from flask_restful import Resource, Api,reqparse
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER']='hare1039'
app.config['MYSQL_DATABASE_PASSWORD'] = 'hare1039'
app.config['MYSQL_DATABASE_DB'] = 'ItemlistDb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

api = Api(app)
class CreateUser(Resource):
	def post(self):
		try:
			parser = reqparse.RequestParser()
			parser.add_argument('email',type=str,help='Email address to createuser')
			parser.add_argument('password',type=str, help='Password to create user')
			args = parser.parse_args()
			__userEmail =args['email']
			__userPassword = args['password']

			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('spCreateUser',(__userEmail,__userPassword))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				return {'StatusCode':'200','Message':'User creation success'}
			else:
				return {'StatusCode':'1000','Message':str(data[0])}
		except Exception as e:
			return {'error':str(e)}
api.add_resource(CreateUser,'/CreateUser')

if __name__=='__main__':
	app.run(host='172.17.0.5',debug=True)
