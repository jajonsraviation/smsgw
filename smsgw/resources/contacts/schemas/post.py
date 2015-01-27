# -*- coding: utf-8 -*-
# http://google-styleguide.googlecode.com/svn/trunk/pyguide.html

from smsgw.resources import patterns

schema = {
    "description": "Schema for the contacts POST endpoint",
    "type": "object",
    "method": "POST",
    "required": [
        "firstName", 
        "lastName",
        "phoneNumber"
    ],
    "additionalProperties": False, 
    "properties": {
        "firstName": {
            "type": "string",
            "minLength": 2,
            "maxLength": 16
        },
        "lastName": {            
            "type": "string",
            "minLength": 2,
            "maxLength": 16
        },
        "email": {
            "type": "string",
            "pattern": patterns.EMAIL
        },
        "phoneNumber": {
            "type": "string",
            "pattern": patterns.PHONE_NUMBER
        },
        "note": {
            "type": "string",
            "maxLength": 255
        }
    }
}