# Send Emails with google account

Send Emails with google account is a mini-lib which help you to generate and send emails message

Supported social profile
  - Generate Emails messages with one method
  - Send multiple message with one click
  - Import Many format (for exemple: csv-file)
 

### Installation

To user this lib, you must create 'MessageSender' object 

```python
from send_emails_gmail.send_message_by_gmail import MessageSender
```

In route
```python
@app.route('/')
def sender_create():
    sender = MessageSender(<user`s_email>, <google_oauth2_credential_object>)
    ...
```

You can also use my other repo to authorization:
[Fast_Social_Login_For_Flask](https://github.com/Maruda-Patryk/Fast_Social_Login_For_Flask)

With [Fast_Social_Login_For_Flask](https://github.com/Maruda-Patryk/Fast_Social_Login_For_Flask) you can easy auth sender:

```python
from google_login.login_with_google import OAuth
oauth = OAuth(app , 'web_client.json' , scopes='https://www.googleapis.com/auth/gmail.send')

@app.route('/')
@oauth.login_required
def sender_create_with_OAuth():
    sender = MessageSender(oauth.email, oauth.credentials)
    ...
```

After auth sender you can easy send emails:

### Send many different Emails messages with csv file or string in csv format:
    
from file:
```python
sender.from_csv_file('path_to_file.csv')
```
file format:
```csv
<email_to>,<title>,<body>
<email_to>,<title>,<body>
<email_to>,<title>,<body>
```

from csv format string:
```python
string_with_csv_format = '<email_to>,<title>,<body>\n
                            <email_to>,<title>,<body>'

sender.str_csv_format(string_with_csv_format)
```
In this case you can also customize your sepatator:
```python
string_with_csv_format = '<email_to>&&##<title>&&##<body>\n
                            <email_to>&&##<title>&&##<body>'
                            
sender.str_csv_format(string_with_csv_format , separator='&&##')
```

### Send the same email to many addresses

```python
list_of_emails_addresses = ('exemple@exemple.com','exemple@exemple.com','exemple@exemple.com','exemple@exemple.com')
title = 'This is a title of message'
body = 'here you got a massage body'

sender.send_message_to_many_emails(list_of_emails_addresses , title , body)
```

### Send only one email 

```python
email_to = 'exemple@exemple.com'
title = 'This is a title of message'
body = 'here you got a massage body'

sender.create_and_send_message(email_to , title , body)
```

### Required Libs

[Google's python lib](https://developers.google.com/api-client-library/python/)

```sh
$ pip install --upgrade google-api-python-client
```

### The Full Exemple 


```tree
|-exemple.py
|-web_client.json
|-send_emails_gmail
| |-send_message_by_gmail
|-google_login # You can find this in my other repo 
| |-login_with_google.py
|-templates
| |-index.html
```
My other google_login repo [Fast_Social_Login_For_Flask](https://github.com/Maruda-Patryk/Fast_Social_Login_For_Flask)

In exemple.py
```python
#!/usr/bin/env python 
# -*- coding: UTF-8 -*-

from flask import Flask , render_template , url_for
from flask_wtf import FlaskForm
from wtforms import StringField , SubmitField 
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired , Email
from wtforms.widgets import TextArea

from google_login.login_with_google import OAuth
from send_emails_gmail.send_message_by_gmail import MessageSender
import os
import json

app = Flask(__name__ , template_folder='templates')

app.secret_key = 'super_secret'

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
oauth = OAuth(app , 'web_client.json' , scopes='https://www.googleapis.com/auth/gmail.send')

    
class ManyEmailsAndMassages(FlaskForm):
    string_csv = StringField('string_csv' , widget=TextArea() , render_kw={"placeholder": "<email.exemple>,<title>,<body>\n<email.exemple>,<title>,<body>\n<email.exemple>,<title>,<body>"}, validators=[DataRequired()])
    submit = SubmitField('submit' , render_kw ={ "style":"margin-top:5px;" , "class":"form-control"})

class ManyEmails(FlaskForm):
    emails_list = StringField('emails_list', widget=TextArea() , render_kw={"placeholder": "<email_to>,<email_to>,<email_to>", "class":"form-control"}, validators=[DataRequired()])
    title = StringField('title' , render_kw={"placeholder": "<title>", "class":"form-control"}, validators=[DataRequired()])
    body = StringField('body' , render_kw={"placeholder": "<message_body>", "class":"form-control"}, validators=[DataRequired()])
    submit = SubmitField('submit' , render_kw ={ "style":"margin-top:5px;" , "class":"form-control"})

