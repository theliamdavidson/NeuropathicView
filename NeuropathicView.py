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
                 
@app.route('/', methods=['POST','GET'])
def home():
    patient_instance.__init__()
    return render_template('home.html')

@app.route('/landing/', methods=['POST','GET'])
def first_tasks():    
    patient_instance.test_type = request.form.get("test")
    patient_instance.patient_name = request.form.get("fname")
    patient_instance.file_reader()
    return(index_call())
         
@app.route('/update_vessel', methods=['POST','GET'])
def change_current_vessel():  
    vessel_list = patient_instance.vessel_finder()  
    return render_template("vessel.html",
                            name=patient_instance.patient_name,
                            LeftLower = vessel_list[0],
                            RightLower = vessel_list[1],
                            RightUpper = vessel_list[2],
                            LeftUpper = vessel_list[3],
                            Viscera = vessel_list[4],
                            MISC = vessel_list[5])
                            
@app.route('/confirm_vessel', methods=['POST','GET'])
def confirm_vessel(): 
    ves_one = request.form.get("LeftLower")
    ves_two = request.form.get("RightLower")
    ves_three = request.form.get("RightUpper")
    ves_four = request.form.get("LeftUpper")
    ves_five = request.form.get("Viscera")
    ves_six = request.form.get("MISC")
    for var in [ves_one, ves_two, ves_three, ves_four, ves_five, ves_six]:
        if var is not None:
            vessel_i = var
            break
    patient_instance.vessel_confirm(vessel_i)
    return(index_call())

@app.route('/confirm_data/', methods=['POST'])
def confirm_data_response():
    response = patient_instance.value_holder()         
    return(index_call())

@app.route('/read_data/', methods=['POST', 'GET'])
def read_data_response():
    return(index_call())

@app.route('/monophasic_form', methods=['POST', 'GET'])  
def monophasic():
    response = patient_instance.monophasic_values()
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
    return render_template("results.html", 
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
                pass
    selected_vessel = patient_instance.vessel_storage
    return(render_template("deletion_page.html",
                            selected_vessel = selected_vessel[0],
                            potential_vals = post_vals,
                            current_vessel_values = selected_vessel[1]))    

@app.route('/confirm_value/', methods=['POST', 'GET'])
def confirm_value():
    to_iterate = [0,2,1,3]
    value_to_save = request.form.get("new_value")
    for index in range(4):
        value = patient_instance.vessel_storage[1][to_iterate[index]]
        if value is None:
            patient_instance. vessel_storage[1][to_iterate[index]]=value_to_save
            break
    response = patient_instance.completion_checker()
    if response is None:
        return(index_call())
    index_val = False
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