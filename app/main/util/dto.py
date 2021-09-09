from flask_restplus import Namespace, fields

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'id': fields.String(required=False, description='auth id'),
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class CompanyDto:
    api = Namespace('company', description='company related operations')
    company = api.model('company', {
        'id': fields.String(required=False, description='company id'),
        'name': fields.String(required=True, description='company name'),
        'description': fields.String(required=True, description='company description'),
        'website': fields.String(description='company website'),
        'industry': fields.String(description='company industry'),
        'status': fields.String(description='company status'),
        'crunchbase': fields.String(description='company crunchbase profile'),
        'pitchbook': fields.String(description='company pitchbook profile')
    })

class DocumentDto:
    api = Namespace('document', description='document related operations')
    document = api.model('document', {
        'id': fields.String(required=False, description='document id'),
        'title': fields.String(required=True, description='document title'),
        'contents': fields.String(required=True, description='document controls'),
        'created_by': fields.String(required=False, description='id of who created the document'),
        'modified_by': fields.String(required=False, description='id of who modified the document'),
        'created_time': fields.String(required=False, description='when the document was created'),
        'modified_time': fields.String(required=False, description='when the document was modified'),
        'is_deleted': fields.String(required=True, description='is the document deleted'),
        'is_active': fields.String(required=True, description = 'is the document active or not')
    })

class UserCompanyDto:
    api = Namespace('user company', description='user_company related operations')
    user_company = api.model('user_company', {
        'id': fields.String(required=False, description='user company id'),
        'user_id': fields.String(required=True, description='user id'),
        'company_id': fields.String(required=True, description='company id'),
        'role': fields.String(required=False, description='user password'),
    })

class UserTeamDto:
    api=Namespace('user team', description='user team related operations')
    user_team = api.model('user_team', {
        'id': fields.String(required=False, description='user team id'),
        'user_id': fields.String(required=True, description='user id'),
        'team_id': fields.String(required=True, description='team id'),
    })

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'id': fields.String(required=False, description='user id'),
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier'),
        'linkedin_url': fields.String(description='user LinkedIn'),
        'twitter_url': fields.String(description='user Twitter')
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
        'model_series': fields.String(required=False, description='model series')
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
        'company_id': fields.String(required=True, description='id of the company the team is part of'),
    })