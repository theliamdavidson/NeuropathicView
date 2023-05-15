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
        self.previous_vessel = None
        self.col_index = False
        self.completed_vessel_values = []
        self.row_index = 0
        self.indexed_list = 0
             
    def list_creator(self, file_name):
        raw_data = pd.read_excel(file_name,'Raw.donate',header=None)
        return raw_data.values.T.tolist()
    
    def data_cleaner(self, long_list):
        for nums in range(len(long_list[1])):
            if long_list[1][nums] == "Left LE":
                return nums
        return False

    def file_looper(self):
        return_list = []
        long_list = self.list_creator(self.file_name)
        iterable = self.data_cleaner(long_list)
        for row_index in range(3, len(long_list)):
            for col_index in range(iterable, len(long_list[row_index])):
                if isinstance(long_list[row_index][col_index], str):
                    return_list.append([long_list[row_index][col_index],[row_index,col_index],[None,None,None,None]])
        return_list.sort(key=lambda x: x[1][1]) # sort by the second element of each key
        return return_list
        
    def file_reader(self):
        date=datetime.datetime.now().strftime("%d-%m-%y_%I-%M")
        self.file_name='output/'+self.patient_name+"_"+self.test_type+"_"+date+'.xlsx'
        if self.test_type == "Food":
            shutil.copyfile('excel/Food.xlsx', self.file_name)
        else:
            shutil.copyfile('excel/NVI.xlsx', self.file_name)
        self.vs_list = self.file_looper()  

    def printing_loop(self, long_list, items):
        counter = 0
        while counter <= 1:
            for rows, rowlist in enumerate(long_list):
                for cols, values in enumerate(rowlist):
                    if values == items[0]:
                        if (self.test_type == "NVI") and (items[1][1] == 0):
                            long_list[rows][cols+2] = items[2][0]         # PI Upper
                            long_list[rows+1][cols+2] = items[2][2]       # VF Upper
                            long_list[rows][cols+3] = items[2][1]         # PI Lower
                            long_list[rows+1][cols+3] = items[2][3]       # VF Lower
                        else:
                            long_list[rows][cols+1] = items[2][0]         # PI Upper
                            long_list[rows+1][cols+1] = items[2][2]       # VF Upper
                            long_list[rows][cols+2] = items[2][1]         # PI Lower
                            long_list[rows+1][cols+2] = items[2][3]       # VF Lower
                        counter +=1
        return long_list     

    def file_writer(self):
        long_list = self.list_creator(self.file_name)

        for items in self.vs_list:
            if items[2][0] is not None:
                try:
                    long_list = self.printing_loop(long_list, items)
                except:
                    return False
        df = pd.DataFrame(long_list)
        df = df.T
        # transpose the matrix back the correct way
 
        b4_time = datetime.datetime.now()
     
        with pd.ExcelWriter(self.file_name, engine='openpyxl', mode='a',if_sheet_exists='overlay') as writer: #
            df.to_excel(writer,'Raw.donate',startrow=0, index=False, header=False)

        cur_time = datetime.datetime.now()
        print(cur_time.strftime("%I:%M:%S"))
        print("time to compute",cur_time-b4_time)
        return True

    def vessel_list_iterator(self):
        for i in range(self.indexed_list, len(self.vs_list)):
            if self.vs_list[i][2][0] is None:
                self.vessel_storage = [self.vs_list[i][0],self.vs_list[i][2]]
                self.col_index = self.vs_list[i][1][1]
                self.indexed_list = i
                return True
            
            # slightly obtuse way to check completion above and below the starting point
            # allows for irratic changes by the user

        for i in range(self.indexed_list):
            if self.vs_list[i][2][0] is None:
                self.vessel_storage = [self.vs_list[i][0],self.vs_list[i][2]]
                self.col_index = self.vs_list[i][1][1]
                self.indexed_list = i
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
                for i in range(self.indexed_list,len(self.vs_list)):
                    if self.vs_list[i][2][0] is None:
                        self.vessel_storage = [self.vs_list[i][0],self.vs_list[i][2]]
                        return self.vessel_storage
                self.vessel_list_iterator()
            except:
                if self.col_index is False:
                    self.vessel_list_iterator()
        return self.vessel_storage
    
    def decimal_wizard(self, found_value):
        '''
            str -> str;
            this function corrects for the common case where  
            OCR does not decect the decimal point in a value
        '''
        try:
            if int(found_value[1]) > 999:
                found_value = found_value[1][:2] + '.' + found_value[1][2:]
                #--------------------------------------------------------------
                return found_value
            elif int(found_value[1]) > 99:
                found_value = found_value[1][:1] + '.' + found_value[1][1:]
                #--------------------------------------------------------------
                return found_value
        except ValueError:
            pass    
        return found_value[1]
        
    def value_hunter(self):
        found_value = capture_decoder()
        self.data_type = found_value[0]
        if self.data_type == "PI":
            value_str = str(found_value)
            if '.' not in value_str:
                self.found_value = self.decimal_wizard(found_value)
        else:
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
        return self.completion_checker()

    def completion_checker(self):
        for value in self.vessel_storage[1]:
            if value is None:
                return False 
        for index, items in enumerate(self.vs_list):
            if items[0] == self.vessel_storage[0]:
                self.vs_list[index][2] = self.vessel_storage[1]
                self.completed_vessel_values.append(self.vessel_storage)
                self.previous_vessel = [self.vessel_storage[0], index]
                self.vessel_storage = [True, [None,None,None,None]]
                return True
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
                vessel_col_iter = ["Pre Vessels", "Post Vessels", "Pre Vessels", "Post Vessels"]
            else: 
                vessel_col_iter =["Left Lower Ex Vessels", "Right Lower Ex Vessels", "Right Upper Ex Vessels", "Left Upper Ex Vessels", "Viscera Vessels", "MISC", ""]

            sorted_values = []
            for items in self.vs_list:
                vessel_name = items[0]
                row_num = items[1][1] 
                sorted_values.append([vessel_name, row_num])
            #sorted_values.sort(key=lambda x: x[1]) # potentially uneccessary; is on the chopping block
            list_of_lists = []
            current_key = sorted_values[0][1]
            counter = 0
            current_list = []
            current_list.append(vessel_col_iter[counter])
            current_list.append(sorted_values[0][0])
            
            # Iterate through the sorted list and add each sublist to the appropriate list
            for sublist in sorted_values[1:]:
                if sublist[1] != current_key:
                    list_of_lists.append(current_list)
                    current_list = []
                    counter+=1
                    current_list.append(vessel_col_iter[counter])
                    current_list.append(sublist[0])
                    current_key = sublist[1]
                    
                else:
                    current_list.append(sublist[0])
            list_of_lists.append(current_list)
        return list_of_lists

    def vessel_confirm(self, vessel_i):
        for index, value in enumerate(self.vs_list):
            if value[0] == vessel_i:
                self.indexed_list = index
                self.col_index = value[1][1]
                self.vessel_storage = [value[0],value[2]]
                break

    def monophasic_values(self):
        self.vessel_storage[1][1] = 1
        self.vessel_storage[1][3] =.01


if __name__ == "__main__":
    p = Patient()
    p.patient_name = "Nicole Davidson"
    p.test_type = "NVI"
    p.file_reader()
    print(p.vessel_finder())
    print(len(p.vs_list))
    print(p.vs_list)
