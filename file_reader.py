import pandas as pd
import shutil
from capture_ocr import capture_decoder
import datetime 
 

# makes a copy of the template file, reads the vessels from the data page
# and 
class Patient:
    def __init__(self):
        self.vessels_found = False
        self.patient_name = ""
        self.vs_list = []
        self.file_name = ""
        self.test_type = ""
        self.data_type = ""
        self.found_value = 0
        self.vessel_storage = [True,[None,None,None,None]]
        self.row_index = False
        self.UE_vessels = ["Upper Ex Vessels"]
        self.LE_vessels = ["Lower Ex Vessels"]
        self.viscera_vessels = ["Viscera Vessels"]
        self.skin_vessels = ["Skin Vessels"]
        self.completed_vessel_values = []
             
    def list_creator(self, file_name):
        raw_data = pd.read_excel(file_name,'Raw.donate',header=None)
        return raw_data.values.T.tolist()

    def file_looper(self):
        return_list = []
        long_list = self.list_creator(self.file_name)
        for i in range(len(long_list)):
            for j in range(len(long_list[i])):
                try:
                    print("storing vessel:" + long_list[i][j])
                    return_list.append([long_list[i][j],[i,j]])
                except TypeError:
                    pass
        for i in range(len(return_list)):
            for index, vessels in enumerate(return_list):
                if vessels[1][1] == i:

                    return_list[index].append([None,None,None,None])    
        return return_list
        
    def file_reader(self):
        #patient_name = "Nicole_Davidson"
        date=datetime.datetime.now().strftime("%d-%m-%y_%I-%M")
        self.file_name='output/'+self.patient_name+"_"+self.test_type+"_"+date+'.xlsx'
        print(self.test_type)
        if self.test_type == "Food":
            shutil.copyfile('excel/Food.xlsx', self.file_name)
        else:
            shutil.copyfile('excel/NVI.xlsx', self.file_name)
        self.vs_list = self.file_looper()  

    def file_writer(self):
        long_list = self.list_creator(self.file_name)
        print(self.vs_list)
        for items in self.vs_list:
            if self.test_type == "NVI":
                if items[1][1] == 0:
                    long_list[items[1][0]][items[1][1]+2] = items[2][0]         # PI Upper
                    long_list[items[1][0]+1][items[1][1]+2] = items[2][2]       # VF Upper
                    long_list[items[1][0]][items[1][1]+3] = items[2][1]         # PI Lower
                    long_list[items[1][0]+1][items[1][1]+3] = items[2][3]       # VF Lower
                else:
                    long_list[items[1][0]][items[1][1]+1] = items[2][0]         # PI Upper
                    long_list[items[1][0]+1][items[1][1]+1] = items[2][2]       # VF Upper
                    long_list[items[1][0]][items[1][1]+2] = items[2][1]         # PI Lower
                    long_list[items[1][0]+1][items[1][1]+2] = items[2][3]       # VF Lower
            else:
                long_list[items[1][0]][items[1][1]+1] = items[2][0]         # PI Upper
                long_list[items[1][0]+1][items[1][1]+1] = items[2][2]       # VF Upper
                long_list[items[1][0]][items[1][1]+2] = items[2][1]         # PI Lower
                long_list[items[1][0]+1][items[1][1]+2] = items[2][3]       # VF Lower
        df = pd.DataFrame(long_list)
        df = df.T
 
        b4_time = datetime.datetime.now()
     
        with pd.ExcelWriter(self.file_name, engine='openpyxl', mode='a',if_sheet_exists='replace') as writer: #
            df.to_excel(writer,'Raw.donate',startrow=0, index=False, header=False)

        cur_time = datetime.datetime.now()
        print(cur_time.strftime("%I:%M:%S"))
        print("time to compute",cur_time-b4_time)
        return True

    def vessel_list_iterator(self):
        for items in self.vs_list:
            for i in range(len(self.vs_list)):
                if items[1][1] == i:
                    if items[2][0] is None:
                        print(i)
                        self.vessel_storage = [items[0],items[2]]
                        self.row_index = i
                        return True
        self.vessel_storage = ["Test Complete", [None,None,None,None]]            

    def index(self):
        '''
            checks the list of values for the 
            values of the vessel (if any),
            and returns them to the main display
        '''
        if self.vessel_storage[0] is True:
            try:
                for items in self.vs_list:
                        if items[1][1] == self.row_index:
                            if items[2][0] is None:
                                self.vessel_storage = [items[0],items[2]]
                                return self.vessel_storage
                self.vessel_list_iterator()
            except:
                if self.row_index is False:
                    self.vessel_list_iterator()
        return self.vessel_storage
        
    def value_hunter(self):
        found_value = capture_decoder()
        self.data_type = found_value[0]
        self.found_value = found_value[1]
        return found_value[1]
    
    def value_holder(self):
        if self.data_type == "PI":
            if self.vessel_storage[1][0] is None:
                self.vessel_storage[1][0] = self.found_value
            elif self.vessel_storage[1][1] is None:
                self.vessel_storage[1][1] = self.found_value
        elif self.data_type == "VF":
            if self.vessel_storage[1][2] is None:
                self.vessel_storage[1][2] = self.found_value
            elif self.vessel_storage[1][3] is None:
                self.vessel_storage[1][3] = self.found_value

        # TODO, SWITCH TO PAGE ACKNOWLEDGING COMPLETETION               
        return self.completion_checker()

    def completion_checker(self):
        for value in self.vessel_storage[1]:
            if value is None:
                #print("not done")
                return False 
        for index, items in enumerate(self.vs_list):
            if items[0] == self.vessel_storage[0]:
                self.vs_list[index][2] = self.vessel_storage[1]
                self.completed_vessel_values.append(self.vessel_storage)
                self.vessel_storage = [True, [None,None,None,None]]
                return True
        print("The vessel name does not match any stored values.")
        print("This most likely means the test is complete.")
        return False
        
    def deletion(self):
        self.vessel_storage[1] = [None, None, None, None] 
        for index, vessel in enumerate(self.vs_list):
            if vessel[0] == self.vessel_storage[0]:
                self.vs_list[index][2] == self.vessel_storage[1]
                return True
    
    def vessel_finder(self):
        if self.vessels_found is False:
            if self.test_type == "Food":
                    self.UE_vessels = ["Pre Vessels"]
                    self.LE_vessels = ["Post Vessels"]
                    self.viscera_vessels = ["Pre Vessels"]
                    self.skin_vessels = ["Post Vessels"]
            for items in self.vs_list:
                vessel_name = items[0]
                column_num = items[1][1] 
                print(items)
                if self.test_type == "Food":

                    if column_num == 0:
                        self.UE_vessels.append(vessel_name)
                    elif column_num == 5:
                        self.LE_vessels.append(vessel_name)
                    else: 
                        print(vessel_name, "failed at", column_num)
                else:
                    if (column_num == 0) or (column_num == 5):
                        self.UE_vessels.append(vessel_name)
                    
                    elif (column_num == 10) or (column_num == 15):
                        self.LE_vessels.append(vessel_name)
                    
                    elif items[1][1] == 20:
                        self.skin_vessels.append(vessel_name)

                    elif (column_num == 26) or (column_num == 31):
                        self.viscera_vessels.append(vessel_name)
                
                    
        return[self.UE_vessels, self.LE_vessels, self.viscera_vessels, self.skin_vessels]

    def vessel_confirm(self, vessel_i):
        for value in self.vs_list:
            if value[0] == vessel_i:
                print("old", self.vessel_storage)
                self.vessel_storage = [value[0],value[2]]
                print("new", self.vessel_storage)
                # STORE THE PREVIOUSLY HELD VALUE ?
                break

    def monophasic_values(self):
        self.vessel_storage[1][1] = 1
        self.vessel_storage[1][3] =.01