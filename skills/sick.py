import pandas as pd
import re
import numpy as np
from joblib import load
import speech_recognition as sr
import sys

sys.path.append("/home/leah/Documents/leah-final-hindi/tools")

from tools import mpg123_player

symptoms_dict = {
    'itching': 'itching',
    'skin rash': 'skin_rash',
    'nodal skin eruptions': 'nodal_skin_eruptions',
    'continuous sneezing': 'continuous_sneezing',
    'shivering': 'shivering',
    'chills': 'chills',
    'joint pain': 'joint_pain',
    'stomach pain': 'stomach_pain',
    'acidity': 'acidity',
    'ulcers on tongue': 'ulcers_on_tongue',
    'muscle wasting': 'muscle_wasting',
    'vomiting': 'vomiting',
    'burning micturition': 'burning_micturition',
    'spotting urination': 'spotting_urination',
    'fatigue': 'fatigue',
    'weight gain': 'weight_gain',
    'anxiety': 'anxiety',
    'cold hands and feets': 'cold_hands_and_feets',
    'mood swings': 'mood_swings',
    'weight loss': 'weight_loss',
    'restlessness': 'restlessness',
    'lethargy': 'lethargy',
    'patches in throat': 'patches_in_throat',
    'irregular sugar level': 'irregular_sugar_level',
    'cough': 'cough',
    'high fever': 'high_fever',
    'sunken eyes': 'sunken_eyes',
    'breathlessness': 'breathlessness',
    'sweating': 'sweating',
    'dehydration': 'dehydration',
    'indigestion': 'indigestion',
    'headache': 'headache',
    'yellowish skin': 'yellowish_skin',
    'dark urine': 'dark_urine',
    'nausea': 'nausea',
    'loss of appetite': 'loss_of_appetite',
    'pain behind the eyes': 'pain_behind_the_eyes',
    'back pain': 'back_pain',
    'constipation': 'constipation',
    'abdominal pain': 'abdominal_pain',
    'diarrhoea': 'diarrhoea',
    'mild fever': 'mild_fever',
    'yellow urine': 'yellow_urine',
    'yellowing of eyes': 'yellowing_of_eyes',
    'acute liver failure': 'acute_liver_failure',
    'fluid overload': 'fluid_overload',
    'swelling of stomach': 'swelling_of_stomach',
    'swelled lymph nodes': 'swelled_lymph_nodes',
    'malaise': 'malaise',
    'blurred and distorted vision': 'blurred_and_distorted_vision',
    'phlegm': 'phlegm',
    'throat irritation': 'throat_irritation',
    'redness of eyes': 'redness_of_eyes',
    'sinus pressure': 'sinus_pressure',
    'runny nose': 'runny_nose',
    'congestion': 'congestion',
    'chest pain': 'chest_pain',
    'weakness in limbs': 'weakness_in_limbs',
    'fast heart rate': 'fast_heart_rate',
    'pain during bowel movements': 'pain_during_bowel_movements',
    'pain in anal region': 'pain_in_anal_region',
    'bloody stool': 'bloody_stool',
    'irritation in anus': 'irritation_in_anus',
    'neck pain': 'neck_pain',
    'dizziness': 'dizziness',
    'cramps': 'cramps',
    'bruising': 'bruising',
    'obesity': 'obesity',
    'swollen legs': 'swollen_legs',
    'swollen blood vessels': 'swollen_blood_vessels',
    'puffy face and eyes': 'puffy_face_and_eyes',
    'enlarged thyroid': 'enlarged_thyroid',
    'brittle nails': 'brittle_nails',
    'swollen extremeties': 'swollen_extremeties',
    'excessive hunger': 'excessive_hunger',
    'extra marital contacts': 'extra_marital_contacts',
    'drying and tingling lips': 'drying_and_tingling_lips',
    'slurred speech': 'slurred_speech',
    'knee pain': 'knee_pain',
    'hip joint pain': 'hip_joint_pain',
    'muscle weakness': 'muscle_weakness',
    'stiff neck': 'stiff_neck',
    'swelling joints': 'swelling_joints',
    'movement stiffness': 'movement_stiffness',
    'spinning movements': 'spinning_movements',
    'loss of balance': 'loss_of_balance',
    'unsteadiness': 'unsteadiness',
    'weakness of one body side': 'weakness_of_one_body_side',
    'loss of smell': 'loss_of_smell',
    'bladder discomfort': 'bladder_discomfort',
    'foul smell of urine': 'foul_smell_of_urine',
    'continuous feel of urine': 'continuous_feel_of_urine',
    'passage of gases': 'passage_of_gases',
    'internal itching': 'internal_itching',
    'toxic look (typhos)': 'toxic_look_(typhos)',
    'depression': 'depression',
    'irritability': 'irritability',
    'muscle pain': 'muscle_pain',
    'altered sensorium': 'altered_sensorium',
    'red spots over body': 'red_spots_over_body',
    'belly pain': 'belly_pain',
    'abnormal menstruation': 'abnormal_menstruation',
    'dischromic patches': 'dischromic_patches',
    'watering from eyes': 'watering_from_eyes',
    'increased appetite': 'increased_appetite',
    'polyuria': 'polyuria',
    'family history': 'family_history',
    'mucoid sputum': 'mucoid_sputum',
    'rusty sputum': 'rusty_sputum',
    'lack of concentration': 'lack_of_concentration',
    'visual disturbances': 'visual_disturbances',
    'receiving blood transfusion': 'receiving_blood_transfusion',
    'receiving unsterile injections': 'receiving_unsterile_injections',
    'coma': 'coma',
    'stomach bleeding': 'stomach_bleeding',
    'distention of abdomen': 'distention_of_abdomen',
    'history of alcohol consumption': 'history_of_alcohol_consumption',
    'fluid overload.1': 'fluid_overload.1',
    'blood in sputum': 'blood_in_sputum',
    'prominent veins on calf': 'prominent_veins_on_calf',
    'palpitations': 'palpitations',
    'painful walking': 'painful_walking',
    'pus filled pimples': 'pus_filled_pimples',
    'blackheads': 'blackheads',
    'scurring': 'scurring',
    'skin peeling': 'skin_peeling',
    'silver like dusting': 'silver_like_dusting',
    'small dents in nails': 'small_dents_in_nails',
    'inflammatory nails': 'inflammatory_nails',
    'blister': 'blister',
    'red sore around nose': 'red_sore_around_nose',
    'yellow crust ooze': 'yellow_crust_ooze'
}

