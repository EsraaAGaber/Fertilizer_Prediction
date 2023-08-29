import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from firebase_admin import credentials ,initialize_app,db
cred=credentials.Certificate("fertilizer-predictor-firebase-adminsdk-3uwde-e28aca2d91.json")
app=initialize_app(cred,{
    'databaseURL':'https://fertilizer-predictor-default-rtdb.firebaseio.com/'
})
ref=db.reference("/fertilizer/")



'''set the data 
k=int(input('k= '))
n=int(input('n= '))
p=int(input('p= '))
crop=input('crop= ')
h=int(input('humidity= '))
m=int(input('moisture= '))
ph=int(input('ph= '))
soil=input('soil= ')
t=int(input('temperture= '))
new_data={
    'K': k, 'N': n, 'P': p, 'crop': crop, 'humidity': h, 'moisture': m, 'soil': soil, 'temperature': t,'ph':ph
}


ref.update(new_data)'''
'''get  data'''
data=ref.get()
print(data)


'''end setting '''

'''model'''
dataset =pd.read_csv('Fertilizer Prediction.csv')
print(dataset['Crop Type'].unique())

x = dataset[['Temparature', 'Humidity ', 'Moisture', 'Soil Type', 'Crop Type', 'Nitrogen', 'Potassium', 'Phosphorous']]
y = dataset['Fertilizer Name']
x_encoded = pd.get_dummies(x)
x_train, x_test, y_train, y_test = train_test_split(x_encoded, y, test_size=0.4,random_state=42)

model =RandomForestClassifier(random_state=42)
sns.countplot(x="Soil Type",data=dataset)
model.fit(x_train, y_train)
print (x)
y_pred = model.predict(x_test)

accuracy = accuracy_score(y_test, y_pred)
print("accuracy = {:.2f}%".format(accuracy*100))


'''dic for values in dataset'''

soil_type ={'Sandy':1,'Loamy': 2, 'Black':3 ,'Red':4, 'Clayey':5}
crop_type={'Maize':1 ,'Sugarcane':2,'Cotton': 3,'Tobacco':4 ,'Paddy':5 ,'Barley':6 ,'Wheat':7 ,'Millets':8 
,'Oil seeds':9 ,'Pulses':10  ,'Ground Nuts':11}



'''add new wanted values 

new_sample= [[t,h,m,soil_type.get(soil),crop_type.get(crop),n,p,ph]]'''
new_sample=[[data['temperature'],data['humidity'],data['moisture'],soil_type.get(data['soil']),crop_type.get(data['crop']),data['N'],data['K'],data['P']]]

new_sample_encoded=pd.get_dummies(pd.DataFrame(new_sample,columns=x.columns))

new_sample_pred=model.predict(new_sample_encoded)
output={
'fertilizer':new_sample_pred[0]   
}
fertilizer_ref=db.reference("/fertilizer")
fertilizer_ref.update(output)
print("The best fertilizer to use is  ", new_sample_pred)



