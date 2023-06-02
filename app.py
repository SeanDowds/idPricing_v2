# This is Python 3.10.11

from flask import Flask, render_template, request, jsonify, make_response
# from datetime import datetime

import os
from email.message import EmailMessage
import ssl
# import smtplib


#for email
import yagmail
import tempfile
import logging

import psycopg2 as pg2
import pdfkit

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
from flask_wtf import FlaskForm

import sys

# Heroku - Remove the following 2 lines
#import dotenv
#dotenv.load_dotenv(dotenv_path="config.env")

'''
# Heroku - Remove the following 2 lines
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']

'''
# HEROKU - ADD THESE INSTEAD:
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')



#Heroku
conn = pg2.connect(
    host=DB_HOST,
    port='5432',
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    sslmode='prefer',
    connect_timeout=10
    )

    #postgres://ayfnpuhjmyxsws:b595e0ce91245d2a73c2d7cb9f6350e43b03356dd98a349c139924b628687975@ec2-44-213-151-75.compute-1.amazonaws.com:5432/dbk4l88vt08i5e


''' #AWS Lightsale
conn = pg2.connect(
    host='ls-74298ef97d6b5b45738cb51f40aad70ec35f056d.couqkmnifact.eu-west-2.rds.amazonaws.com',
    port='5432',
    dbname='postgres',
    user='dbmasteruser',
    password='s*7:%<}[{n9YG]xa39A4Z;7:nt[*)ip[',
    sslmode='prefer',
    connect_timeout=10
    )
'''

def initialSelection():
    c = conn.cursor()

    # Fetch All data
    c.execute('SELECT * FROM currentSelection WHERE id=1')

    # This is the data from the DB as above
    data = c.fetchall()

    # Close the cursor #excluded for sqlite
    c.close()

    # Return the data #excluded for sqlite
    return data



def clearAllDB():

    # Connect to the database
    c = conn.cursor()

    # Get the values for the row with id=1
    c.execute("SELECT * FROM currentSelection WHERE id = 1")
    row1_values = c.fetchone()

    
    c.execute("DELETE FROM currentSelection WHERE id = 2")


    sql = "INSERT INTO currentSelection (id, business, appType, qualityType, authType, budgetValue, userVolume, chip_Dashboard, chip_StaffManagement, chip_CustomerManagement, chip_Activity, chip_Ratings, chip_Animations, chip_Analytics, chip_QRCodes, chip_Calculator, chip_Video, chip_Upload, chip_Calendar, chip_Otherfeature, chip_Payments, chip_email, chip_Maps, chip_IOT, chip_SMS, chip_Finance, chip_Delivery, chip_Chat, chip_CRM, chip_ERP, chip_Fitness, chip_Other) "
    sql += "SELECT 2, business, appType, qualityType, authType, budgetValue, userVolume, chip_Dashboard, chip_StaffManagement, chip_CustomerManagement, chip_Activity, chip_Ratings, chip_Animations, chip_Analytics, chip_QRCodes, chip_Calculator, chip_Video, chip_Upload, chip_Calendar, chip_Otherfeature, chip_Payments, chip_email, chip_Maps, chip_IOT, chip_SMS, chip_Finance, chip_Delivery, chip_Chat, chip_CRM, chip_ERP,chip_Fitness, chip_Other "
    sql += "FROM currentSelection "
    sql += "WHERE id = 1"

    c.execute(sql)

    # Commit the changes
    conn.commit()

    # Close the connection
    # conn.close()


def updateBtnSelection(optionBus, optionApp, optionQuality, optionAuth):
    
    # conn = sqlite3.connect('db/appPrice.db')
    c = conn.cursor()

    # Insert a new row into the "currentSelection" table
    if optionBus:
        c.execute("UPDATE currentSelection SET business = %s WHERE id = 2", (optionBus,))
    if optionApp:
        c.execute("UPDATE currentSelection SET appType = %s WHERE id = 2", (optionApp,))
    if optionQuality:
        c.execute("UPDATE currentSelection SET qualityType = %s WHERE id = 2", (optionQuality,))
    if optionAuth:
        c.execute("UPDATE currentSelection SET authType = %s WHERE id = 2", (optionAuth,))

    # Commit the changes to the database
    conn.commit()


