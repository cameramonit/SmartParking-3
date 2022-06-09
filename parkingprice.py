import os
def calculate_parking_price(days,hours,minutes):
    price = 0
    price = days*2500 + hours*100
    if(minutes<30):
        price += 50
    else:
        price += 70
    
    return price

#Tests
#p=calculate_parking_price(1,2,3)
#print(p)