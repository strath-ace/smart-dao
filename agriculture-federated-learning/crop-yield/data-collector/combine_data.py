import pandas as pd
import os
import numpy as np
import json
import hashlib

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output


load_xl = True



this_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists(this_dir+"/output_data"):
    os.makedirs(this_dir+"/output_data")



# Get files
sheet_to_df_map = []
jsons_roots = []
for root, dirs, files in os.walk(this_dir+"/input_data_country"):
    for name in files:
        if name[-5:] == ".xlsx":
            sheet_to_df_map.append(pd.read_excel(os.path.join(root, name), sheet_name=None))
        if name[-8:] == ".geojson":
            jsons_roots.append(os.path.join(root, name))


############ Excel Loader ############
if load_xl:
    # Check if documents are same size for number of crops
    for i in range(len(sheet_to_df_map)-1):
        if len(sheet_to_df_map[i].keys()) != len(sheet_to_df_map[i+1].keys()):
            raise Exception("XLSX files not same size (Number of crops)")

    for j in range(1,len(sheet_to_df_map[0].keys())-1):
    # for j in range(5,6):
        all_dates = []
        all_yielder = []
        for i in range(len(sheet_to_df_map)):
            # print("Sheet "+str(j))
            # print(sheet_to_df_map[i]["Sheet "+str(j)])
            namer = "".join(list(sheet_to_df_map[i]["Sheet "+str(j)].iloc[4][2]))
            # print(namer)
            namer2 = ("".join(list(sheet_to_df_map[i]["Sheet "+str(j)].iloc[5][2])))[:4]
            # print(namer)
            new_header = list(sheet_to_df_map[i]["Sheet "+str(j)].iloc[7])
            sheet_to_df_map[i]["Sheet "+str(j)] = sheet_to_df_map[i]["Sheet "+str(j)][9:47] # 447 for nuts 2 - 47 for country
            sheet_to_df_map[i]["Sheet "+str(j)].columns = new_header
            # print(sheet_to_df_map[i]["Sheet "+str(j)])

            regions = sheet_to_df_map[i]["Sheet "+str(j)]["TIME"].to_numpy()
            # print(regions)

            new_df = sheet_to_df_map[i]["Sheet "+str(j)].drop("TIME", axis='columns')
            # print(new_df.columns)
            for k in range(0,len(new_df.columns),2):
                date = new_df.columns[k]
                yielder = new_df[new_df.columns[k]].to_numpy()
                try:
                    remover = new_df[new_df.columns[k+1]].notnull().to_numpy()
                    yielder[remover] = ":"
                except:
                    pass

                all_dates.append(date)
                all_yielder.append(yielder)

        indx = np.argsort(all_dates)
        all_dates = np.array(all_dates)[indx]
        all_yielder = np.array(all_yielder)[indx]

        out_df = pd.DataFrame(np.swapaxes(all_yielder,0,1), columns=all_dates, index=regions)

        # if float(int(j/2)) == float(j/2):
        #     save_name = "yield_"
        # hashlib.sha256(b"").hexdigest()
        try:
            out_df.to_csv(this_dir+"/output_data_country/"+namer2+"_"+namer+".csv")
        except:
            pass












# regions_only = sheet_to_df_map[0]["Sheet 1"].iloc[9:449,0].to_numpy()

# time = []
# regions_new = []

# nuts_years = [2003,2006,2010,2013,2016,2021]
# for regions in regions_only:
#     if "Extra-Regio NUTS 2" not in regions:
#         found = False
#         for nuts in nuts_years:
#             if "(NUTS "+str(nuts)+")" in regions:
#                 regions_new.append(regions.replace("(NUTS "+str(nuts)+")", "").strip())
#                 time.append(nuts)
#                 found = True
#                 break
#             if "(statistical region "+str(nuts)+")" in regions:
#                 regions_new.append(regions.replace("(statistical region "+str(nuts)+")", "").strip())
#                 time.append(nuts)
#                 found = True
#                 break
#         if not found:
#             regions_new.append(regions.strip())
#             time.append(9999)


# # for i in range(len(regions_new)):
# #     print(regions_new[i], "\t\t\t", time[i])

# regions2 = regions_new.copy()

# numbers = []
# for i in jsons_roots:
#     numbers.append(i[-17:-13])
# indx = np.flip(np.argsort(numbers))
# jsons_roots = np.array(jsons_roots)[indx]
# numbers = np.array(numbers)[indx]

# pos2 = []
# for i in range(len(regions_new)):
#     pos2.append([])


# for k, js in enumerate(jsons_roots):
#     print(k)
#     js_data = load_json(js)["features"]
#     js_names = []
#     pos = []
#     for i in range(len(js_data)):
#         if js_data[i]["properties"]["LEVL_CODE"] == 2:
#             try:
#                 js_names.append(js_data[i]["properties"]["NAME_LATN"])
#                 pos.append(i)
#             except:
#                 js_names.append(js_data[i]["properties"]["NUTS_NAME"])
#                 pos.append(i)
#     # print(js_names)

    
#     for j, name in enumerate(js_names):
#         if name == "Mardin":
#             print(name, [int(numbers[k]), pos[j]])
#         if name == "Batman":
#             print(name, [int(numbers[k]), pos[j]])
#         for ii in range(len(regions_new)):
#             if int(numbers[k]) <= int(time[j]):
#                 if name in regions_new[ii]:
#                     pos2[ii].append([int(numbers[k]), pos[j]])
#                     # print(regions_new[ii])
#                     regions_new[ii] = regions_new[ii].replace(name, " ")
#                     # print(regions_new[ii])
#                     break

    

# # print(np.array(regions_new))
# # print(pos2)

# # for x in zip(regions2, regions_new, pos2):
# #     print(x)

