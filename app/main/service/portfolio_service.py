import uuid
import datetime

from app.main import db
from app.main.model.portfolio import Portfolio
from app.main.model.property_portfolio import PropertyPortfolio
from app.main.model.team_portfolio import TeamPortfolio
from app.main.service.property_portfolio_service import get_portfolios_from_property
from app.main.service.team_portfolio_service import get_portfolios_from_team, get_teams_from_portfolio, save_new_team_portfolio
from app.main.service.team_service import get_personal_team_id
def save_new_portfolio(data):
    try:
        new_portfolio = Portfolio(
            title=data['title'],
            description=data['description'],
            created_by=data['login_user_id'],
            modified_by=data['login_user_id'],
            created_time=data['action_time'],
            modified_time=data['action_time'],
            is_deleted=False,
            is_active=True,
        )
        save_changes(new_portfolio)
        new_data=dict()
        new_data["portfolio_id"]=new_portfolio.id
        new_data["team_id"]=get_personal_team_id(data['login_user_id'])["id"]
        new_data["role"]="Owner"
        save_new_team_portfolio(new_data)
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

def update_portfolio(portfolio_id, data):
    try:
        portfolio=get_a_portfolio(portfolio_id)
        if 'title' not in data.keys():
            data['title']=portfolio.title
        if 'description' not in data.keys():
            data['description']=portfolio.description
            #####
        portfolio.title=data['title']
        portfolio.description=data['description']
        portfolio.modified_by=data['login_user_id']
        portfolio.modified_time=data['action_time']
        save_changes(portfolio)
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


def delete_a_portfolio(portfolio_id, data):
    try:
        del_pfs=Portfolio.query.filter_by(id=portfolio_id).all()
        for pf in del_pfs:
            pf.is_deleted=True
            pf.modified_time=data['action_time']
            pf.modified_by=data['modified_by']
        db.session.commit()
        #need to change this
        dppfs=PropertyPortfolio.query.filter_by(portfolio_id=portfolio_id).all()
        for ppf in dppfs:
            ppf.is_deleted=True
            ppf.modified_time=data["action_time"]
            ppf.modified_by=data["login_user_id"]
        db.session.commit()
        del_tpfs=TeamPortfolio.query.filter_by(portfolio_id=portfolio_id).all()
        for tpf in del_tpfs:
            tpf.is_deleted=True
            tpf.modified_time=data['action_time']
            tpf.modified_by=data['modified_by']
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

def get_all_portfolios(property_id="", team_id="", is_deleted=False, is_active=True):
    # Get all portfolios
    portfolios=Portfolio.query.filter_by(is_deleted=False).filter_by(is_active=True)
    if property_id and property_id!="":
        portfolio_ids=[pt.portfolio_id for pt in get_portfolios_from_property(property_id)]
        portfolios=portfolios.filter(Portfolio.id.in_(portfolio_ids))
    if team_id and team_id!="":
        portfolios_ids=[tp.portfolio_id for tp in get_teams_from_portfolio(team_id)]
        portfolios=portfolios.filter(Portfolio.id.in_(portfolios_ids))
    return portfolios.all()

def get_all_deleted_portfolios():
    return Portfolio.query.filter_by(is_deleted=True).all()


def get_a_portfolio(portfolio_id):
    return Portfolio.query.filter_by(id=portfolio_id).filter_by(is_deleted=False).filter_by(is_active=True).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()