from flask_restplus import Namespace, fields


class ActivityDto:
    api = Namespace('activity', description='activity related operations')
    activity = api.model('activity', {
        'id': fields.String(required=False, description='company id'),
        'title': fields.String(required=True, description='activity title'),
        'priority': fields.String(required=True, description='activity priority'),
        'due': fields.DateTime(required=True, description='activity_due_date', dt_format='rfc822')
    })

class AssessmentDto:
    api = Namespace('assessment', description='assessment related operations')
    assessment = api.model('assessment', {
        'id': fields.String(required=False, description='company id'),
        'quarter': fields.String(required=True, description='assessment quarter'),
        'assessment_field_1': fields.String(required=True, description='assessment field one rank'),
        'assessment_field_1_des': fields.String(required=True, description='assessment field one description'),
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'id': fields.String(required=False, description='company id'),
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class CompanyActivityDto:
    api = Namespace('company_activity', description='company_activity related operations')
    company_activity = api.model('company_activity', {
        'id': fields.String(required=False, description='company id'),
        'activity_id': fields.String(required=True, description='activity id'),
        'company_id': fields.String(required=True, description='company id'),
    })

class CompanyAssessmentDto:
    api = Namespace('company_assessment', description='company_assessment related operations')
    company_assessment = api.model('company_assessment', {
        'id': fields.String(required=False, description='company id'),
        'assessment_id': fields.String(required=True, description='activity id'),
        'company_id': fields.String(required=True, description='company id'),
    })

class CompanyDto:
    api = Namespace('company', description='company related operations')
    company = api.model('company', {
        'id': fields.String(required=False, description='company id'),
        'name': fields.String(required=True, description='company name'),
        'description': fields.String(required=True, description='company description'),
        'website': fields.String(description='company website'),
        'crunchbase': fields.String(description='company crunchbase profile'),
        'pitchbook': fields.String(description='company pitchbook profile')
    })

class DealEventDto:
    api = Namespace('deal_event', description='deal_event related operations')
    deal_event = api.model('deal_event', {
        'id': fields.String(required=False, description='company id'),
        'deal_id': fields.String(required=True, description='deal id'),
        'event_id': fields.String(required=True, description='event id'),
    })

class DealInvestorDto:
    api = Namespace('deal investor', description='deal_investor related operations')
    deal_investor = api.model('deal_investor', {
        'id': fields.String(required=False, description='company id'),
        'deal_id': fields.String(required=True, description='deal id'),
        'investor_id': fields.String(required=True, description='investor id'),
        'amount': fields.String(description="investor size")
    })

class DealNoteDto:
    api = Namespace('deal_note', description='deal_note related operations')
    deal_note = api.model('deal_note', {
        'id': fields.String(required=False, description='company id'),
        'deal_id': fields.String(required=True, description='deal id'),
        'note_id': fields.String(required=True, description='note id'),
    })

class DealDto:
    api = Namespace('deal', description='deal related operations')
    deal = api.model('deal', {
        'id': fields.String(required=False, description='company id'),
        'stage': fields.String(required=True, description='deal stage'),
        'name': fields.String(description='descriptive name of deal'),
        'size': fields.String(required=True, description='size of deal'),
        'post_money': fields.String(required=True, description='post money valuation of deal'),
        'lead_id': fields.String(description='user leading deal'),
        'company_id': fields.String(required=True, description='company for the deal'),
        'initial_vote_id': fields.String(description='intial vote'),
        'final_vote_id': fields.String(description='final vote'),
    })

class EventParticipantDto:
    api = Namespace('event participant', description='event_participant related operations')
    event_participant = api.model('event_participant', {
        'id': fields.String(required=False, description='company id'),
        'event_id': fields.String(required=True, description='event id'),
        'participant_id': fields.String(required=True, description='user id'),
    })

class EventDto:
    api = Namespace('event', description='event related operations')
    event = api.model('event', {
        'id': fields.String(required=False, description='company id'),
        'time': fields.DateTime(required=True, description='time of event', dt_format='rfc822'),
        'link': fields.String(description='event link'),
        'description': fields.String(required=True, description='event description'),
        'notes': fields.String(description='event notes'),
        'event_type': fields.String(description='event type')
    })

class NoteDto:
    api = Namespace('note', description='note related operations')
    note = api.model('note', {
        'id': fields.String(required=False, description='company id'),
        'description': fields.String(required=True, description='note content'),
        'category': fields.String(required=True, description='category of note'),
        'is_thesis': fields.String(required=True, description='is note a thesis'),
    })

class UserCompanyDto:
    api = Namespace('user company', description='user_company related operations')
    user_company = api.model('user_company', {
        'id': fields.String(required=False, description='company id'),
        'user_id': fields.String(required=True, description='user id'),
        'company_id': fields.String(required=True, description='company id'),
        'role': fields.String(required=True, description='user password'),
    })

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'id': fields.String(required=False, description='company id'),
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier'),
        'linkedin_url': fields.String(description='user LinkedIn'),
        'twitter_url': fields.String(description='user Twitter')
    })

class VoteDto:
    api = Namespace('vote', description='vote related operations')
    vote = api.model('vote', {
        'id': fields.String(required=False, description='company id'),
        'vote_field_1': fields.String(required=True, description='vote field 1'),
        'vote_field_1_des': fields.String(required=True, description='vote field 1 description'),
    })