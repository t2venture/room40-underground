import uuid
import datetime

from app.main import db
from app.main.model.property_model import PropertyModel
import datetime

def save_new_property_model(data):
    try:
        new_property_model = PropertyModel(
            property_id=data['property_id'],
            project_oneyear=data['project_oneyear'],
            project_twoyear=data['project_twoyear'],
            project_fiveyear=data['project_fiveyear'],
            threemonth_corr=data['threemonth_corr'],
            sixmonth_corr=data['sixmonth_corr'],
            lower_series=data['lower_series'],
            median_series=data['median_series'],
            upper_series=data['upper_series'],
            model_metrics=data['model_metrics'],
            model_type=data['model_type'],
            created_time=datetime.datetime.utcnow(),
            modified_time=datetime.datetime.utcnow(),
            is_deleted=False,
            is_active=True,
            created_by=1,
            modified_by=1,
        )
        save_changes(new_property_model)
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

def update_property_model(property_model_id, data):

    try:
        property_model = get_a_property_model(property_model_id)
        if 'property_id' not in data.keys():
            data['property_id']=property_model.property_id
        if 'project_oneyear' not in data.keys():
            data['project_oneyear']=property_model.project_oneyear
        if 'project_twoyear' not in data.keys():
            data['project_twoyear']=property_model.project_twoyear
        if 'project_fiveyear' not in data.keys():
            data['project_fiveyear']=property_model.project_fiveyear
        if 'threemonth_corr' not in data.keys():
            data['threemonth_corr']=property_model.threemonth_corr
        if 'sixmonth_corr' not in data.keys():
            data['sixmonth_corr']=property_model.sixmonth_corr
        if 'lower_series' not in data.keys():
            data['lower_series']=property_model.lower_series
        if 'median_series' not in data.keys():
            data['median_series']=property_model.median_series
        if 'upper_series' not in data.keys():
            data['upper_series']=property_model.upper_series
        if 'model_metrics' not in data.keys():
            data['model_metrics']=property_model.model_metrics
        property_model.property_id=data['property_id']
        property_model.project_oneyear=data['project_oneyear']
        property_model.project_twoyear=data['project_twoyear']
        property_model.project_fiveyear=data['project_fiveyear']
        property_model.threemonth_corr=data['threemonth_corr']
        property_model.sixmonth_corr=data['sixmonth_corr']
        property_model.lower_series=data['lower_series']
        property_model.median_series=data['median_series']
        property_model.upper_series=data['upper_series']
        property_model.model_metrics=data['model_metrics']
        property_model.modified_by=data['login_user_id']
        property_model.modified_time=data['action_time']
        save_changes(property_model)

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

def delete_a_property_model(property_model_id, data):
    try:
        del_pms=PropertyModel.query.filter_by(id=property_model_id).all()
        for dpm in del_pms:
            dpm.is_deleted=True
            dpm.modified_time=data['action_time']
            dpm.modified_by=data['login_user_id']
            #should be 1
        db.session.commit()
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

def get_all_property_models(is_deleted=False, is_active=True, property_id=""):
    pms=PropertyModel.query
    if property_id and property_id!="":
        pms=pms.filter_by(property_id=property_id)
    pms=pms.filter_by(is_deleted=False).filter_by(is_active=True).all()
    return pms

def get_all_deleted_property_models():
    return PropertyModel.query.filter_by(is_deleted=True).all()

def get_a_property_model(property_model_id):
    return PropertyModel.query.filter_by(id=property_model_id).filter_by(is_deleted=False).filter_by(is_active=True).first()

def get_a_property_model_by_property_id(property_id):
    return PropertyModel.query.filter_by(property_id=property_id).filter_by(is_deleted=False).filter_by(is_active=True).first()

def save_changes(data):
    db.session.add(data)
    db.session.commit()