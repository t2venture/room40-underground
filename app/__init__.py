from app.main.model import user_team
from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.user_team_controller import api as user_team_ns
from .main.controller.property_controller import api as property_ns
from .main.controller.property_model_controller import api as property_model_ns
from .main.controller.portfolio_controller import api as portfolio_ns
from .main.controller.property_portfolio_controller import api as property_portfolio_ns
from .main.controller.team_portfolio_controller import api as team_portfolio_ns
from .main.controller.rent_controller import api as rent_ns
from .main.controller.team_controller import api as team_ns
from .main.controller.document_controller import api as document_ns
from .main.controller.property_history_controller import api as property_history_ns
from .main.controller.confirm_controller import api as confirm_ns
from .main.controller.changepassword_controller import api as changepassword_ns

blueprint = Blueprint('api', __name__)
#STUFF LUKE ADDED
authorizations = {
    'apiKey': {
        'type' : 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
##HERE
api = Api(blueprint,
          title='Lasso Real Estate',
          version='1.0',
          description='The development environment for endpoints for the Lasso Real Estate App.',
          contact='luke@fromstandard.com',
          security='apiKey',
          authorizations=authorizations
          )

api.add_namespace(user_ns, path="/user")
api.add_namespace(user_team_ns, path="/user_team")
api.add_namespace(auth_ns)
api.add_namespace(property_ns, path="/property")
api.add_namespace(property_model_ns, path="/property_model")
api.add_namespace(portfolio_ns, path="/portfolio")
api.add_namespace(property_portfolio_ns, path="/property_portfolio")
api.add_namespace(rent_ns, path="/rent")
api.add_namespace(team_ns, path="/team")
api.add_namespace(team_portfolio_ns, path="/team_portfolio")
api.add_namespace(document_ns, path="/document")
api.add_namespace(property_history_ns, path="/property_history")
api.add_namespace(confirm_ns, path="/confirm")
api.add_namespace(changepassword_ns, path="/changepassword")