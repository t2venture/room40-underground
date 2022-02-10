import datetime
import random
from app.main import db
from app.main.model.property import Property
from app.main.model.property_model import PropertyModel
from app.main.model.summary import Summary
from sqlalchemy import func 

fields = [
	"zipcode", "total_units", "low_curr_frac", "high_curr_frac", "low_proj1_frac",
	"high_proj1_frac", "low_proj2_frac", "high_proj2_frac"]

headers = dict() # custom header names for given fieldname (no difference here)
for field in fields:
	headers[field] = field

# build data structures
data = []
rowMap = dict()    

query = db.session.query(Survey, Task, Assignment, Response) \
                      .join(Task, Survey.id==Task.survey_id) \
                      .join(Assignment, Task.id==Assignment.task_id) \
                      .join(Response, Assignment.id==Response.assignment_id) \
                      .filter(Survey.id == 1)

results = query.all()

# summarise counts
for (_, _, _, response) in results:
	rowMap[response.response_item][response.response_value] = rowMap[response.response_item][response.response_value] + 1

V=db.session.query(
	Property.zipcode, func.count(Property.id).label('count'), 
	func.avg(Property.market_price)
	).group_by(
		Property.zipcode).all()


