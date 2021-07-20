from flask import Flask , render_template , request , session , redirect , flash , url_for
import os
#####################################################################################     SQLALCHEMY IMPORTS    ###########
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import exc
import json
#####################################################################################     MAIL IMPORTS    #################
from flask_mail import Mail
from datetime import datetime
from flask_mail import Mail
#########################################################################            LOGIN MODULES IMPORT        ######
import secrets
#from PIL import Image

from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user , current_user , logout_user , login_required

#########################################################################            WTF FORMS   IMPORT        ######
from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from wtforms import StringField , PasswordField , SubmitField , BooleanField
from wtforms.validators import DataRequired , Length , Email , EqualTo , ValidationError

#from flask_bcrypt import Bcrypt


#!*!*!*!!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!**!*!*!!!*!*!*!*!*!*---------------  IMPORTS  -------------!*!*!*!*!*!*!*!*!*!**!*!*!!*!*!* 





app = Flask(__name__)
app.secret_key = 'super secret'

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465' ,
    MAIL_USE_SSL = True ,
    MAIL_USERNAME = "repairmemain@gmail.com",
    MAIL_PASSWORD = "100billion$"
)
mail = Mail(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/repairme"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


##################################################################################################        CLASS START *  
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80) ,nullable=False )
    email = db.Column(db.String(120), nullable=False)
    phone_num = db.Column(db.String(120),  nullable=False)
    subject = db.Column(db.String(120), nullable=True)
    msg = db.Column(db.String(120),nullable=False  )
    date = db.Column(db.String(80),nullable=True )

class Services(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80) ,nullable=False )
    description = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120),  nullable=False)
    icon = db.Column(db.String(120), nullable=True)
    color = db.Column(db.String(120),nullable=False  )
    date = db.Column(db.String(80),nullable=True )
    
class Bookservices(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80) ,nullable=False )
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120),  nullable=False)
    service = db.Column(db.String(120),  nullable=False)
    category = db.Column(db.String(120),  nullable=True)
    status = db.Column(db.String(120),  nullable=True)
    serviceman = db.Column(db.String(120), nullable=True)
    area = db.Column(db.String(120),nullable=False  )
    location = db.Column(db.String(80), nullable=False)
    service_date = db.Column(db.String(120), nullable=False)
    service_time = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(80),nullable=True )

class Category_homeapp(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    instruments = db.Column(db.String(80) ,nullable=False )
    position = db.Column(db.String(80) ,nullable=False )

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80) , unique=False ,nullable=False )
    phone = db.Column(db.String(80) ,nullable=False )
    email = db.Column(db.String(120),unique=True , nullable=False)
    img = db.Column(db.String(120),nullable=False , default='default.jpg ')
    password = db.Column(db.String(120), nullable=False)

class Servicemen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80)  ,nullable=False )
    description = db.Column(db.String(80)  ,nullable=False )
    status = db.Column(db.String(80),nullable=True )
    phone = db.Column(db.String(80) ,nullable=True )
    address = db.Column(db.String(80),nullable=False)
    image = db.Column(db.String(80),nullable=False , default='default_serviceman.jpg')
    adhar_no = db.Column(db.String(120),unique=True , nullable=False)
    adhar_img = db.Column(db.String(120),nullable=True , default='default_adhar.jpg ')
    
#!*!*!*!!*!*!*!*!*!*!*!*!!*!*!*!!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!**!*!*!*!*!*!*       CLASS  CLOSE !   

###################################################################################################       FORMS START  *    

class RegistrationForm(FlaskForm):
    #name = StringField('Name' , validators=[DataRequired(), Length(min=7 , max=20)]) 
    name = StringField('Name' , validators=[DataRequired(), Length(min=7 , max=20)])   
    phone = StringField('phone Number' , validators=[DataRequired(), Length(min=10 , max=13)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired() , EqualTo('password')])
    submit = SubmitField('Sign up')

    """
    def validate_name(self,name):
        user = User.query.filter_by(name=name.data).first()
        
        if user:
            raise ValidationError('That username is already taken. Please choose a different one')

    """
                    
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
         
        if user:
            raise ValidationError('Thid email is already exist . Please choose a different one or log in . ')

    def validate_phone(self,phone):
        user = User.query.filter_by(phone=phone.data).first()
         
        if user:
            raise ValidationError('Thid Number is already exist . Please choose a different one')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Login')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
         
        if user is None:
            raise ValidationError('This email does not exist. Please register first')

    def validate_password(self,password):
        user = User.query.filter_by(password=password.data).first()
         
        if user is None:
            raise ValidationError('Password is incorrect')

