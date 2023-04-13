from flask import Flask, render_template, request
from file_reader import Patient
import logging
from capture_ocr import find_all
app = Flask(__name__)

def index_call(end=False):
    if end == False:
        value = patient_instance.value_hunter()
        value_name = patient_instance.data_type
        selected_vessel = patient_instance.index()
        return render_template("index.html", 
                                selected_vessel = selected_vessel[0],
                                name = patient_instance.patient_name, 
                                num = value_name + ": " + value, 
                                test = patient_instance.test_type,
                                current_vessel_values = selected_vessel[1])
    return render_template("index.html", 
                                selected_vessel =  "None",
                                name = patient_instance.patient_name, 
                                num = "None" + ": " + "None", 
                                test = "Completed",
                                current_vessel_values = "None")
def vessel_setter():
    # ue = ["Upper Extremity Pre"]
    # le = ["Lower Extremity Pre"]
    # viscera = ["Upper Extremity Post"]
    # skin = ["Lower Extremity Post"]
    # for vessel in food.vessels_for_food_test:
    #     if vessel in patient_instance.UE_vessels:
    #         ue.append(vessel)
    #     elif vessel in patient_instance.LE_vessels:
    #         le.append(vessel)
    #     elif vessel[5:] in patient_instance.UE_vessels:
    #         viscera.append(vessel)
    #     elif vessel[5:] in patient_instance.LE_vessels:
    #         skin.append(vessel)
    return("ue","le","viscera","skin")
                 
@app.route('/', methods=['POST','GET'])
def home():
    patient_instance.__init__()
    # food.__init__()
    # nvi.__init__()
    return render_template('home.html')

# @app.route('/home', methods=['POST','GET'])
# def althome():
#     # patient_instance.__init__()
#     # food.__init__()
#     # nvi.__init__()
#     return render_template('home.html')

@app.route('/landing/', methods=['POST','GET'])
def first_tasks():    
    patient_instance.test_type = request.form.get("test")
    patient_instance.patient_name = request.form.get("fname")
    patient_instance.file_reader()
    return(index_call())
         
@app.route('/update_vessel', methods=['POST','GET'])
def change_current_vessel():  
    # if patient_instance.test_type == "Food":
    #     vessel_list = vessel_setter()
    # else:
        # ["no","no","no","no"]#
    vessel_list = patient_instance.vessel_finder()   #[patient_instance.UE_vessels, patient_instance.LE_vessels, \
        #     patient_instance.viscera_vessels, patient_instance.skin_vessels]

    return render_template("vessel.html",
                            name=patient_instance.patient_name,
                            #finished_vessel_values=patient_instance.completed_vessel_values,
                            UE_vessels = vessel_list[0],
                            LE_vessels = vessel_list[1],
                            viscera_vessels = vessel_list[2],
                            skin_vessels = vessel_list[3])
                            
@app.route('/confirm_vessel', methods=['POST','GET'])
def confirm_vessel():
    
    ves_one = request.form.get("uevessel")
    ves_two = request.form.get("levessel")
    ves_three = request.form.get("visvessel")
    ves_four = request.form.get("skinvessel")
    if ves_one is not None:
        vessel_i = ves_one
    elif ves_two is not None:
        vessel_i = ves_two
    elif ves_three is not None:
        vessel_i = ves_three
    elif ves_four is not None:
        vessel_i = ves_four
    # if patient_instance.test_type == "Food":
    #     for numbs, name in enumerate(patient_instance.vessels_for_food_test):
    #         if name == vessel_i:
    #             patient_instance.food_test_values[patient_instance.vessel_name_index][1] = patient_instance.vessel_value_holder[1]
    #             patient_instance.vessel_name_index = numbs
    #             patient_instance.vessel_value_holder = patient_instance.food_test_values[patient_instance.vessel_name_index]
    #             return(index_call())
    patient_instance.vessel_confirm(vessel_i)
        
    return(index_call())

@app.route('/confirm_data/', methods=['POST'])
def confirm_data_response():
    response = patient_instance.value_holder() 
    #if response is False:
        
    return(index_call())

@app.route('/read_data/', methods=['POST', 'GET'])
def read_data_response():
    return(index_call())


@app.route('/monophasic_form', methods=['POST', 'GET'])  
def monophasic():
    response = patient_instance.monophasic_values()
    # if response is not None:
    #     done = converter_store()    
    #     if done is not None:
    #         return(index_call(True))
    return(index_call())

@app.route('/view_data', methods=['POST','GET'])
def view_data():
    if patient_instance.patient_name == "":
        patient_instance.patient_name = request.form.get("fname")
    return render_template("rawdata.html", 
                            name = patient_instance.patient_name, 
                            micro_vessel_results = patient_instance.completed_vessel_values
                            )

@app.route('/results/', methods=['GET','POST'])
def results():
    post_val = []
    if patient_instance.test_type == "NVI":
       pass

    elif patient_instance.test_type == "Food":
        pass

    return render_template("results.html", 
                            macro_vessel_values = post_val, 
                            name=patient_instance.patient_name)

@app.route('/print_data/', methods=['GET','POST'])
def print_data():
    completed = patient_instance.file_writer()
    if completed is True:
        success = ""
    else:
        success = "not "
    success += "successful"
    return render_template("print_result.html", 
                            name=patient_instance.patient_name,
                            success=success)

@app.route('/delete_last', methods=['GET','POST'])
def delete_recent():
    vals_to_show = find_all()
    post_vals = ["All Found Numbers"]
    for rows in vals_to_show.split("\n"):
        for data in rows.split(" "):
            try:
                if float(data) != 0:
                    post_vals.append(data)
            except:
                print(data)
    selected_vessel = patient_instance.vessel_storage
    return(render_template("deletion_page.html",
                            selected_vessel = selected_vessel[0],
                            potential_vals = post_vals,
                            #vessels = patient_instance.vessel_storage[1],
                            current_vessel_values = selected_vessel[1]))    

@app.route('/confirm_value/', methods=['POST', 'GET'])
def confirm_value():
    to_iterate = [0,2,1,3]
    value_to_save = request.form.get("new_value")
    for index in range(4):
        value = patient_instance.vessel_value_holder[1][to_iterate[index]]
        if value is None:
            patient_instance.vessel_value_holder[1][to_iterate[index]]=value_to_save
            break
    print("values",value)
    response = patient_instance.completed_vessel_actions()
    if response is None:
        return(index_call())
    #done = converter_store(response)    
    index_val = False
    #if done is not None:
    #    index_val = True
    return(index_call(index_val))
    

@app.route('/confirm_delete', methods=['GET','POST'])
def confirm_and_return():
    deletion_attempt = patient_instance.deletion()
    return(index_call())
    

if __name__ == '__main__':
    logging.basicConfig(filename="debug.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
    logger = logging.getLogger()
    # Setting the threshold of logger to DEBUG
    patient_instance = Patient()
    logger.setLevel(logging.DEBUG)
    app.run(host='0.0.0.0', debug = True, use_reloader=False)