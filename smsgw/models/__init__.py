# -*- coding: utf-8 -*-
# http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

from smsgw.extensions import db
from datetime import datetime
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.declarative import AbstractConcreteBase


class BaseModel(AbstractConcreteBase, db.Model):
    
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}

    createdAt = db.Column(db.TIMESTAMP, default=datetime.utcnow, 
                          server_default=text('CURRENT_TIMESTAMP'))
    updatedAt = db.Column(db.TIMESTAMP, default=datetime.utcnow, 
                          onupdate=datetime.utcnow)

    def to_dict(self, properties):
        return {key: getattr(self, key) for key in properties}

    def update(self, data):
        for key in data:
            if hasattr(self, key):
                setattr(self, key, data[key])

    @classmethod
    def get_or_create(cls, _latest=True, **kwargs):
        """
        Get or create row in DB
        """
        instance = cls.query.filter_by(**kwargs).first()
        if instance is None:
            instance = cls(**kwargs)
            db.session.add(instance)
        return instance


# list of models
from smsgw.models.user import User
from smsgw.models.user_token import UserToken
from smsgw.models.template import Template
from smsgw.models.tag import Tag
from smsgw.models.contact import Contact
from smsgw.models.relations import contactTags