class UpdateProfileForm(FlaskForm):
    name = StringField('name' , validators=[DataRequired(), Length(min=3 , max=15)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg','png'])])
    
    submit = SubmitField('Update')

    def validate_name(self,name):
        if name.data != current_user.name:
            user = User.query.filter_by(name=name.data).first()
            if user:
                raise ValidationError('That username is already taken. Please choose a different one')


    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Thid email is already exist . Please choose a different one')


class UpdateStatusForm(FlaskForm):
    status = StringField('Status' , validators=[DataRequired()])

#!!*!*!*!*!*!*!*!*!!*!*!*!!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!***!*!*!!!*!*!*!*     FORMS CLOSE !    

@login_manager.user_loader        ##################################################################     USER LOADER             
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')        #############################################################################     HOME              
def home():
    services = Services.query.filter_by().all()
    bookservices = Bookservices.query.all()
    lenght_b = 3*len(bookservices)
    lenght_s = 3*len(services)

    return render_template('index.html' , services = services,bookservices=bookservices,lenght_b=lenght_b,
                           lenght_s=lenght_s)

@app.route('/signup', methods=['GET','POST'])        ###############################################     SIGN UP   
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data , phone=form.phone.data ,email=form.email.data ,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data}! Please Log In ' , 'success')

        mail.send_message( "Welcome to Repair Me",  
                          sender=form.email.data,
                          recipients=[form.email.data],
                          html="<h1>Thanks for sign Up  </h1>" 
                                
                                "<div style='background-color: black;color: chartreuse;'> <h1>Welcome to Repair Me</h1></div>"


                                
                                "<p>thduhfhf </P>"
                                "<img src='https://unsplash.com/photos/yO12O8j3JK0'>"
                          )
        

        
        mail.send_message("New Sign Up  " + form.name.data,
                          sender=form.email.data,
                          recipients=["repairmemain@gmail.com"],
                          body=form.email.data+"\n"+"\nPhone number :" + form.phone.data
                          ) 
        
        
        
        
        
        
        return redirect(url_for('login'))
    
    
    
    
    return render_template('signup.html',form=form)

@app.route('/login', methods=['GET','POST'])        ################################################     USER LOG IN          
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data , password=form.password.data).first()
        if user :
            login_user(user , remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You are successfully Logged In ' , 'primary')
            return redirect(next_page) if next_page else  redirect(url_for('account'))

        else :
            flash('login unsuccessful. Please check email and password' , 'danger')

    return render_template('user_login.html',form=form)

@app.route('/userlogout' )        ##################################################################     Logout  
def userlogout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')        ######################################################################     ACCOUNT   
def account():

    """
    form =  UpdateProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img = picture_file

        current_user.name = form.name.data
        current_user.email = form.email.data 
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    """
    bookservices = Bookservices.query.order_by(Bookservices.date.desc()).filter_by(email=current_user.email)
    
    book_1 = Bookservices.query.filter_by(email=current_user.email).all()
    len_book = len(book_1)
    
    

    


    image_file = url_for('static',filename='assets/img/profile_pics/'+ current_user.img)
    return render_template("account.html" , image_file = image_file ,bookservices=bookservices,len_book =len_book   )
    
@app.route('/service/<string:service_slug>' , methods=['GET' , 'POST'])        #####################     BOOK SERVICES     
@login_required
def bookservice(service_slug):
    if current_user.is_authenticated:
        service = Services.query.filter_by(slug=service_slug).first()
        homeapps = Category_homeapp.query.all()
        
        if (request.method == 'POST'):
            name = request.form.get('name')
            #email = request.form.get('email')
            email = current_user.email
            phone = request.form.get('phone')
            service = service.title           
            category = request.form.get('category',default=("None")) 
            status =  request.form.get('status',default=("Pending")) 
            serviceman =  request.form.get('serviceman',default=("Not yet alloted"))     
            area = request.form.get('area')
            location = request.form.get('location')
            service_date = request.form.get('service_date')
            service_time = request.form.get('service_time')
            

            entry = Bookservices(name=name, email=email ,  phone=phone,  area=area , service=service ,category=category, 
                                status=status,serviceman=serviceman,location=location ,service_date=service_date , service_time=service_time  ,
                                 date =datetime.now())
            db.session.add(entry)
            db.session.commit()


            mail.send_message("Thanks for booking " + current_user.name,
                          sender=email,
                          recipients=[current_user.email],
                          body=email+"\n"+"\nPhone number :" + phone 
                          )

            

                 
            mail.send_message("New Service request from " + name,
                          sender=email,
                          recipients=["contact@repairmeshop.in"],
                          body=email  + "\nPhone Number : " + phone +  "\nService : "+ service +
                          "\nCategory  : "+ category + "\nArea : " + area + "\nLocation : " + location + 
                          "\nService date : " + service_date  +"\nService Time  : " + service_time 
                          )
            return redirect(url_for('account'))              
            

        return render_template('bookservices.html',  service=service ,homeapps=homeapps)

@app.route('/editbookservice/<string:sno>' , methods=['GET' , 'POST'])        ######################     EDIT BOOK SERVICES    
def editbookservice(sno):
    if ('user' in session and session['user'] == "rex"):

        if request.method == 'POST':
            status = request.form.get('status') 
            serviceman = request.form.get('serviceman')         
            bookservice = Bookservices.query.filter_by(sno=sno).first()
            bookservice.status = status
            bookservice.serviceman = serviceman
            db.session.commit()
            return redirect(url_for('dashboard'))
        
        bookservice = Bookservices.query.filter_by(sno=sno).first()
        return render_template('editbookservice.html', bookservice= bookservice )
  
@app.route('/editservice/<string:sno>' , methods=['GET' , 'POST'])        ##########################     EDIT SERVICES    
def editservice(sno):
    if ('user' in session and session['user'] == "rex"):

        if request.method == 'POST':

            title = request.form.get('title')
            slug = request.form.get('slug')
            icon = request.form.get('icon')
            color = request.form.get('color')
            description = request.form.get('description')
            date = datetime.now()
            


            if sno=='0':
                service = Services( sno=sno , title=title , description=description , slug=slug , icon=icon , 
                color = color , date=date )
                db.session.add(service)
                db.session.commit()
                return redirect(url_for('dashboard'))


            else:
                service = Services.query.filter_by(sno=sno).first()
                service.title = title
                service.description = description
                service.slug = slug
                service.icon = icon
                service.color = color
                service.date = date
                 



                db.session.commit()
                return redirect(url_for('dashboard'))

        service = Services.query.filter_by(sno=sno).first()
        return render_template('editservice.html',  service=service, sno=sno)

@app.route('/editserviceman/<string:id>' , methods=['GET' , 'POST'])        ########################     EDIT SERVICES MAN    
def editserviceman(id):
    if ('user' in session and session['user'] == "rex"):

        if request.method == 'POST':

            name = request.form.get('name')
            description = request.form.get('description')
            status = request.form.get('status')
            phone = request.form.get('phone')
            address = request.form.get('address')
            adhar_no = request.form.get('adhar_no')

            if id=='0':
                serviceman = Servicemen( id=id, name=name , description=description , status=status , phone=phone ,
                                     address=address , adhar_no=adhar_no )
                db.session.add(serviceman)
                db.session.commit()
                return redirect(url_for('dashboard'))

            else:
                serviceman = Servicemen.query.filter_by(id=id).first()
                serviceman.name = name
                serviceman.description = description
                serviceman.status = status
                serviceman.phone = phone
                serviceman.address = address
                serviceman.adhar_no = adhar_no

                db.session.commit()
                return redirect(url_for('dashboard'))
        
        serviceman = Servicemen.query.filter_by(id=id).first()
        return render_template('editservicemen.html', serviceman=serviceman,id=id)

@app.route('/about')        ########################################################################     ABOUT    
def about():
    services = Services.query.filter_by().all()
    return render_template('about.html',  services=services )

@app.route('/team')        #########################################################################     TEAM  
def team():
    return render_template('team.html')

@app.route('/dashboard' ,  methods=['GET' , 'POST'] )        #######################################     DASHBOARD 
def dashboard():
    if ('user' in session and session['user'] == "rex"):
        services = Services.query.all()
        contacts = Contacts.query.order_by(Contacts.date.desc()).all()
        bookservices = Bookservices.query.order_by(Bookservices.date.desc()).all()
        homeapps = Category_homeapp.query.all()
        servicemen = Servicemen.query.all()

        

        return render_template('dashboard.html',  services=services , contacts=contacts , 
                                bookservices=bookservices , homeapps=homeapps ,servicemen=servicemen)

    if request.method == 'POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if (username == "rex" and userpass == "rex5467"):
            session['user'] = username
            services = Services.query.all()
            contacts = Contacts.query.all()
                                        
            return render_template('dashboard.html',  services=services , contacts=contacts)

    return render_template('login.html')

@app.route('/logout')        #######################################################################     LOGOUT
def logout():
    session.pop('user')
    return redirect('/dashboard')

@app.route('/delete/<string:sno>' , methods = ['GET' , 'POST'])        #############################     DELETE  SERVICE 
def delete(sno):
    if ('user' in session and session['user'] == "rex"):
        service = Services.query.filter_by(sno=sno).first()
        db.session.delete(service)
        db.session.commit()
    return redirect('/dashboard')

@app.route('/portfolio')        ####################################################################     PORTFOLIO
def portfolio():
    return render_template('portfolio.html')

@app.route('/contact', methods = ['GET','POST'])        ############################################     CONTACT 
def contact():
    if (request.method == 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num=phone, msg=message, date=datetime.now(), email=email , subject=subject)
        db.session.add(entry)
        db.session.commit()

        
        mail.send_message("Thanks " + name,
                          sender=email,
                          recipients=[email],
                          body=email+"\n"+"\nPhone number :" + phone +"\n\nSubject:  "+ subject + "\n\n" +message 
                          )
        


        mail.send_message("New Contact Request from " + name,
                          sender=email,
                          recipients=["repairmemain@gmail.com"],
                          body=email+"\n"+"\nPhone number :" + phone +"\n\nSubject:  "+ subject + "\n\n" +message 
                          )
        return render_template('index.html')
        
        
    
    
    
    
    
    
    return render_template('contact.html')


