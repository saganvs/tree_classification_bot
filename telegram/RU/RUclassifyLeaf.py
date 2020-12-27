import pickle
import numpy as np
import pandas as pd

def classify(data, model_name):
    data = data.drop(['Mode','Vertical_symmetry','Horizontal_symmetry', 'Minimal_peak'], axis=1)
    mms = pd.read_pickle('RUmms.p',compression='infer')
    example = data.iloc[0:1,0:data.shape[1]]
    mms = pd.concat([mms,example],ignore_index=True)
    example_scaled = ((mms-mms.min())/(mms.max()-mms.min())).loc[2:2,]

    ### загрузка модели
    filename = f'RUmodel_{model_name}.sav'
    loaded_model = pickle.load(open(filename, 'rb'))    
    
    ### загрузка названий классов
    filehandler = open('./RUclasses.obj', 'rb') 
    classes = pickle.load(filehandler)
    result1 = loaded_model.predict(example_scaled)[0]
    return result1