import uuid
import datetime

from app.main import db
from app.main.model.document import Document

def save_new_document(data):
    try:
        new_document = Document(
            title=data['title'],
	    contents=data['contents'],
	    created_by=0,
	    modified_by=0,
	    #UPDATE THIS
	    created_date=datetime.datetime.now(),
	    modified_date=datetime.datetime.now(),
	    is_deleted=False,
	    is_active=True
        )
        save_changes(new_document)
        response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
            }
        return response_object, 201

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

def update_document(document_id, data):

    try:
        property = get_a_document(document_id)

        property.title=data['title'],
        property.contents=data['contents'],
        property.modified_by=0,
	property.modified_time=datetime.datetime.now(),
	property.is_active=data['is_active'],
	#CHANGE THIS
        save_changes(property)

        response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                }
        return response_object, 201

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401



def save_changes(data):
    db.session.add(data)
    db.session.commit()
