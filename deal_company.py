# Luke

## Company
def load_company(deal_id):
    ## Find deal in deal table with matching id
    ## Find the current company by taking company id and searching in the company table
    ## Pull up all the notes by looking at all dealNotes that have this dealId, then pull in all the notes
    ## Pull in all the founders from the foundersCompany table and then all the founders from the users table
    ## Pull in all the files from blog storage with this dealId
    # return dictionary of company statistics and supplementary info
### Pull up company overview/details

### Pull up current stage to determine greyed out buttons
### Pull up all notes
### Deal Lead Eval SUmmary pull up initial vote
### Pull up all files associated with the company

    return {}

def update_status(deal_id, status):
    ## change the status field in the company table
    ## return deal status as dictionary
    return {}

def add_note(deal_id, note):
    ## create new note record
    ## get company from deal
    ## create linking record from company to note
    ## return all notes for the company
    return []

def edit_eval(deal_id, eval):
    ## find the vote in the vote table and overwrite changes
    ## return the db version of the eval
    return {}

def add_file(deal_id, file):
    # more complicated but will likely add to blob with company_id pulled from deal
    # return all files
    return []