import os
def calculate_parking_price(days,hours,minutes):

    price = 0

    price = days*250 + hours*10
    if(minutes<30):
        price += 5
    else:
        price += 7
    
    return price

#Tests
#p=calculate_parking_price(1,2,3)
#print(p)