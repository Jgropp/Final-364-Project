from flask import Flask, request, render_template, make_response, redirect, url_for, flash
from flask import Flask, render_template
from flask_wtf import Form 
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from wtforms.validators import DataRequired, Email,Length
import sqlite3
from flask_table import Table, Col
import requests




app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'

APIKEY="iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv"

class LoginForm(Form):
        username = StringField('username', validators=[DataRequired(), Email(), Length(max=20)])
        password = PasswordField('password', validators=[InputRequired(),Length(min=4, max=16)])

class SignupForm(Form):
        username = StringField('username', validators=[DataRequired(), Email(), Length(max=20)])
        password = PasswordField('password', validators=[InputRequired(),Length(min=4, max=16)])


class ItemTable(Table):
    
    year = Col('year')
    Population = Col('population')
    violentCrimes=Col('violentCrimes')
    homicide=Col('Homicide')
    robbery=Col('robbery')

    
class Item(object):
        def __init__(self, year,Population,violentCrimes,homicide,robbery):
                self.Population = Population
                self.year = year
                self.violentCrimes=violentCrimes
                self.homicide=homicide
                self.robbery=robbery
                



@app.route('/', methods=['GET', 'POST'])
def Login():

        loginform = LoginForm()
        if loginform.validate_on_submit():
                Username=loginform.username.data;
                Password=loginform.password.data;

                usernameDatabase = sqlite3.connect('data/usernames')
                cursor = usernameDatabase.cursor()
                cursor.execute('''SELECT id,Username FROM username WHERE Username=?''', (Username,))
                user1 = cursor.fetchone() #retrieve the first row
                if(user1 is not None):
                                passwordDatabase = sqlite3.connect('data/password')
                                cursor = passwordDatabase.cursor()
                                cursor.execute('''SELECT id,Password FROM passwords WHERE Password=?''', (Password,))
                                user1 = cursor.fetchone() #retrieve the first row
                                if(user1 is not None):
                                        return redirect(url_for('Cookie'))  

                        




                

                
                
                        
                        
                       
        return render_template('index.html', loginform=loginform)



@app.route('/signup', methods=['GET', 'POST'])
def Signup():
        
        form = SignupForm()
        if form.validate_on_submit():
                


                usernameDatabase = sqlite3.connect('data/usernames')
                
                
                cursor = usernameDatabase.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS username(id INTEGER PRIMARY KEY, Username TEXT)''')

                
                usernameDatabase.commit()
                cursor = usernameDatabase.cursor()

                
                usernamez=form.username.data;

                cursor.execute('''INSERT INTO username(Username) VALUES(?)''', (usernamez,))
                print('Second user inserted')
 
                usernameDatabase.commit()


                ################
                passwordDatabase=sqlite3.connect('data/password');
                cursor = passwordDatabase.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS passwords(id INTEGER PRIMARY KEY, Password TEXT)''')

                
                passwordDatabase.commit()
                cursor = passwordDatabase.cursor()

                
                passwords=form.password.data;

                cursor.execute('''INSERT INTO passwords(Password) VALUES(?)''', (passwords,))
                print('Second user inserted')
 
                passwordDatabase.commit()
                
                              
        return render_template('signup.html', form=form)
       




@app.route('/Login', methods=['GET', 'POST'])
def Cookie():
        printed = make_response('<h1 style="color:blue;padding-left: 430px;">  Welcome to Course:SI 364 </h1> </br></br>  <h1 style="padding-left: 400px;border-style: solid;"> Michigan: Crime Information </h1> <br> <br> <br> <br> <div style="color:#0000FF;padding-left: 475px;"><a href = "/national" style="border-style: solid;padding:10px;">Crime Report for State Of Michigan</a> </br>     </br> <br>  <br><a href = "/Images" style="border-style: solid;padding:10px;margin-top:10sp;margin-left:70px"> View Images </a>   </br>  </div>   ')
        printed.set_cookie('Crime', 'Project')
        return printed







@app.route('/national', methods=['GET', 'POST'])
def Players():
        Key="iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv";
        URL="https://api.usa.gov/crime/fbi/ucr/estimates/states/MI?page=1&per_page=10&output=json&api_key="+Key;
   
        print(URL)
        response = requests.get(URL)
        data=response.json()

        items=[]

        i=0
        while(i<9):
                year=(((data["results"])[i])['year'])
                population=(((data["results"])[i])['population'])
                violent_crime=(((data["results"])[i])['violent_crime'])
                homicide=(((data["results"])[i])['homicide'])
                robbery=(((data["results"])[i])['robbery'])
                items.append(Item(year,population,violent_crime,homicide,robbery))
                i=i+1


        table = ItemTable(items)
        table.border=True;


        print(table.__html__())
        printed = make_response('<br><br><br><br><br><br><br><br><br><br> <div style="color:#0000FF;padding-left: 600px;">'+table.__html__()+'</div>')
        return printed;
        





@app.route('/Images')
def insert_image():
        return render_template ("image.html")


@app.errorhandler(404)
def Error(e):
        return render_template("Error1.html")

@app.errorhandler(408)
def Error1(e):
        return render_template("Error1.html")



if __name__ == '__main__':
        app.run(debug=True)
