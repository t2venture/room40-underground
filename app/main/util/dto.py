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

class DealInvestorDto:
    api = Namespace('deal investor', description='deal_investor related operations')
    deal_investor = api.model('deal_investor', {
        'id': fields.String(required=False, description='deal investor id'),
        'deal_id': fields.String(required=True, description='deal id'),
        'investor_id': fields.String(required=True, description='investor id'),
        'amount': fields.String(description="investor size"),
        'date': fields.DateTime(description='investment date', dt_format='rfc822'),
        'investment_type': fields.String(description="opportunistic or core"),
        'fund_invested': fields.String(description="fund 1, 2, ..."),
    })

class DealDto:
    api = Namespace('deal', description='deal related operations')
    deal = api.model('deal', {
        'id': fields.String(required=False, description='deal id'),
        'stage': fields.String(required=True, description='deal stage'),
        'name': fields.String(description='descriptive name of deal'),
        'size': fields.String(required=True, description='size of deal'),
        'post_money': fields.String(required=True, description='post money valuation of deal'),
        'lead_id': fields.String(description='user leading deal'),
        'company_id': fields.String(required=True, description='company for the deal'),
    })

class EventParticipantDto:
    api = Namespace('event participant', description='event_participant related operations')
    event_participant = api.model('event_participant', {
        'id': fields.String(required=False, description='event participant id'),
        'event_id': fields.String(required=True, description='event id'),
        'participant_id': fields.String(required=True, description='user id'),
    })

class NoteDto:
    api = Namespace('note', description='note related operations')
    note = api.model('note', {
        'id': fields.String(required=False, description='note id'),
        'description': fields.String(required=True, description='note content'),
        'category': fields.String(required=True, description='category of note'),
        'is_thesis': fields.String(required=True, description='is note a thesis'),
        'deal_id': fields.String(required=False, description='what deal is the note apart of'),
        'keywords': fields.String(required=True, description='note keywords'),
        'deal_id': fields.String(required=True, description='deal for note'),
    })

class UserCompanyDto:
    api = Namespace('user company', description='user_company related operations')
    user_company = api.model('user_company', {
        'id': fields.String(required=False, description='user company id'),
        'user_id': fields.String(required=True, description='user id'),
        'company_id': fields.String(required=True, description='company id'),
        'role': fields.String(required=True, description='user password'),
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

class HouseUnitDto:
    api = Namespace('house_unit', description='houseunit related operations')
    house_unit = api.model('house_unit', {
        'id': fields.String(required=False, description='houseunit id'),
        'majorcity': fields.String(required=True, description='majorcity'),
        'building_sqft_area': fields.String(required=True, description='houseunit building area'),
        'gross_sqft_area': fields.String(required=True, description='housunit total area'),
        'address': fields.String(required=True, description='houseunit address'),
    })

class HouseModelDto:
    api = Namespace('house_model', description='house_model related operations')
    house_model = api.model('house_model', {
        'id': fields.String(required=False, description='id'),
        'houseunit_id': fields.String(required=True, description='houseunit_id'),
        'project_oneyear': fields.String(required=True, description='project_oneyear'),
        'project_twoyear': fields.String(required=True, description='project_twoyear'),
        'project_fiveyear': fields.String(required=True, description='project_fiveyear'),
    })
