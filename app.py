from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql
import requests
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/weatherapi_data'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Database configuration
db_config = {
    'host': 'localhost',
    'database': 'weatherapi_data',
    'user': 'root',
    'password': 'password'
}

# to create a database connection
def create_connection():
    connection = None
    try:
        connection = pymysql.connect(**db_config)
        # print("Connected to MySQL database")
        return connection
    except pymysql.Error as e:
        print(f"Error while connecting to MySQL database: {e}")
    return connection


@app.route('/', methods=['GET'])
def index():
    # return "render_template('index.html')"
    return render_template('index.html')


# to check the database connection
@app.route('/check_db_connection', methods=['GET'])
def check_db_connection():
    try:
        connection = create_connection()
        if connection is None:
            return jsonify(status="Error", message="Failed to connect to the database")

        connected_database = db_config['database']  # Retrieve the database name from the db_config dictionary
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        table_names = [table[0] for table in cursor.fetchall()] #LIST COMPRENSION TO DISPLAY THE TABLES IN THAT DATABASE
        cursor.close()
        connection.close()
        return jsonify(status="Connected", database=connected_database, tables=table_names)
    except pymysql.Error as e:
        return jsonify(status="Error", message=str(e))

@app.route('/weather_data', methods=['POST'])
def weather_detials():
    try:
        # api key from openweathermap website
        api_key = "150edd73ba28de68a18817e4d62dbbfa"
        # if api_key is invalid it will be handled(show error automatically)
        # error msg{"cod": 401,"message": "Invalid API key. Please see https://openweathermap.org/faq#error401 for more info."}
        data = request.json
        city = data.get('city')
        if not city:
            return jsonify({'error': 'City not provided.'}), 400
        weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}")
        weather = weather_data.json()
        return jsonify(weather), 200
    except Exception as e:
        return jsonify(status="Error", message=str(e))


class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)



if __name__ == '__main__':
    app.run(debug=True)