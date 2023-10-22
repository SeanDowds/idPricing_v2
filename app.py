# This is Python 3.10.11

from flask import Flask, render_template, request, jsonify, make_response, send_file, session
import io
import datetime
import requests

import os
import anvil
import anvil.server

import webbrowser

import psycopg2 as pg2

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
from flask_wtf import FlaskForm


# uplink_key = os.environ['UPLINK_KEY']
anvil.server.connect("server_JI4CJBFWWDR57RGATW5TJREU-KXOSLB3E74XGJLIP")

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


def initialSelection():
    c = conn.cursor()

    # Fetch All data
    c.execute('SELECT * FROM currentSelection WHERE id=1')

    # This is the data from the DB as above
    data = c.fetchall()

    # Close the cursor #excluded for sqlite
    c.close()
    print(f'Data from intial selections -=> {data}')
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
    c.close()

    # Commit the changes
    conn.commit()




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

    c = conn.cursor()

    # Insert a new row into the "currentSelection" table
    if budget_value:
        c.execute("UPDATE currentSelection SET budgetValue = %s WHERE id = 2", (budget_value,))
    if user_volume:
        c.execute("UPDATE currentSelection SET userVolume = %s WHERE id = 2", (user_volume,))

    # Commit the changes to the database
    conn.commit()
    print(f'138 retreived Uses sent to pgAdmin = {user_volume}')


def updateChipSelection(allChips, selectedChips):

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

    return(listCurrentChips)


def retrieveCurrentValue(my_column):

    # Build the SQL query with a placeholder
    query = "SELECT {} FROM currentSelection WHERE id = 2".format(my_column)

    # Execute the query and retrieve the value
    c = conn.cursor()
    c.execute(query)
    value = c.fetchone()[0]
    print(f'198 retreived Uses from pgAdmin = {value}')

    # Close the cursor ,not the connection
    c.close()

    return(value)


def recordNewUser(name, email):
    c = conn.cursor()
    
    query = "SELECT EXISTS(SELECT 1 FROM users WHERE email = %s)" 
    c.execute(query, (email,))
    email_exists = c.fetchone()[0]
      
    if not email_exists:
       query = "INSERT INTO users (name, email) VALUES (%s, %s)"
       c.execute(query, (name, email)) 
       conn.commit()


def recordQuoteDetails(email):
    c = conn.cursor()
    c.execute("SELECT * FROM currentSelection WHERE id = 2")
    row1_values = c.fetchone()

    email = email 
    created_at = datetime.datetime.now()

    SQL = "INSERT INTO estimate_variables (email,created_at, business,apptype,qualitytype,authtype,budgetvalue, uservolume, chip_other, chip_crm, chip_erp, chip_fitness, chip_dashboard, chip_staffmanagement, chip_customermanagement, chip_activity, chip_ratings, chip_animations, chip_analytics, chip_qrcodes, chip_calculator, chip_video, chip_upload, chip_calendar, chip_otherfeature, chip_payments, chip_email, chip_maps, chip_iot, chip_sms, chip_finance, chip_delivery, chip_chat)"
    SQL += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (email, created_at) + row1_values[1:]

    c.execute(f"{SQL} RETURNING id", values)

    id = c.fetchone()[0]

    conn.commit()

    return id


def recordQuoteValues(estimate_id, items, total):

    itemsLen=len(items)

    descriptions = [item[0] for item in items]
    amnts = [item[1] for item in items]

    # now add these to the db with a ref to the estimate_id for each one - Both TEXT CHARVAR(10)
    # Then add the list total INT to the DB

    num_elements_to_add = 35 - len(items)

    new_elements = [None for _ in range(num_elements_to_add)]
    descriptions.extend(new_elements)
    amnts.extend(new_elements)

    c = conn.cursor()

    SQL_descriptions = "INSERT INTO estimate_descriptions (estimate_id,Row_type,total,col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8,col_9,col_10,col_11,col_12,col_13,col_14,col_15,col_16,col_17,col_18,col_19,col_20,col_21,col_22,col_23,col_24,col_25,col_26,col_27,col_28,col_29,col_30,col_31,col_32,col_33,col_34,col_35)"
    SQL_descriptions += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    descriptions = (estimate_id, "descriptions", "TOTAL") + tuple(descriptions)

    c.execute(SQL_descriptions, descriptions)


    SQL_values = "INSERT INTO estimate_values (estimate_id, Row_type, total,col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8,col_9,col_10,col_11,col_12,col_13,col_14,col_15,col_16,col_17,col_18,col_19,col_20,col_21,col_22,col_23,col_24,col_25,col_26,col_27,col_28,col_29,col_30,col_31,col_32,col_33,col_34,col_35)"
    SQL_values += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (estimate_id, "values", str(total)) + tuple(amnts)

    c.execute(SQL_values, values)
    c.close()
    conn.commit()



