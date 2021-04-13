from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.assessment_controller import api as assessment_ns
from .main.controller.activity_controller import api as activity_ns
from .main.controller.company_controller import api as company_ns
from .main.controller.user_company_controller import api as user_company_ns
from .main.controller.deal_controller import api as deal_ns
from .main.controller.deal_investor_controller import api as deal_investor_ns
from .main.controller.event_controller import api as event_ns
from .main.controller.event_participant_controller import api as event_participant_ns
from .main.controller.note_controller import api as note_ns
from .main.controller.vote_controller import api as vote_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Room 40 API',
          version='1.0',
          description='The development environment for endpoints for the Room 40 superapp. One app to rule them All.',
          contact='luke@fromstandard.com',
          
          )

api.add_namespace(user_ns, path="/user")
api.add_namespace(user_company_ns, path="/user_company")
api.add_namespace(auth_ns)
api.add_namespace(assessment_ns, path="/company/<company_id>/assessment")
api.add_namespace(activity_ns, path="/company/<company_id>/activity")
api.add_namespace(company_ns, path="/company")
api.add_namespace(deal_ns, path="/deal")
api.add_namespace(event_ns, path="/deal/<deal_id>/event")
api.add_namespace(note_ns, path="/deal/<deal_id>/note")
api.add_namespace(deal_investor_ns, path="/deal_investor")
api.add_namespace(event_participant_ns, path="/event_participant")
api.add_namespace(vote_ns, path="/vote")

