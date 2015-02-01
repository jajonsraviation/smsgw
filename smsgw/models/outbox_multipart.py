# -*- coding: utf-8 -*-
# http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.schema import Index
from smsgw.extensions import db
from smsgw.models import BaseModel


class OutboxMultipart(BaseModel):
    """ Outbox multipart model """

    __tablename__ = "outbox_multipart"

    id = db.Column(mysql.INTEGER(10, unsigned=True), primary_key=True)
    sequencePosition = db.Column(mysql.INTEGER(11), primary_key=True)

    coding = db.Column(db.Enum('Default_No_Compression','Unicode_No_Compression',
                               '8bit','Default_Compression','Unicode_Compression'), 
                        server_default='Default_No_Compression', nullable=False)
    text = db.Column(mysql.TEXT)
    textEncoded = db.Column(mysql.TEXT)
    udh = db.Column(mysql.TEXT)
    klass = db.Column('class', mysql.INTEGER, server_default='-1')