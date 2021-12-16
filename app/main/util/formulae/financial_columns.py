import random
market_value=random.randint(3500, 5000)*100
ann_mortgage_cost = market_value/20
estimated_rent = ann_mortgage_cost / 7
hoa_fee = random.randint(400,800)
hoa_rent = True
est_property_tax = 0.0315 * market_value
est_insurance= 0.007452 * market_value
cap_rate = (estimated_rent - (ann_mortgage_cost/12) - hoa_fee - est_insurance - est_property_tax)/market_value
yield_rate: cap_rate * random.randint(95,105)/100