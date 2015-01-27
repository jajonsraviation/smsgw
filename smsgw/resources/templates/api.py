# -*- coding: utf-8 -*-
# http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

from flask import request, current_app
from flask.ext.classy import FlaskView, route

from smsgw.models import Template
from smsgw.lib.utils import response
from smsgw.resources import decorators
from smsgw.resources.templates.schemas import post, put
from smsgw.resources.error.api import ErrorResource
from smsgw.extensions import db


class TemplatesResource(FlaskView):
    """ Templates endpoints """

    route_base = '/users/<uuid:user_uuid>/templates/'

    @decorators.auth()
    def index(self, **kwargs):
        """
        Getting list of user's templates
        """
        user = kwargs.get('user')
        payload = []
        for template in user.templates:
            payload.append({
                'uuid': template.uuid,
                'label': template.label,
                'text': template.text,
                'createdAt': template.createdAt.isoformat(sep=' ')
            })

        return response(payload)

    @route('/<uuid:template_uuid>/')
    @decorators.auth()
    def get(self, **kwargs):
        """
        Get user template
        """
        template = kwargs.get('template')
        return response({
            'uuid': template.uuid,
            'label': template.label,
            'text': template.text,
            'createdAt': template.createdAt.isoformat(sep=' ')
        })

    @decorators.auth()
    @decorators.jsonschema_validate(payload=post.schema)
    def post(self, **kwargs):
        """
        Creating new user template
        """
        user = kwargs.get('user')

        # create and save template
        template = Template(**request.json)
        template.userId = user.id
        db.session.add(template)
        db.session.commit()

        # create payload
        payload = {
            'uuid': template.uuid,
            'label': template.label,
            'text': template.text,
            'createdAt': template.createdAt.isoformat(sep=' ')
        }
        return response(payload, status_code=201)

    @route('/<uuid:template_uuid>/', methods=['PUT'])
    @decorators.auth()
    @decorators.jsonschema_validate(payload=put.schema)
    def put(self, **kwargs):
        """
        Updateing existing template
        """
        template = kwargs.get('template')
        template.update(request.json)
        db.session.commit()
 
        return response({
            'uuid': template.uuid,
            'label': template.label,
            'text': template.text,
            'createdAt': template.createdAt.isoformat(sep=' ')
        })

    @route('/<uuid:template_uuid>/', methods=['DELETE'])
    @decorators.auth()
    def delete(self, **kwargs):
        """
        Delete template
        """        
        # delete template
        template = kwargs.get('template')
        db.session.delete(template)
        db.session.commit()

        return response({
            'uuid': template.uuid,
            'label': template.label,
            'text': template.text,
            'createdAt': template.createdAt.isoformat(sep=' ')
        })