def extract_symptoms(input_text):
    # Define the list of symptoms
    symptoms = [
    'itching', 'skin rash', 'nodal skin eruptions', 'continuous sneezing', 'shivering', 'chills', 'joint pain',
    'stomach pain', 'acidity', 'ulcers on tongue', 'muscle wasting', 'vomiting', 'burning micturition',
    'spotting urination', 'fatigue', 'weight gain', 'anxiety', 'cold hands and feets', 'mood swings',
    'weight loss', 'restlessness', 'lethargy', 'patches in throat', 'irregular sugar level', 'cough',
    'high fever', 'sunken eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache',
    'yellowish skin', 'dark urine', 'nausea', 'loss of appetite', 'pain behind the eyes', 'back pain',
    'constipation', 'abdominal pain', 'diarrhoea', 'mild fever', 'yellow urine', 'yellowing of eyes',
    'acute liver failure', 'fluid overload', 'swelling of stomach', 'swelled lymph nodes', 'malaise',
    'blurred and distorted vision', 'phlegm', 'throat irritation', 'redness of eyes', 'sinus pressure',
    'runny nose', 'congestion', 'chest pain', 'weakness in limbs', 'fast heart rate', 'pain during bowel movements',
    'pain in anal region', 'bloody stool', 'irritation in anus', 'neck pain', 'dizziness', 'cramps', 'bruising',
    'obesity', 'swollen legs', 'swollen blood vessels', 'puffy face and eyes', 'enlarged thyroid', 'brittle nails',
    'swollen extremeties', 'excessive hunger', 'extra marital contacts', 'drying and tingling lips',
    'slurred speech', 'knee pain', 'hip joint pain', 'muscle weakness', 'stiff neck', 'swelling joints',
    'movement stiffness', 'spinning movements', 'loss of balance', 'unsteadiness', 'weakness of one body side',
    'loss of smell', 'bladder discomfort', 'foul smell of urine', 'continuous feel of urine', 'passage of gases',
    'internal itching', 'toxic look (typhos)', 'depression', 'irritability', 'muscle pain', 'altered sensorium',
    'red spots over body', 'belly pain', 'abnormal menstruation', 'dischromic patches', 'watering from eyes',
    'increased appetite', 'polyuria', 'family history', 'mucoid sputum', 'rusty sputum', 'lack of concentration',
    'visual disturbances', 'receiving blood transfusion', 'receiving unsterile injections', 'coma',
    'stomach bleeding', 'distention of abdomen', 'history of alcohol consumption', 'fluid overload.1',
    'blood in sputum', 'prominent veins on calf', 'palpitations', 'painful walking', 'pus filled pimples',
    'blackheads', 'scurring', 'skin peeling', 'silver like dusting', 'small dents in nails', 'inflammatory nails',
    'blister', 'red sore around nose', 'yellow crust ooze'
]

    # Initialize an empty list to store the extracted symptoms
    extracted_symptoms = []

    # Iterate over the symptoms list and check if each symptom exists in the input text
    for symptom in symptoms:
        if re.search(r'\b{}\b'.format(symptom), input_text, re.IGNORECASE):
            extracted_symptoms.append(symptom)

    return extracted_symptoms

