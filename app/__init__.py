from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.company_controller import api as company_ns
from .main.controller.user_company_controller import api as user_company_ns
from .main.controller.property_controller import api as property_ns
from .main.controller.property_model_controller import api as property_model_ns
from .main.controller.portfolio_controller import api as portfolio_ns
from .main.controller.property_portfolio_controller import api as property_portfolio_ns

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
api.add_namespace(company_ns, path="/company")
api.add_namespace(property_ns, path="/property")
api.add_namespace(property_model_ns, path="/property_model")
api.add_namespace(portfolio_ns, path="/portfolio")
api.add_namespace(property_portfolio_ns, path="/property_portfolio")