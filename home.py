# Luke

## AUTH
### Get user and permissions
def get_user():
    ### Firebase
    return 0

## EVENTS

def get_events():
    ### Get all events this week from event table
    ### Seperate into today and rest of week
    ### return array of dictionaries of events
    return []
## PortCo TODOs
def get_portcos():
    ## for every company in portfolio, add it to list
    ## retunr list
    return []
### Pull Activities for all portcos, list highest priority or any that have a near due date
## RP TODOs
### Pull Activities for RPVC Company
def get_activities(company_ids):
    ## For every company id in company ids, get all it's activities in the table
    ## return top X or all sorted by priority in a list of dictionaries
    ## to get RPVC todos, just pass only RPVC company id, to get portcos, run the get portcos first then pass their ids in
    return []
## Deals
### Pull all the active deals RPVC has
def get_deals():
    ## pull all active deals from the deals table
    ## list of dictionaries of deals
    return []

def add_to_agenda(item):
    ## Item is a dictionary of agenda details
    ## To do this, we add an activity and activityComapny with RPVC id and new activity id
    ## return the db copy of the activity
    return {}

def add_deal(deal):
    ## Create new deal record
    ## Return db copy of deal
    return {}

