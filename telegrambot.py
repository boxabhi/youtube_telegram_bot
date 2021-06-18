import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tele_core.settings'
django.setup()


from telegram.ext import * 
from home.models import *
import re
from home.helpers import *

API_KEY = '1850071620:AAEgnLjlFXXST25n-ZvuojWhMtZQ1AucETk'

def isValidPinCode(pinCode):
    regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$"; 
    p = re.compile(regex)
    if (pinCode == ''):
        return False;
    m = re.match(p, pinCode)
    if m is None:
        return False
    else:
        return True

def num_there(s):
    return any(i.isdigit() for i in s)

def handle_message(update , context):
    text = str(update.message.text).lower()
    
    if num_there(text):
        if isValidPinCode(text):
            cowin_objs = CowinData.objects.filter(pincode = text)

            if not cowin_objs.exists():
                get_cowin_data_by_pincode(text)
                cowin_objs = CowinData.objects.filter(pincode = text)



            message = f""" Total {cowin_objs.count()} slots found in your pincode """
            
            for cowin_obj in cowin_objs:
                message += f"""Place nam {cowin_obj.fee_type} {cowin_obj.fee} {cowin_obj.available_capacity} {cowin_obj.available_capacity_dose1} {cowin_obj.available_capacity_dose2} {cowin_obj.min_age_limit} {cowin_obj.vaccine} \n \n """

                
            update.message.reply_text(f"{message}")
            return
        else:
            update.message.reply_text(f"Not a vaild pincode")
            return



    update.message.reply_text(f"Hi, {update['message']['chat']['first_name']} enter pincode to get vaccine updates")



if __name__ == '__main__':
    updater = Updater(API_KEY , use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text , handle_message))

    updater.start_polling(1.0)
    updater.idle()