def updateRangeSelection(budget_value, user_volume):
    #conn = sqlite3.connect('db/appPrice.db')
    c = conn.cursor()

    # Insert a new row into the "currentSelection" table
    if budget_value:
        c.execute("UPDATE currentSelection SET budgetValue = %s WHERE id = 2", (budget_value,))
    if user_volume:
        c.execute("UPDATE currentSelection SET userVolume = %s WHERE id = 2", (user_volume,))


    # Commit the changes to the database
    conn.commit()


def updateChipSelection(allChips, selectedChips):

    #conn = sqlite3.connect('db/appPrice.db')
    c = conn.cursor()

    integerList = createIntegerList(allChips, selectedChips)

    for i, chip in zip(integerList, allChips):
        query = "UPDATE currentSelection SET {} = %s WHERE id = 2".format(chip)
        c.execute(query, (i,))

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    # conn.close()   


def createIntegerList(fullList, selectedList):
    integerList = []
    for item in fullList:
        if item in selectedList:
            integerList.append(1)
        else:
            integerList.append(0)

    return(integerList)



def listCurrentChips(listOfColumns):

    listCurrentChips = []

    # Open the connection
    c = conn.cursor()

    for this_column in listOfColumns:
        # Build the SQL query with a placeholder
        query = "SELECT {} FROM currentSelection WHERE id = 2".format(this_column)
        c.execute(query)
        current = c.fetchone()[0]
        if current == 1:
            listCurrentChips.append(this_column)

    # Close the cursor and the connection
    c.close()

    # conn.close() 

    return(listCurrentChips)


def retrieveCurrentValue(my_column):

    # Build the SQL query with a placeholder
    query = "SELECT {} FROM currentSelection WHERE id = 2".format(my_column)

    # Execute the query and retrieve the value
    c = conn.cursor()
    c.execute(query)
    value = c.fetchone()[0]

    # Close the cursor ,not the connection
    c.close()

    return(value)



app = Flask(__name__)


# Execute the init_db.py script on startup of the app
select = initialSelection()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


# Configuration for use in postgres on Huroku
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['postgres://ayfnpuhjmyxsws:b595e0ce91245d2a73c2d7cb9f6350e43b03356dd98a349c139924b628687975@ec2-44-213-151-75.compute-1.amazonaws.com:5432/dbk4l88vt08i5e']

# Endpoint for LightSail:
# ls-74298ef97d6b5b45738cb51f40aad70ec35f056d.couqkmnifact.eu-west-2.rds.amazonaws.com
# port for LightSail: 5432
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg2://dbmasteruser:s*7:%<}[{n9YG]xa39A4Z;7:nt[*)ip[@ls-74298ef97d6b5b45738cb51f40aad70ec35f056d.couqkmnifact.eu-west-2.rds.amazonaws.com:5432/postgres'

# Secret Key used with forms for when it goes on the cloud so it is not hacked
# app.config['SECRET_KEY']="pensil"


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/business_type.html", methods=["GET", "POST"])
def business_type():
    busOption = retrieveCurrentValue('business')
    return render_template('business_type.html',currentOption=busOption)

@app.route("/budget.html")
def budget():
    optionBudget = retrieveCurrentValue('budgetValue')
    return render_template('budget.html', currentRange=optionBudget)

@app.route("/apptype.html")
def app_type():
    optionApp = retrieveCurrentValue('appType')
    return render_template('apptype.html', currentOption=optionApp)

@app.route("/quality.html")
def quality():
    optionQuality = retrieveCurrentValue('qualityType')
    return render_template('quality.html', currentOption=optionQuality)

@app.route("/users.html")
def users():
    optionUsers = retrieveCurrentValue('userVolume')
    return render_template('users.html',currentRange=optionUsers)

@app.route("/auth.html")
def auth():
    optionAuth = retrieveCurrentValue('authType')
    return render_template('auth.html', currentOption=optionAuth)

@app.route("/intergrations.html")
def intergrations():
    intergrationsList=["chip_Payments","chip_email","chip_Maps", "chip_IOT", "chip_SMS", "chip_Finance", "chip_Delivery", "chip_Chat", "chip_CRM", "chip_ERP", "chip_Fitness", "chip_Other"]
    currentChips = listCurrentChips(intergrationsList)

    return render_template('intergrations.html', currentChips=currentChips)