app = Flask(__name__)

app.config['SECRET_KEY'] = 'your secret key here'

# Execute the init_db.py script on startup of the app
select = initialSelection()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


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
    print(f'375 Now {user_volume = }')
    
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


@app.route('/render_quote')
def render_quote():
    
    #Collect variables from js in final.html
    name = request.args.get('name')
    email = request.args.get('email')

    # Call priceCalculations function to get quote data  sen@dow.com
    itemList, listTotal = priceCalculations(name, email)

    recordNewUser(name, email)

    estimate_id = recordQuoteDetails(email)

    recordQuoteValues(estimate_id, itemList, listTotal)

    clearAllDB()

    return render_template('email.html', name=name.capitalize(), email=email, itemList=itemList, listTotal=listTotal)


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
        'MVP':{'amnt':0, 'weight':0.9},
        'UI':{'amnt':170, 'weight':1.15},
        'UX':{'amnt':200, 'weight':1.3},
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
        'email':{'amnt':600, 'weight':1},
        'maps':{'amnt':500, 'weight':1},
        'iot':{'amnt':1000, 'weight':1.1},
        'sms':{'amnt':400, 'weight':1},
        'finance':{'amnt':1000, 'weight':1.1},
        'delivery':{'amnt':1000, 'weight':1.1},
        'chat':{'amnt':900, 'weight':1},
        'crm':{'amnt':1000, 'weight':1.1},
        'erp':{'amnt':1000, 'weight':1.1},
        'fitness':{'amnt':1000, 'weight':1},
        'other':{'amnt':1000, 'weight':1.1},
    },
    'features':{
        'dashboard':{'amnt':1000, 'weight':1.1},
        'staffMan':{'amnt':1000, 'weight':1.1},
        'customerMan':{'amnt':1000, 'weight':1.2},
        'activity':{'amnt':300, 'weight':1.1},
        'ratings':{'amnt':450, 'weight':1.2},
        'Animations':{'amnt':500, 'weight':1},
        'Analytics':{'amnt':600, 'weight':1.15},
        'QRCodes':{'amnt':150, 'weight':1},
        'tools':{'amnt':150, 'weight':1},
        'video':{'amnt':180, 'weight':1},
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
                    print(f'543 backend: {each[0]=}')
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
    print(f'568 users now => {retrieveCurrentValue("userVolume")=}')
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
    print(f'635 users now => {retrieveCurrentValue("userVolume")=}')
    if retrieveCurrentValue('userVolume') <= 20:
        userVolAmnt = priceDict['users']['None']['amnt']
        userVolWeight = priceDict['users']['None']['weight']
    elif 20 < retrieveCurrentValue('userVolume') < 100:
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

    return itemRecords


def priceCalculations(userName, userEmail):

    selectedRecords = fetchSelectedRecords()

    printList, total = createPrintList(selectedRecords)

    return printList, total

# The following pair with IE-Invoicing-App with Anvil

@anvil.server.callable
def heroku_calls_anvil():
  return anvil.server.call("hello_from_anvil")

@anvil.server.callable  
def hello_from_heroku(name):
  return f"Hello  {name}, from Heroku!"

# The following is an email API request to Mailgun
@anvil.server.callable
def send_simple_message():
    recipient = 'sean@mondocivils.co.za'
    subject = 'Test email from Python'
    body = 'This is a test email sent from Python using Mailgun'
    
    url = 'https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN)
    
    auth = ('api', MAILGUN_API_KEY)
    
    data = {
      'from': 'Excited User <mailgun@yourdomain.com>',
      'to': [recipient], 
      'subject': subject,
      'text': body
    }

    response = requests.post(url, auth=auth, data=data)
    
    print('Status code:', response.status_code)
    print('Response:', response.text)
    
    # Process the response and return the necessary data
    return {
        "status_code": response.status_code,
        "text": response.text
    }
    # Handle the error appropriately)




