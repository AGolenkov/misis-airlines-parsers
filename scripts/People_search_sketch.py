import pymongo
import db
import pandas as pd
import fuzzy


soundex = fuzzy.Soundex(4)
i = 0
q = db.sirena.find({},{"PassengerFirstName":1,"PassengerSecondName":1,"PassengerLastName":1,
                        "PassengerFirstName_en":1,"PassengerSecondName_en":1,"PassengerLastName_en":1,
                        "PassengerFirstName_sx":1,"PassengerSecondName_sx":1,"PassengerLastName_sx":1,
                        "PaxBirthDate":1,"TravelDoc":1,"_id":0})
col = ["Index","PassengerFirstName","PassengerSecondName","PassengerLastName",
                        "PassengerFirstName_en","PassengerSecondName_en","PassengerLastName_en","PaxBirthDate", "TravelDoc","IsInBoardingData"]
df = pd.DataFrame(columns=col)
for row in q:
    row["Index"] = [i]
    IsRowFinded = False
    if row['PaxBirthDate'] != 'N/A':
        bdata = db.boarding_data.find({"PassengerFirstName":row["PassengerFirstName_en"],"PassengerLastName":row["PassengerLastName_en"],
                                    "PassengerBirthDate":row["PaxBirthDate"]},
                                    {"_id":0,"PassengerFirstName":1,"PassengerSecondName":1,"PassengerLastName":1,
                                    "PassengerDocument":1,"PassengerBirthDate":1})
        if bdata.count() != 0:
            row['IsInBoardingData'] = True
            IsRowFinded = True
        else:
            row['IsInBoardingData'] = False 
    else:
        bdata = db.boarding_data.find({"PassengerFirstName":row["PassengerFirstName_en"],"PassengerLastName":row["PassengerLastName_en"],
                                    "PassengerSecondName":row["PassengerSecondName"]},
                                    {"_id":0,"PassengerFirstName":1,"PassengerSecondName":1,"PassengerLastName":1,
                                    "PassengerDocument":1,"PassengerBirthDate":1})
        if bdata.count() != 0:
            row['IsInBoardingData'] = True
            row['PaxBirthDate'] = bdata[0]['PassengerBirthDate']
            IsRowFinded = True
        else:
            row['IsInBoardingData'] = False
    if  not IsRowFinded:
        bdata = db.boarding_data.find({"PassengerFirstName":row["PassengerFirstName_en"],"PassengerLastName":row["PassengerLastName_en"]},
                                    {"_id":0,"PassengerFirstName":1,"PassengerSecondName":1,"PassengerLastName":1,
                                    "PassengerDocument":1,"PassengerBirthDate":1})
        if bdata.count() != 0:
            row['IsInBoardingData'] = True
            row['PaxBirthDate'] = bdata[0]['PassengerBirthDate']
            IsRowFinded = True
        else:
            row['IsInBoardingData'] = False 
    if not IsRowFinded: # 
        bdata = db.boarding_data.find({"PassengerFirstName_sx":row["PassengerFirstName_sx"],"PassengerLastName_sx":row["PassengerLastName_sx"]},
                                    {"_id":0,"PassengerFirstName":1,"PassengerSecondName":1,"PassengerLastName":1,
                                    "PassengerDocument":1,"PassengerBirthDate":1})
        if bdata.count() != 0:
            row['IsInBoardingData'] = True
            row['PaxBirthDate'] = bdata[0]['PassengerBirthDate']
        else:
            row['IsInBoardingData'] = False 
            IsRowFinded = True
    df = df.append(pd.DataFrame(row, columns=col),ignore_index=True)
    i+=1
    if i==100:
        break

#s = db.boarding_data.find({"PassengerLastName":q["PassengerLastName_en"],"PassengerFirstName":q["PassengerFirstName_en"]
#                            ,"PassengerSecondName":q["PassengerSecondName_en"]})[0]
print(df)


