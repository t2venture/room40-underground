from app.main.model import user_team
from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.company_controller import api as company_ns
from .main.controller.user_company_controller import api as user_company_ns
from .main.controller.user_team_controller import api as user_team_ns
from .main.controller.property_controller import api as property_ns
from .main.controller.property_model_controller import api as property_model_ns
from .main.controller.portfolio_controller import api as portfolio_ns
from .main.controller.property_portfolio_controller import api as property_portfolio_ns
from .main.controller.team_portfolio_controller import api as team_portfolio_ns
from .main.controller.rent_controller import api as rent_ns
from .main.controller.team_controller import api as team_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Lasso Real Estate',
          version='1.0',
          description='The development environment for endpoints for the Lasso Real Estate App.',
          contact='luke@fromstandard.com',
          )

api.add_namespace(user_ns, path="/user")
api.add_namespace(user_company_ns, path="/user_company")
api.add_namespace(user_team_ns, path="/user_team")
api.add_namespace(auth_ns)
api.add_namespace(company_ns, path="/company")
api.add_namespace(property_ns, path="/property")
api.add_namespace(property_model_ns, path="/property_model")
api.add_namespace(portfolio_ns, path="/portfolio")
api.add_namespace(property_portfolio_ns, path="/property_portfolio")
api.add_namespace(rent_ns, path="/rent")
api.add_namespace(team_ns, path="/team")
api.add_namespace(team_portfolio_ns, path="/team_portfolio")