class OneEmail(FlaskForm):
    email_to = EmailField('email' ,render_kw={'placeholder':'<email>',"class":"form-control"} , validators=[DataRequired() , Email()])
    title = StringField('title' , render_kw={"placeholder": "<title>", "class":"form-control"}, validators=[DataRequired()])
    body = StringField('body' , render_kw={"placeholder": "<message_body>", "class":"form-control"}, validators=[DataRequired()])
    submit = SubmitField('submit' , render_kw ={ "style":"margin-top:5px;" , "class":"form-control"})

@app.route('/forms' , methods=['GET','POST'])
@oauth.login_required
def index():
    string_csv_form = ManyEmailsAndMassages(prefix='string_csv_form')
    emails_list_form = ManyEmails(prefix='emails_list_form')
    send_email_to_one = OneEmail(prefix='send_email_to_one')

    if string_csv_form.validate_on_submit() and string_csv_form.submit.data:
        sender = MessageSender(oauth.email, oauth.credentials)
        sender.str_csv_format(string_csv_form.string_csv.data)
        return 'Succes'

    if emails_list_form.validate_on_submit() and emails_list_form.submit.data:
        sender = MessageSender(oauth.email, oauth.credentials)
        sender.send_message_to_many_emails(emails_list_form.emails_list.data,emails_list_form.title.data,emails_list_form.body.data)
        return 'Succes'

    if send_email_to_one.validate_on_submit and send_email_to_one.submit.data:
        sender = MessageSender(oauth.email, oauth.credentials)
        args = (send_email_to_one.email_to.data, send_email_to_one.title.data , send_email_to_one.body.data)
        message = sender.create_and_send_message(*args)
        return str(message)

    return render_template('index.html' , string_csv_form=string_csv_form , emails_list_form=emails_list_form ,send_email_to_one=send_email_to_one)

@app.route('/logout')
@oauth.login_required
def delete():
    oauth.clear()
    return 'clear'


if __name__ == "__main__":
    app.run(port=8080 , debug=True)

```

How 'web_client.json' file should look (of course all keys should be fill with values)

```json
{"web":{"client_id":"","project_id":"","auth_uri":"","token_uri":"","auth_provider_x509_cert_url":"","client_secret":"","redirect_uris":[""]}}
```

in index.html:

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO"
        crossorigin="anonymous">
</head>

<body>
    <div class="container">
        <div class="row">
            <div class="col-12">
                <p>
                    Send Emails to many address , and crete title, body for each emails
                </p>
                <form method="POST" action="{{url_for('index')}}">
                    {{string_csv_form.hidden_tag()}}
                    {{string_csv_form.string_csv.label}} {{string_csv_form.string_csv( class='form-control')}}
                    {{string_csv_form.submit}}
                </form>
            </div>
        </div>
        <div class="row">
            <div class="col-12" style="background-color:black;height:2px;margin-top:55px;margin-bottom:55px;"></div>
        </div>
        <div class="row">
            <div class="col-12">
                <p>
                    Crete Emails list and then send same tiltle and body to each one
                </p>
                <form method="POST" action="{{url_for('index')}}">
                    {{emails_list_form.hidden_tag()}}
                    {{emails_list_form.emails_list.label}} {{emails_list_form.emails_list()}}
                    {{emails_list_form.title.label}} {{emails_list_form.title()}}
                    {{emails_list_form.body.label}} {{emails_list_form.body()}}
                    {{emails_list_form.submit}}
                </form>
            </div>
        </div>
        <div class="row">
            <div class="col-12" style="background-color:black;height:2px;margin-top:55px;margin-bottom:55px;"></div>
        </div>
        <div class="row">
            <div class="col-12">
                <p>
                    Crete and Send Email to only one address</p>
                <form method="POST" action="{{url_for('index')}}">
                    {{send_email_to_one.hidden_tag()}}
                    {{send_email_to_one.email_to.label}} {{send_email_to_one.email_to()}}
                    {{send_email_to_one.title.label}} {{send_email_to_one.title()}}
                    {{send_email_to_one.body.label}} {{send_email_to_one.body()}}
                    {{send_email_to_one.submit}}
                </form>
            </div>
        </div>
    </div>
</body>
</html>
```