preset = {'itching': 0, 'skin_rash': 0, 'nodal_skin_eruptions': 0, 'continuous_sneezing': 0,
          'shivering': 0, 'chills': 0, 'joint_pain': 0, 'stomach_pain': 0, 'acidity': 0, 'ulcers_on_tongue': 0,
          'muscle_wasting': 0, 'vomiting': 0, 'burning_micturition': 0, 'spotting_ urination': 0, 'fatigue': 0,
          'weight_gain': 0, 'anxiety': 0, 'cold_hands_and_feets': 0, 'mood_swings': 0, 'weight_loss': 0,
          'restlessness': 0, 'lethargy': 0, 'patches_in_throat': 0, 'irregular_sugar_level': 0, 'cough': 0,
          'high_fever': 0, 'sunken_eyes': 0, 'breathlessness': 0, 'sweating': 0, 'dehydration': 0,
          'indigestion': 0, 'headache': 0, 'yellowish_skin': 0, 'dark_urine': 0, 'nausea': 0, 'loss_of_appetite': 0,
          'pain_behind_the_eyes': 0, 'back_pain': 0, 'constipation': 0, 'abdominal_pain': 0, 'diarrhoea': 0, 'mild_fever': 0,
          'yellow_urine': 0, 'yellowing_of_eyes': 0, 'acute_liver_failure': 0, 'fluid_overload': 0, 'swelling_of_stomach': 0,
          'swelled_lymph_nodes': 0, 'malaise': 0, 'blurred_and_distorted_vision': 0, 'phlegm': 0, 'throat_irritation': 0,
          'redness_of_eyes': 0, 'sinus_pressure': 0, 'runny_nose': 0, 'congestion': 0, 'chest_pain': 0, 'weakness_in_limbs': 0,
          'fast_heart_rate': 0, 'pain_during_bowel_movements': 0, 'pain_in_anal_region': 0, 'bloody_stool': 0,
          'irritation_in_anus': 0, 'neck_pain': 0, 'dizziness': 0, 'cramps': 0, 'bruising': 0, 'obesity': 0, 'swollen_legs': 0,
          'swollen_blood_vessels': 0, 'puffy_face_and_eyes': 0, 'enlarged_thyroid': 0, 'brittle_nails': 0, 'swollen_extremeties': 0,
          'excessive_hunger': 0, 'extra_marital_contacts': 0, 'drying_and_tingling_lips': 0, 'slurred_speech': 0,
          'knee_pain': 0, 'hip_joint_pain': 0, 'muscle_weakness': 0, 'stiff_neck': 0, 'swelling_joints': 0, 'movement_stiffness': 0,
          'spinning_movements': 0, 'loss_of_balance': 0, 'unsteadiness': 0, 'weakness_of_one_body_side': 0, 'loss_of_smell': 0,
          'bladder_discomfort': 0, 'foul_smell_of urine': 0, 'continuous_feel_of_urine': 0, 'passage_of_gases': 0, 'internal_itching': 0,
          'toxic_look_(typhos)': 0, 'depression': 0, 'irritability': 0, 'muscle_pain': 0, 'altered_sensorium': 0,
          'red_spots_over_body': 0, 'belly_pain': 0, 'abnormal_menstruation': 0, 'dischromic _patches': 0, 'watering_from_eyes': 0,
          'increased_appetite': 0, 'polyuria': 0, 'family_history': 0, 'mucoid_sputum': 0, 'rusty_sputum': 0, 'lack_of_concentration': 0,
          'visual_disturbances': 0, 'receiving_blood_transfusion': 0, 'receiving_unsterile_injections': 0, 'coma': 0,
          'stomach_bleeding': 0, 'distention_of_abdomen': 0, 'history_of_alcohol_consumption': 0, 'fluid_overload.1': 0,
          'blood_in_sputum': 0, 'prominent_veins_on_calf': 0, 'palpitations': 0, 'painful_walking': 0, 'pus_filled_pimples': 0,
          'blackheads': 0, 'scurring': 0, 'skin_peeling': 0, 'silver_like_dusting': 0, 'small_dents_in_nails': 0, 'inflammatory_nails': 0,
          'blister': 0, 'red_sore_around_nose': 0, 'yellow_crust_ooze': 0}