@app.route("/features.html")
def features():
    features = ['chip_Dashboard', 'chip_StaffManagement',  'chip_CustomerManagement', 'chip_Activity', 
     'chip_Ratings', 'chip_Animations', 'chip_Analytics', 'chip_QRCodes', 'chip_Calculator', 
     'chip_Video', 'chip_Upload', 'chip_Calendar', 'chip_Otherfeature']
    currentChips = listCurrentChips(features)

    return render_template('features.html', currentChips=currentChips)

@app.route("/final.html", methods=['GET','POST'])
def final():
    return render_template('final.html')


@app.route('/handle_btn_id', methods=['POST'])
def handle_btn_id():
    # data is a reading form each front end page when a button is pressed that returns the button pressed and value
    # like this: data={'btn_id_auth': 'btn_email', 'is_button_true': True}
    data = request.get_json()
 
    btn_id_bus = data.get('btn_id_bus')
    btn_id_apptype = data.get('btn_id_apptype')
    btn_id_quality = data.get('btn_id_quality')
    btn_id_auth = data.get('btn_id_auth')

    is_button_true = data.get('is_button_true')
    
    if is_button_true:
        optionBus=btn_id_bus
        optionApp=btn_id_apptype
        optionQuality=btn_id_quality
        optionAuth=btn_id_auth

        #Enter in DB:
        updateBtnSelection(optionBus, optionApp, optionQuality, optionAuth)

    return ''


@app.route('/handle_range_value', methods=['POST'])
def handle_range_value():
    data = request.get_json()
    budget_value = data.get('budget_value')
    user_volume = data.get('user_volume')
    
    # Do something with the slider_value parameter here

    updateRangeSelection(budget_value, user_volume)
    
    return ''


@app.route('/handle_intergrations', methods=['POST'])
def handle_intergrations():
    intergrations = ['chip_Payments', 'chip_email', 'chip_Maps', 'chip_IOT', 'chip_SMS', 'chip_Finance', 
    'chip_Delivery', 'chip_Chat', 'chip_CRM', 'chip_ERP', 'chip_Fitness', 'chip_Other']

    data = request.get_json()
    intergration_ids = data.get('intergration_ids')

    # Do something with the list of button IDs here
    updateChipSelection(intergrations, intergration_ids)

    return ''


@app.route('/handle_features', methods=['POST'])
def handle_features():
    features = ['chip_Dashboard', 'chip_StaffManagement',  'chip_CustomerManagement', 'chip_Activity', 
     'chip_Ratings', 'chip_Animations', 'chip_Analytics', 'chip_QRCodes', 'chip_Calculator', 
     'chip_Video', 'chip_Upload', 'chip_Calendar', 'chip_Otherfeature']

    data = request.get_json()
    feature_ids = data.get('feature_ids')

    # Do something with the list of button IDs here
    updateChipSelection(features, feature_ids)

    return ''


def generate_pdf(html, pdf_name):
    with app.app_context():
       pdfkit.from_string(html, pdf_name)


@app.route('/handle_formdata', methods=['POST'])
def handle_formdata():
    # Get form data 
    name = request.form.get('name') 
    email = request.form.get('email')
    successMsg = ''

    # Generate unique PDF name
    pdf_name = 'inDetailQuote_' + name + '.pdf'

    itemList, listTotal = onSubmitButtonPressed(name, email)
    
    html = render_template('email.html', 
        name=name.capitalize(), email=email, itemList=itemList, listTotal=listTotal)

    # Call function to generate PDF
    generate_pdf(html, pdf_name)

    successMsg = sendEmail(pdf_name, email)

    # successMsg should be sent back to the final.htlm to a div to show success or failure

    return ''


def sendEmail(pdf_name, userEmail):
    print(f'({userEmail=}_______________this is the user email!)')
    try:
        logging.info('Sending email...')
        # Get the PDF file path 
        attachment = pdf_name #/path/to/file.pdf'

        text_content = 'Thank you for interest in our services. \nA detailed quote is attached.'
        text_failure = 'User email failed from ' + userEmail
        
        # Create a yagmail instance using your email account settings
        '''
        # DELETE THESE IN GITHUB AND USE IN THE ENV_VAR ON SERVER
        SENDER_EMAIL = os.environ['SENDER_EMAIL']
        SENDER_PASSWORD = os.environ['SENDER_PASSWORD']
        SENDER_SERVER = os.environ['SENDER_SERVER']
        '''
        # FOR HEROKU
        SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
        SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
        SENDER_SERVER = os.environ.get('SENDER_SERVER')
        
        yag = yagmail.SMTP(SENDER_EMAIL, SENDER_PASSWORD, SENDER_SERVER, 465)
        
        # Send the email with the file attachment
        yag.send(to=userEmail, subject='Quote details from inDetail.tech', contents=[text_content], attachments=[attachment])


    except Exception as e:
        print('--> Error sending email: %s' % e)
        logging.error('Error sending email: %s' % e)
        yag.send(to='sean@indetail.tech', subject='Error from userMail - Quote not delivered', contents=[text_failure], attachments=[attachment])


