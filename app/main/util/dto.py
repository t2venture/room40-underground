from flask_restplus import Namespace, fields

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'id': fields.String(required=False, description='auth id'),
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class ConfirmDto:
    api = Namespace('confirm', description='confirmation related operations')
    user_confirm = api.model('confirmation_details', {
        'token': fields.String(required=True, description='confirmation token'),
        'password': fields.String(required=True, description='password to be changed')
    })

class ChangepasswordDto:
    api = Namespace('changepassword', description='change password related operations')
    changepassword = api.model('change password details', {
        'oldpassword': fields.String(required=True, description='old password'),
        'newpassword': fields.String(required=True, description='new password')
    })

class DocumentDto:
    api = Namespace('document', description='document related operations')
    document = api.model('document', {
        'id': fields.String(required=False, description='document id'),
        'title': fields.String(required=True, description='document title'),
        'contents': fields.String(required=True, description='document controls'),
    })

class UserTeamDto:
    api=Namespace('user team', description='user team related operations')
    user_team = api.model('user_team', {
        'id': fields.String(required=False, description='user team id'),
        'user_id': fields.String(required=True, description='user id'),
        'team_id': fields.String(required=True, description='team id'),
        'role': fields.String(required=True, description='role of the user')
    })

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'id': fields.String(required=False, description='user id'),
        'first_name': fields.String(required=True, description='user first name'),
        'last_name': fields.String(required=True, description='user last name'),
        'profile_url': fields.String(required=False, description='img profile url'),
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=False, description='user username'),
        'linkedin_url': fields.String(required=False, description='user LinkedIn'),
        'twitter_url': fields.String(required=False, description='user Twitter'),
        'phonenumber': fields.String(required=False, description='phone number'),
        'company_name': fields.String(required=False, description="company of the user")
    })

class PropertyDto:
    api = Namespace('property', description='property related operations')
    property = api.model('property', {
        'id': fields.String(required=False, description='property id'),
        'majorcity': fields.String(required=True, description='majorcity'),
        'building_sqft_area': fields.String(required=True, description='property building area'),
        'gross_sqft_area': fields.String(required=True, description='property total area'),
        'address': fields.String(required=True, description='property address'),
        'latitude': fields.String(required=True, description='latitude of the property'),
        'longitude': fields.String(required=True, description='longitude of the property'),
        'street': fields.String(required=False, description='street name of the property'),
        'housenumber': fields.String(required=False, description='house number of the property'),
        'state': fields.String(required=False, description='state in which the property is'),
        'fips_code': fields.String(required=False, description='fips code'),
        'usage_code': fields.String(required=False, description='usage code'),
        'bd_rms': fields.String(required=False, description='number of bedrooms'),
        'bt_rms': fields.String(required=False, description='number of bathrooms'),
        'zipcode': fields.String(required=True, description='zipcode of the house'),
        'photos': fields.String(required=True, description='photos of the house - webpage links'),
        'market_price': fields.String(required=True, description='market price'),
        'listed': fields.String(required=True, description='whether it is listed or not'),
        'ann_mortgage_cost': fields.String(required=True, description='annual mortgage cost'),
        'estimated_rent': fields.String(required=True, description='estimated rent'),
        'cap_rate': fields.String(required=True, description='cap rate'),
        'yield_rate': fields.String(required=True, description='yield rate'),
        'lasso_score': fields.String(required=True, description='lasso score'),
        'lasso_property': fields.String(required=True, description='lasso property subscore'),
        'lasso_economics': fields.String(required=True, description='lasso economics subscore'),
        'lasso_location': fields.String(required=True, description='lasso location subscore'),
        'lasso_macro': fields.String(required=True, description='lasso macro subscore'),
        'hoa_fee': fields.String(required=True, description='hoa fee'),
        'hoa_rent': fields.String(required=True, description='hoa_rent'),
        'est_property_tax': fields.String(required=True, description='estimated property tax'),
        'est_insurance': fields.String(required=True, description='estimated insurance')
    })

class PropertyModelDto:
    api = Namespace('property_model', description='property_model related operations')
    property_model = api.model('property_model', {
        'id': fields.String(required=False, description='id'),
        'property_id': fields.String(required=True, description='property_id'),
        'project_oneyear': fields.String(required=True, description='project_oneyear'),
        'project_twoyear': fields.String(required=True, description='project_twoyear'),
        'project_fiveyear': fields.String(required=True, description='project_fiveyear'),
        'threemonth_corr': fields.String(required=True, description='seasonal trend for 3 months'),
        'sixmonth_corr': fields.String(required=True, description='seasonal trend for 6 months'),
        'lower_series': fields.String(required=False, description='lower series'),
        'median_series': fields.String(required=False, description='median series'),
        'upper_series': fields.String(required=False, description='upper series'),
        'model_metrics': fields.String(required=False, description='model metrics'),
        'model_type': fields.String(required=False, description='type of the model')
    })

class PropertyHistoryDto:
    api=Namespace('property_history', description='property_history related operations')
    property_history = api.model('proeprty_history',{
        'id': fields.String(required=False, description='id'),
        'property_id': fields.String(required=True, description='property_id'),
        'prices': fields.String(required=False, description='stringified dict of the prices'),
        'events': fields.String(required=False, description='events in the history of the property')
    })

class PortfolioDto:
    api = Namespace('portfolio', description='portfolio related operations')
    portfolio = api.model('portfolio_model', {
        'id': fields.String(required=False, description='id'),
        'title': fields.String(required=True, description='title of the portfolio'),
        'description': fields.String(required=True, description='description of portfolio'),
    })

class PropertyPortfolioDto:
    api = Namespace('property_portfolio', description='property and portfolio link related operations')
    property_portfolio=api.model('property_portfolio', {
        'id': fields.String(required=False, description = 'id'),
	    'property_id': fields.String(required=True, description = 'id of the property'),
	    'portfolio_id': fields.String(required=True, description = 'id of portfolio'),
    })

class TeamPortfolioDto:
    api=Namespace('team_portfolio', description='team and portfolio link related operations')
    team_portfolio=api.model('team_portfolio', {
        'id': fields.String(required=False, description='id'),
        'team_id': fields.String(required=True, description= 'id of the team'),
        'portfolio_id': fields.String(required=True, description = 'id of portfolio'),
        'role': fields.String(required=True, description='role of the team in this portfolio'),
    })

class RentDto:
    api = Namespace('rent', description='rent related operations')
    rent=api.model('rent', {
        'id': fields.String(required=False, description='id of the rent'),
        'bedroom_count': fields.String(required=True, description='number of bedrooms in the rent unit'),
        'bathroom_count': fields.String(required=True, description='number of bathrooms in the rent unit'),
        'rounded_sqft_area': fields.String(required=True, description='area in sq ft rounded to the nearest 100'),
        'rent_amount': fields.String(required=False, description='monthly rent of the unit'),
    })

class TeamDto:
    api = Namespace('team', description='team related operations')
    team=api.model('team', {
        'id': fields.String(required=False, description='id of the team'),
        'name': fields.String(required=True, description='name of the team'),
        'color': fields.String(required=False, description='color scheme of the team'),
    })

class DemographicsDto:
    api = Namespace('demographics', description='summarized demographics')
    demographics=api.model('demographics',{
        'demog': fields.String(required=False, description='stringified dict of summarized demographics'),
    })