tts_obj = None
sr_obj = None

def predict_disease(intent_dict):
    sr_obj = intent_dict['sr_obj']
    tts_obj = intent_dict['tts_obj']
    mic = sr.Microphone()
    input_text = None

    print("Mention all symptoms : ")
    tts_obj.text = "tell me how do you feel?"
    tts_obj.play()

    with mic as source:
        mpg123_player.play_mpg123("/home/leah/Documents/leah-final-hindi/wake_word_engine/start_sound.mp3")
        audio = sr_obj.listen(source, phrase_time_limit = 10)
        mpg123_player.play_mpg123("/home/leah/Documents/leah-final-hindi/wake_word_engine/end_sound.mp3")
        input_text = sr_obj.recognize_google(audio)
        print("USER SAID : ", input_text)
        tts_obj.text = "okay, please wait while I use my experience to give a diagnosis. this will take some time"
        tts_obj.play()
    
    result = extract_symptoms(input_text)

    final_symptoms_list = []

    for symp in result:
        final_symptoms_list.append(symptoms_dict[symp])
    
    print(final_symptoms_list)

    # Set the input symptoms to 1 in the preset dictionary
    for symptom in final_symptoms_list:
        preset[symptom] = 1

    # Prepare Test Data
    df_test = pd.DataFrame(columns=list(preset.keys()))
    df_test.loc[0] = np.array(list(preset.values()))

    # Load pre-trained model
    clf = load("/home/leah/Documents/leah-final-hindi/tools/random_forest.joblib")
    result = clf.predict(df_test)
    print(result)
    tts_obj.text = "Based on the information provided, I have completed an initial assessment of your symptoms. It appears that the most likely diagnosis is, " + str(result[0]) + ". It's important to consult a healthcare professional for a confirmed diagnosis and appropriate-treatment."
    tts_obj.play()
    return result