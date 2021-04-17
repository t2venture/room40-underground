from flask_restplus import Namespace, fields


class ActivityDto:
    api = Namespace('activity', description='activity related operations')
    activity = api.model('activity', {
        'id': fields.String(required=False, description='activity id'),
        'title': fields.String(required=True, description='activity title'),
        'priority': fields.String(required=True, description='activity priority'),
        'due': fields.DateTime(required=True, description='activity_due_date', dt_format='rfc822')
    })

class AssessmentDto:
    api = Namespace('assessment', description='assessment related operations')
    assessment = api.model('assessment', {
        'id': fields.String(required=False, description='assessment id'),
        'quarter': fields.String(required=True, description='assessment quarter'),
        'sentiment': fields.String(required=True, description='assessmentrank'),
        'notes': fields.String(required=True, description='assessment description'),
    })

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'id': fields.String(required=False, description='auth id'),
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })

class CompanyActivityDto:
    api = Namespace('company_activity', description='company_activity related operations')
    company_activity = api.model('company_activity', {
        'id': fields.String(required=False, description='company activity id'),
        'activity_id': fields.String(required=True, description='activity id'),
        'company_id': fields.String(required=True, description='company id'),
    })

class CompanyAssessmentDto:
    api = Namespace('company_assessment', description='company_assessment related operations')
    company_assessment = api.model('company_assessment', {
        'id': fields.String(required=False, description='company assessment id'),
        'assessment_id': fields.String(required=True, description='assessment id'),
        'company_id': fields.String(required=True, description='company id'),
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
    
class CompanyHighlightDto:
    api = Namespace('company_highlight', description='company highlights')
    company_highlight = api.model('company_highlight', {
        'id': fields.String(required=False, description='company_highlight id'),
        'highlight_id': fields.String(required=True, description='highlight id'),
        'company_id': fields.String(required=True, description='company id'),
    })

class DealEventDto:
    api = Namespace('deal_event', description='deal_event related operations')
    deal_event = api.model('deal_event', {
        'id': fields.String(required=False, description='deal event id'),
        'deal_id': fields.String(required=True, description='deal id'),
        'event_id': fields.String(required=True, description='event id'),
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

class DealNoteDto:
    api = Namespace('deal_note', description='deal_note related operations')
    deal_note = api.model('deal_note', {
        'id': fields.String(required=False, description='deal note id'),
        'deal_id': fields.String(required=True, description='deal id'),
        'note_id': fields.String(required=True, description='note id'),
    })

class DealVoteDto:
    api = Namespace('deal_vote', description='deal_vote related operations')
    deal_note = api.model('deal_vote', {
        'id': fields.String(required=False, description='deal note id'),
        'deal_id': fields.String(required=True, description='deal id'),
        'vote_id': fields.String(required=True, description='vote id'),
        'stage': fields.String(required=True, description='stage of vote'),
        'name': fields.String(required=True, description='name of voter'),
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

class EventDto:
    api = Namespace('event', description='event related operations')
    event = api.model('event', {
        'id': fields.String(required=False, description='event id'),
        'time': fields.DateTime(required=True, description='time of event', dt_format='rfc822'),
        'link': fields.String(description='event link'),
        'description': fields.String(required=True, description='event description'),
        'notes': fields.String(description='event notes'),
        'event_type': fields.String(description='event type')
    })
class HighlightDto:
    api = Namespace('highlight', description='highlights')
    highlight = api.model('highlight', {
        'id': fields.String(required=False, description='highlight id'),
        'notes': fields.String(required=True, description='highlight notes'),
        'is_active': fields.String(description='active displayed highlight'),
    })

class NoteDto:
    api = Namespace('note', description='note related operations')
    note = api.model('note', {
        'id': fields.String(required=False, description='note id'),
        'description': fields.String(required=True, description='note content'),
        'category': fields.String(required=True, description='category of note'),
        'is_thesis': fields.String(required=True, description='is note a thesis'),
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

class VoteDto:
    api = Namespace('vote', description='vote related operations')
    vote = api.model('vote', {
        'id': fields.String(required=False, description='vote id'),
        'team': fields.String(required=True, description='team rank'),
        'team_notes': fields.String(required=True, description='team description'),
        'market': fields.String(required=True, description='market rank'),
        'market_notes': fields.String(required=True, description='market description'),
        'product': fields.String(required=True, description='product rank'),
        'product_notes': fields.String(required=True, description='product description'),
    })