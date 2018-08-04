import pickle
test = [55, 1, 14.1, 7.6, 750, 35, 63, 5.0, 1.6, 0.47]
load_model = pickle.load(open('final_model.sav','rb'))
result = load_model.predict([test])
print(result)
