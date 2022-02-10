import uuid
import datetime
from sqlalchemy import desc
from app.main import db
from app.main.model.summary import Summary

def save_new_summary(data):
	try:
		new_summary =Summary(
			zipcode=data['zipcode'],
			total_units=data['total_units'],
			low_curr_frac=data['low_curr_frac'],
			high_curr_frac=data['high_curr_frac'],
			low_proj1_frac=data['low_proj1_frac'],
			high_proj1_frac=data['high_proj1_frac'],
			low_proj2_frac=data['low_proj2_frac'],
			high_proj2_frac=data['high_proj2_frac'],
  	          	created_by=data['login_user_id'],
  	          	modified_by=data['login_user_id'],
  	          	created_time=data['action_time'],
  	          	modified_time=data['action_time'],
            		is_deleted=False,
            		is_active=True
		)
		response_object={'summmary_id': new_summary.id, 'status': 'success','message': 'Successfully registered.'}
		save_changes(new_summary)
		return response_object, 201
	except Exception as e:
		print (e)
		response_object={'status': 'fail', 'message': 'Something went wrong while adding a summary.'}
		return response_object, 400
def delete_a_summary(summary_id, data):
	try:
		summary_to_delete=get_a_summary(summary_id)
		summary_to_delete.is_deleted=True
		summary_to_delete.modified_time=data['action_time']
		summary_to_delete.modified_by=data['login_user_id']
		db.session.commit()
		response_object = {
			'status': 'success',
			'message': 'Successfully deleted.'
			}
		return response_object, 200
	except Exception as e:
		print(e)
		response_object = {
			'status': 'fail',
			'message': 'Some error occurred while deleting a summary. Please try again.'
			}
		return response_object, 401
			


def get_all_summaries(zipcode=0,is_deleted=False, is_active=True):
	V=Summary.query.filter(Summary.is_deleted==is_deleted).filter(Summary.is_active==is_active)
	if zipcode!=0:
		V=V.filter(Summary.zipcode==zipcode)
	return V.all()

def get_all_deleted_summaries():
	return Summary.query.filter(Summary.is_deleted==True).all()

def get_a_summary(summary_id):
	return Summary.query.filter(Summary.id==summary_id).filter(Summary.is_deleted==False).filter(Summary.is_active==True).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()
