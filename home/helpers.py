import requests
import datetime

from .models import *
import json

def get_cowin_data_by_pincode(pincode):
    try:
        current_date = datetime.date.today().strftime('%d-%m-%Y')
        
        payload = requests.get(f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={current_date}')
        
        sessions = payload.json()


        for session in sessions.get('sessions'):
            
            if session.get('available_capacity') > 0:
                CowinData.objects.create(
                    center_id = session.get('center_id'),
                    name = session.get('name'),
                    state = session.get('state_name'),
                    pincode = session.get('pincode'),
                    fee_type = session.get('fee_type'),
                    fee = session.get('fee'),
                    available_capacity = session.get('available_capacity'),
                    available_capacity_dose1 = session.get('available_capacity_dose1'),
                    available_capacity_dose2 = session.get('available_capacity_dose2'),
                    min_age_limit = session.get('min_age_limit'),
                    vaccine = session.get('vaccine'),
                )




    except Exception as e:
        print(e)

    return False