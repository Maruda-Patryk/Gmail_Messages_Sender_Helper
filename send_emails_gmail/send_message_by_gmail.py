#!/usr/bin/env python 
# -*- coding: UTF-8 -*-
from email.mime.text import MIMEText
import base64
from apiclient import errors
from googleapiclient.discovery import build

class MessageSender(object):
    def __init__(self , email , credentials):
        self.email = email
        self.credentials = credentials
        self.service = build('gmail', 'v1', credentials=credentials)

    def send_message(self , message):
        """Send an email message.

        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

        Returns:
        Sent Message.
        """
        
        try:
            message = message['raw'].decode("utf-8")
            message = (self.service.users().messages().send(userId=self.email, body={'raw':message})
                    .execute())
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' %error)
            return {'status':{'error':error}}

    @classmethod
    def massive_sender_csv(cls, messages_csv_format ,  sender=None):
        import csv
        csv_lines = csv.reader(messages_csv_format , delimiter=',')
        for i, line in enumerate(csv_lines):
            print('Lines[{}]: {}'.format(i , line))
    
    def create_and_send_message(self , to, subject, message_text , sender=None):
        if sender == None:
            sender = self.email
        args = (sender, to, subject, message_text)
        return self.send_message(self.create_message(*args))

    def str_csv_format(self ,messages_csv_format , sender=None , separator = None):
        if separator == None:
            separator = ','
        message_array = messages_csv_format.split('\n')
        for message in message_array:
            arguments = message.split(separator)
            args = (self.email ,arguments[0] , arguments[1] , arguments[2] )
            message = self.create_message(*args)
            self.send_message(message)

    def send_message_to_many_emails(self , emails_array , title , body):
        try:
            emails_array = emails_array.split(',')
            for email in emails_array:
                self.send_message(self.create_message(self.email , email , title , body))
            return {'status':'Succes'}
        except Exception as e:
            return {'status':{'error':str(e)}}
            
    def create_message(self , sender, to, subject, message_text):
        """Create a message for an email.

        Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

        Returns:
        An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes())}