def priceTable():

    dict = {'business':{
        'SME':{'amnt':150, 'weight':1},
        'Startup':{'amnt':150, 'weight':1},
        'Corp':{'amnt':150, 'weight':1.1},
        },
    'appType':{
        'Web':{'amnt':300, 'weight':1},
        'Mobile':{'amnt':350, 'weight':1.1},
        'WM':{'amnt':550, 'weight':1.2},
    },
    'quality':{
        'MVP':{'amnt':0, 'weight':1},
        'UI':{'amnt':150, 'weight':1.3},
        'UX':{'amnt':200, 'weight':1.4},
    },    
    'auth':{
        'noAuth':{'amnt':0, 'weight':1},
        'email':{'amnt':100, 'weight':1.05},
        'fullAuth':{'amnt':150, 'weight':1.1},
    },
    'users':{
        'None':{'amnt':0, 'weight':1},
        '<100':{'amnt':500, 'weight':1.1},
        '<1000':{'amnt':600, 'weight':1.2},
        '<10000':{'amnt':1200, 'weight':1.3},
        '>10000':{'amnt':1500, 'weight':1.4},
    },
    'intergrations':{
        'payments':{'amnt':700, 'weight':1},
        'email':{'amnt':500, 'weight':1},
        'maps':{'amnt':500, 'weight':1},
        'iot':{'amnt':1000, 'weight':1.1},
        'sms':{'amnt':400, 'weight':1},
        'finance':{'amnt':1000, 'weight':1.1},
        'delivery':{'amnt':1100, 'weight':1.1},
        'chat':{'amnt':1000, 'weight':1},
        'crm':{'amnt':1000, 'weight':1.2},
        'erp':{'amnt':1000, 'weight':1.1},
        'fitness':{'amnt':1000, 'weight':1},
        'other':{'amnt':1000, 'weight':1.1},
    },
    'features':{
        'dashboard':{'amnt':1000, 'weight':1.2},
        'staffMan':{'amnt':1000, 'weight':1.1},
        'customerMan':{'amnt':1000, 'weight':1.2},
        'activity':{'amnt':300, 'weight':1.1},
        'ratings':{'amnt':450, 'weight':1.2},
        'Animations':{'amnt':500, 'weight':1},
        'Analytics':{'amnt':600, 'weight':1.15},
        'QRCodes':{'amnt':150, 'weight':1},
        'tools':{'amnt':150, 'weight':1},
        'video':{'amnt':150, 'weight':1},
        'upload':{'amnt':150, 'weight':1},
        'calendar':{'amnt':250, 'weight':1.15},
        'other':{'amnt':250, 'weight':1},
    },
    }

    return dict


def createPrintList(summaryList):
    finalAmnt, total, itemAmnt = 0, 0, 0
    combinedAmnts = 0
    combinedWeights = 1
    sumOfEach = 0
    ratio = 1
    printList = []

    for each in summaryList:
        combinedAmnts += each[1]
        combinedWeights *= each[2]
        sumOfEach += (each[1]*each[2])

    finalAmnt = (combinedAmnts*combinedWeights)
    ratio = finalAmnt/sumOfEach


    for each in summaryList:

        itemAmnt = round(ratio * each[1] * each[2],0)
        
        if itemAmnt != 0:

            if each[0] == 'btn_SME' or  each[0] == 'btn_Startup' or  each[0] == 'btn_Corporate':
                itemName = 'Discovery and Planning:'

            elif each[0] == 'btn_Web' or  each[0] == 'btn_Mobile' or  each[0] == 'btn_WM':
                itemName = 'Frontend SDK and Templating:'

            elif each[0] == 'btn_MVP':
                itemName = 'Layout design, Logo and colours:'

            elif each[0] == 'btn_UI':
                itemName = 'Visual design, layout and UI:'

            elif each[0] == 'btn_UX':
                itemName = 'Visual design, layout , UI and UX:'

            elif each[0] == 'btn_email' or  each[0] == 'btn_NoAuth' or  each[0] == 'btn_fullAuth':
                itemName = 'User authentication and authorisation:'

            else:
                try:
                    int(each[0])  
                except ValueError:  
                    itemName = each[0].capitalize()
                else:
                    itemName = 'Backend algorithms, structure and Database:'
            

            printList.append([itemName, format(itemAmnt, '.2f')])
        total += round(itemAmnt, 0)

        print(f'{itemName}:  {format(round(itemAmnt, 0),".2f")}')
        
    print()
    print(f'Total = {round(total,0)} ,  Check:{round(finalAmnt,0)}')


    strTotal = format(total, '.2f')

    return (printList, strTotal)


def fetchSelectedRecords():
    def getChipVal(group, chip, val):
        return priceDict[group][chip][val]

    priceDict=priceTable()
    print('These are the amnts and weights for key choices')

    totalPrice = 0
    totalWeight = 1
    itemRecords = []

    # Retreive the records for business from the DB, allocate amnt and weight
    # from the dict, and store them itemsRecord List
    if retrieveCurrentValue('business') == 'btn_SME':
        busAmnt = priceDict['business']['SME']['amnt']
        busWeight = priceDict['business']['SME']['weight']
    elif retrieveCurrentValue('business') == 'btn_Startup':
        busAmnt = priceDict['business']['Startup']['amnt']
        busWeight = priceDict['business']['Startup']['weight']
    elif retrieveCurrentValue('business') == 'btn_Corporate':
        busAmnt = priceDict['business']['Corp']['amnt']
        busWeight = priceDict['business']['Corp']['weight']
    items = [retrieveCurrentValue('business'),busAmnt,busWeight]
    itemRecords.append(items)
    print(f'{items[0]}: {items[1]} and {items[2]}')

    # Retreive the records for appType from the DB, allocate amnt and weight
    # from the dict, and store them itemsRecord List
    if retrieveCurrentValue('appType') == 'btn_Web':
        appTypeAmnt = priceDict['appType']['Web']['amnt']
        appTypeWeight = priceDict['appType']['Web']['weight']
    elif retrieveCurrentValue('appType') == 'btn_Mobile':
        appTypeAmnt = priceDict['appType']['Mobile']['amnt']
        appTypeWeight = priceDict['appType']['Mobile']['weight']
    elif retrieveCurrentValue('appType') == 'btn_WM':
        appTypeAmnt = priceDict['appType']['WM']['amnt']
        appTypeWeight = priceDict['appType']['WM']['weight']
    items = [retrieveCurrentValue('appType'),appTypeAmnt,appTypeWeight]
    itemRecords.append(items)
    print(f'{items[0]}: {items[1]} and {items[2]}')

    # Retreive the records for qualityType from the DB, allocate amnt and weight
    # from the dict, and store them itemsRecord List
    if retrieveCurrentValue('qualityType') == 'btn_MVP':
        qualityTypeAmnt = priceDict['quality']['MVP']['amnt']
        qualityTypeWeight = priceDict['quality']['MVP']['weight']
    elif retrieveCurrentValue('qualityType') == 'btn_UI':
        qualityTypeAmnt = priceDict['quality']['UI']['amnt']
        qualityTypeWeight = priceDict['quality']['UI']['weight']
    elif retrieveCurrentValue('qualityType') == 'btn_UX':
        qualityTypeAmnt = priceDict['quality']['UX']['amnt']
        qualityTypeWeight = priceDict['quality']['UX']['weight']
    items = [retrieveCurrentValue('qualityType'),qualityTypeAmnt,qualityTypeWeight]
    itemRecords.append(items)
    print(f'{items[0]}: {items[1]} and {items[2]}')    

    # Retreive the records for authType from the DB, allocate amnt and weight
    # from the dict, and store them itemsRecord List
    if retrieveCurrentValue('authType') == 'btn_NoAuth':
        authTypeAmnt = priceDict['auth']['noAuth']['amnt']
        authTypeWeight = priceDict['auth']['noAuth']['weight']
    elif retrieveCurrentValue('authType') == 'btn_email':
        authTypeAmnt = priceDict['auth']['email']['amnt']
        authTypeWeight = priceDict['auth']['email']['weight']
    elif retrieveCurrentValue('authType') == 'btn_fullAuth':
        authTypeAmnt = priceDict['auth']['fullAuth']['amnt']
        authTypeWeight = priceDict['auth']['fullAuth']['weight']
    items = [retrieveCurrentValue('authType'),authTypeAmnt,authTypeWeight]
    itemRecords.append(items)
    print(f'{items[0]}: {items[1]} and {items[2]}')   

    # Retreive the records for userVolume from the DB, allocate amnt and weight
    # from the dict, and store them itemsRecord List
    if retrieveCurrentValue('userVolume') == 0:
        userVolAmnt = priceDict['users']['None']['amnt']
        userVolWeight = priceDict['users']['None']['weight']
    elif 0 < retrieveCurrentValue('userVolume') < 100:
        userVolAmnt = priceDict['users']['<100']['amnt']
        userVolWeight = priceDict['users']['<100']['weight']
    elif 100 <= retrieveCurrentValue('userVolume') < 1000:
        userVolAmnt = priceDict['users']['<1000']['amnt']
        userVolWeight = priceDict['users']['<1000']['weight']
    elif 1000 <= retrieveCurrentValue('userVolume') < 10000:
        userVolAmnt = priceDict['users']['<10000']['amnt']
        userVolWeight = priceDict['users']['<10000']['weight']
    else:
        userVolAmnt = priceDict['users']['>10000']['amnt']
        userVolWeight = priceDict['users']['>10000']['weight']
    items = [retrieveCurrentValue('userVolume'),userVolAmnt,userVolWeight]
    itemRecords.append(items)
    print(f'Users {items[0]}: {items[1]} and {items[2]}')   


    print(f"this is the cost and weight for this Intergrations:")
    intergrationsDB=["chip_Payments","chip_email","chip_Maps", "chip_IOT", "chip_SMS", "chip_Finance", "chip_Delivery", "chip_Chat", "chip_CRM", "chip_ERP", "chip_Fitness", "chip_Other"]
    intergrationsDict=["payments","email","maps", "iot", "sms", "finance", "delivery", "chat", "crm", "erp", "fitness", "other"]

    totalIntergrationAmnt, totalIntergrationWeight = 0, 1
    totalFeaturesAmnt, totalFeaturesWeight = 0, 1
    thisAmnt, thisWeight = 0, 1

    # Check which intergrations are applicable, get their amnts and weight and 
    # add to itemRecords
    for iDB,iDict in zip(intergrationsDB,intergrationsDict):
        if retrieveCurrentValue(iDB) == 1:
            thisAmnt = getChipVal('intergrations', iDict, 'amnt')
            thisWeight = getChipVal('intergrations', iDict, 'weight')
            totalIntergrationAmnt += thisAmnt
            totalIntergrationWeight *= thisWeight
            itemRecords.append([iDict, thisAmnt, thisWeight])
            print (f'intergr: {iDict}: {thisAmnt} and {thisWeight}')

    print(f"this is the cost and weight for this Features:")
    featuresDB=['chip_Dashboard', 'chip_StaffManagement',  'chip_CustomerManagement', 'chip_Activity', 
     'chip_Ratings', 'chip_Animations', 'chip_Analytics', 'chip_QRCodes', 'chip_Calculator', 
     'chip_Video', 'chip_Upload', 'chip_Calendar', 'chip_Otherfeature']
    featuresDict=['dashboard', 'staffMan',  'customerMan', 'activity', 
     'ratings', 'Animations', 'Analytics', 'QRCodes', 'tools', 
     'video', 'upload', 'calendar', 'other']


    # Check which features are applicable, get their amnts and weight and 
    # add to itemRecords
    for fDB,fDict in zip(featuresDB,featuresDict):
        if retrieveCurrentValue(fDB) == 1:
            thisAmnt = getChipVal('features', fDict, 'amnt')
            thisWeight = getChipVal('features', fDict, 'weight')
            totalFeaturesAmnt += thisAmnt
            totalFeaturesWeight *= thisWeight
            itemRecords.append([fDict, thisAmnt, thisWeight])
            print (f'feature: {fDict}: {thisAmnt} and {thisWeight}')
    print('______________________________________________________')

    return itemRecords


def onSubmitButtonPressed(userName, userEmail):

    selectedRecords = fetchSelectedRecords()

    printList, total = createPrintList(selectedRecords)

    # SAVE QUOTE TO DB
    clearAllDB()

    return printList, total




