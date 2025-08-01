from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from requests.exceptions import ConnectionError
from urllib3.exceptions import MaxRetryError, NameResolutionError

# ff. imports are for getting secret values from .env file
from pathlib import Path
import re
import tensorflow as tf
import pandas as pd
import numpy as np

# import and load model architectures as well as decoder
from modelling.models.cueva import LSTM_FE
from modelling.models.llanes_jurado import LSTM_CNN
from modelling.utilities.preprocessors import correct_signals, prep_stress_feats, mark_signals
from modelling.utilities.loaders import load_meta_data, load_model, load_lookup_array, charge_raw_data
from modelling.utilities.feature_extractors import extract_features, extract_features_hybrid, extract_features_per_hour

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

# # configure location of build file and the static html template file
app = Flask(__name__, template_folder='static')

# since simple html from url http://127.0.0.1:5000 requests to
# api endpoint at http://127.0.0.1:5000/ we must set the allowed
# origins or web apps with specific urls like http://127.0.0.1:5000
# to be included otherwise it will be blocked by CORS policy
CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5000", "http://localhost:5000", "https://aristodemus8-eda-denoiser-stress-detector.hf.space"])

# global variables
models = {
    "cueva-C_1_gamma_0p1_svm": {
        # 'model':
        # 'hyper_params':
    },
    "hossain-n_estimators_600_learning_rate_0p01_max_depth_10_gbt": {
        # 'model':
        # 'hyper_params':
        # 'scaler':
    },
    # "taylor-n_estimators_600_max_depth_30_class_weight_None_rf": {
    #     # 'model':
    #     # 'selected_feats':
    # },
    "taylor-C_1000_gamma_0p1_svm": {
        # 'model':
        # 'selected_feats':
    },
    "hossain-C_100_gamma_0p01_svm": {
        # 'model':
        # 'selected_feats':
        # 'scaler':
    },
    'taylor-C_100_class_weight_None_lr': {
        # 'model':
        # 'selected_feats':
    },
    'hossain-C_10_class_weight_None_lr': {
        # 'model':
        # 'selected_feats':
        # 'scaler':
    },
    'jurado-lstm-cnn': {
        # 'model':
        # 'selected_feats':
    },
    'cueva-lstm-fe': {
        # 'model':
        # 'hyper_params':
    },
    'stress-detector': {

    }
}


# functions to load miscellaneous variables, hyperparameters, and the model itself
def load_miscs():
    """
    loads miscellaneous variables to be used by the model
    """

    global models

    print('loading miscellaneous...')
    # this is for loading miscellaneous variables for 
    # deep learning models such as hyper parameters
    lstm_fe_hp = load_meta_data('./modelling/saved/misc/cueva_lstm-fe_meta_data.json')
    lstm_cnn_hp = load_meta_data('./modelling/saved/misc/jurado_lstm-cnn_meta_data.json')

    models['cueva-lstm-fe']['hyper_params'] = lstm_fe_hp
    models['jurado-lstm-cnn']['hyper_params'] = lstm_cnn_hp

    # this is for loading miscellaneous variables for
    # machine learning models such as the reduced feature set
    taylor_lr_red_feats = load_lookup_array(f'./modelling/data/Artifact Detection Data/reduced_taylor_lr_feature_set.txt')
    taylor_svm_red_feats = load_lookup_array(f'./modelling/data/Artifact Detection Data/reduced_taylor_svm_feature_set.txt')
    taylor_rf_red_feats = load_lookup_array(f'./modelling/data/Artifact Detection Data/reduced_taylor_rf_feature_set.txt')
    hossain_lr_red_feats = load_lookup_array(f'./modelling/data/Artifact Detection Data/reduced_hossain_lr_feature_set.txt')
    hossain_svm_red_feats = load_lookup_array(f'./modelling/data/Artifact Detection Data/reduced_hossain_svm_feature_set.txt')
    hossain_gbt_red_feats = load_lookup_array(f'./modelling/data/Artifact Detection Data/reduced_hossain_gbt_feature_set.txt')
    cueva_svm_red_feats = load_lookup_array(f'./modelling/data/Artifact Detection Data/reduced_cueva_second_phase_svm_feature_set.txt')
   

    # pre-load reduced features here so that features don't have to 
    # be loaded every single time user makes a request
    models['taylor-C_100_class_weight_None_lr']['selected_feats'] = taylor_lr_red_feats
    models['taylor-C_1000_gamma_0p1_svm']['selected_feats'] = taylor_svm_red_feats
    # models['taylor-n_estimators_600_max_depth_30_class_weight_None_rf']['selected_feats'] = taylor_rf_red_feats
    models['hossain-C_10_class_weight_None_lr']['selected_feats'] = hossain_lr_red_feats
    models['hossain-C_100_gamma_0p01_svm']['selected_feats'] = hossain_svm_red_feats
    models['hossain-n_estimators_600_learning_rate_0p01_max_depth_10_gbt']['selected_feats'] = hossain_gbt_red_feats 
    models['cueva-C_1_gamma_0p1_svm']['selected_feats'] = cueva_svm_red_feats

    print('miscellaneous loaded.')


def load_preprocessors():
    """
    prepares and loads the saved encoders, normalizers of
    the dataset to later transform raw user input from
    client-side
    """
    global models

    print('loading preprocessors...')

    # pre-load here scaler of hossain used during training
    hossain_C_10_class_weight_None_lr_scaler = load_model('./modelling/saved/misc/hossain_lr_scaler.pkl')
    hossain_C_100_gamma_0p01_svm_scaler = load_model('./modelling/saved/misc/hossain_svm_scaler.pkl')
    hossain_n_estimators_600_learning_rate_0p01_max_depth_10_gbt_scaler = load_model('./modelling/saved/misc/hossain_gbt_scaler.pkl')
    cueva_C_1_gamma_0p1_svm_scaler = load_model('./modelling/saved/misc/cueva_second_phase_svm_scaler.pkl')
    
    # separate loading of scaler for stress detection
    xgb_scaler = load_model('./modelling/saved/misc/xgb_scaler.pkl')

    models['hossain-C_10_class_weight_None_lr']['scaler'] = hossain_C_10_class_weight_None_lr_scaler
    models['hossain-C_100_gamma_0p01_svm']['scaler'] = hossain_C_100_gamma_0p01_svm_scaler
    models['hossain-n_estimators_600_learning_rate_0p01_max_depth_10_gbt']['scaler'] = hossain_n_estimators_600_learning_rate_0p01_max_depth_10_gbt_scaler
    models['cueva-C_1_gamma_0p1_svm']['scaler'] = cueva_C_1_gamma_0p1_svm_scaler

    models['stress-detector']['scaler'] = xgb_scaler

    print('preprocessors loaded.')

def load_models():
    """
    prepares and loads sample input and custom model in
    order to use trained weights/parameters/coefficients
    """
    global models
    
    print('loading models...')
    # pre load saved weights for deep learning models
    jurado_lstm_cnn = LSTM_CNN(**models['jurado-lstm-cnn']['hyper_params'])
    jurado_lstm_cnn.load_weights('./modelling/saved/weights/EDABE_LSTM_1DCNN_Model.h5')

    # load side task model and convert it to a feature extractor model 
    lstm_fe = LSTM_FE(**models['cueva-lstm-fe']['hyper_params'])
    lstm_fe.load_weights('./modelling/saved/weights/cueva_lstm-fe_21_0.7489.weights.h5')
    lstm_layer_2 = lstm_fe.get_layer('lstm-layer-2')
    lstm_fe_main = tf.keras.Model(inputs=lstm_fe.inputs, outputs=lstm_layer_2.output)

    # pre load saved machine learning models
    taylor_C_100_class_weight_None_lr = load_model('./modelling/saved/models/taylor_C_100_class_weight_None_lr_clf.pkl')
    taylor_C_1000_gamma_0p1_svm = load_model('./modelling/saved/models/taylor_C_1000_gamma_0p1_probability_True_class_weight_None_svm_clf.pkl')
    # taylor_n_estimators_600_max_depth_30_class_weight_None_rf = load_model('./modelling/saved/models/taylor_n_estimators_600_max_depth_30_class_weight_None_rf_clf.pkl')
    hossain_C_10_class_weight_None_lr = load_model('./modelling/saved/models/hossain_C_10_class_weight_None_lr_clf.pkl')
    hossain_C_100_gamma_0p01_svm = load_model('./modelling/saved/models/hossain_C_100_gamma_0p01_probability_True_class_weight_None_svm_clf.pkl')
    hossain_n_estimators_600_learning_rate_0p01_max_depth_10_gbt = load_model('./modelling/saved/models/hossain_n_estimators_600_learning_rate_0p01_max_depth_10_gbt_clf.pkl')
    cueva_C_1_gamma_0p1_svm = load_model('./modelling/saved/models/cueva_second_phase_C_1_gamma_0p1_probability_True_class_weight_None_svm_clf.pkl')

    # load stress detector model separately
    stress_detector = load_model('./modelling/saved/models/stress_detector.pkl')

    # populate dictionary with loaded models
    models['jurado-lstm-cnn']['model'] = jurado_lstm_cnn
    models['cueva-lstm-fe']['model'] = lstm_fe
    models['cueva-lstm-fe']['feature_extractor'] = lstm_fe_main

    models['taylor-C_100_class_weight_None_lr']['model'] = taylor_C_100_class_weight_None_lr
    models['taylor-C_1000_gamma_0p1_svm']['model'] = taylor_C_1000_gamma_0p1_svm
    # models['taylor-n_estimators_600_max_depth_30_class_weight_None_rf']['model'] = taylor_n_estimators_600_max_depth_30_class_weight_None_rf
    models['hossain-C_10_class_weight_None_lr']['model'] = hossain_C_10_class_weight_None_lr
    models['hossain-C_100_gamma_0p01_svm']['model'] = hossain_C_100_gamma_0p01_svm
    models['hossain-n_estimators_600_learning_rate_0p01_max_depth_10_gbt']['model'] = hossain_n_estimators_600_learning_rate_0p01_max_depth_10_gbt
    models['cueva-C_1_gamma_0p1_svm']['model'] = cueva_C_1_gamma_0p1_svm

    models['stress-detector']['model'] = stress_detector

    print('models loaded.')
    



load_miscs()
load_preprocessors()
load_models()

print(models)



@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    print(error)
    return 'This page does not exist', 404

# upon loading of client side fetch the model names
@app.route('/model-names', methods=['GET'])
def retrieve_model_names():
    """
    flask app will run at http://127.0.0.1:5000 if /
    in url succeeds another string <some string> then
    app will run at http://127.0.0.1:5000/<some string>

    returns json object of all model names loaded upon
    start of server and subsequent request of client to
    this view function
    """

    data = {
        'model_names': list(models.keys())
    }

    # return data at once since no error will most likely
    # occur on mere loading of the model
    return jsonify(data)

@app.route('/send-data', methods=['POST'])
def predict():
    """
    this route will receive clients uploaded .csv file which contains
    the eda signals of a subject 

    this function will then parse and convert the eda signals from dataframe
    to numerical features if ml model is to be used but if dl model then the
    eda signal df is left as it is and passed to trained model

    if dl models are chosen the charge_raw_data() function is used to 
    preprocess the eda signal df and be used as input to the dl model
    and if ml models signals are then used to extract features from
    via extract_features() function

    we will also have to select only the features as selected during tuning

    depending on what model the client chooses the model may be under Hossain
    et al. (2022), Taylor et al. (2015), or Llanes-Jurado et al. (2023) pipeline
    which may or may not have used StandardScaler() during training, if such is
    the case that the user chooses a model under Hossain et al. (2022) then the
    eda signal df which have now been transformed to numerical features must undergo
    further normalization based on the scaler used during training
    """

    # if user requests for demo file raw_files will be empty
    # but if user uploads a file the raw_files will have this file
    raw_data = request.form
    raw_files = request.files

    model_name = raw_data.get('model_name')
    
    spreadsheet_file = raw_files.get('spreadsheet_file')
    spreadsheet_file = raw_data.get('spreadsheet_file') if not spreadsheet_file  else spreadsheet_file

    # spreadsheet_fname = re.sub(r".csv", "", spreadsheet_file.filename)
    show_raw = raw_data.get('show_raw')
    show_correct = raw_data.get('show_correct')
    show_art = raw_data.get('show_art')

    subject_eda_data = pd.read_csv(spreadsheet_file, sep=';')
    subject_eda_data.columns = ['time', 'raw_signal', 'clean_signal', 'label', 'auto_signal', 'pred_art', 'post_proc_pred_art']
    print(subject_eda_data)
    
    selector_config, estimator_name = model_name.split('-', 1)
    print(selector_config)
    print(estimator_name)

    # this is if deep learning model is chosen
    if selector_config == "hossain" or selector_config == "taylor":
        # load the extracted test features instead as opposed 
        # to using extract-features() method which takes longer to run
        subject_features, subject_labels = extract_features(subject_eda_data, extractor_fn=extract_features_per_hour)
        # subject_features = pd.read_csv(f'./modelling/data/Artifact Detection Data/test/{spreadsheet_fname}_features.csv', index_col=0)
        # subject_labels = pd.read_csv(f'./modelling/data/Artifact Detection Data/test/{spreadsheet_fname}_labels.csv', index_col=0)
        print(subject_features.shape)
        print(subject_labels.shape)

        # once features are extracted features selected during
        # tuning will be used in testing as done also during training
        selected_feats = models[model_name]['selected_feats']
        subject_features = subject_features[selected_feats]
        print(subject_features.columns)

        # convert features and labels into numpy matrices
        X = subject_features.to_numpy()
        Y = subject_labels.to_numpy().ravel()

        # if hossain is the researcher chosen the scaler used during training
        # will be used to scale the test subject features
        if selector_config == "hossain":    
            scaler = models[model_name]['scaler']
            X = scaler.transform(X)

        model = models[model_name]['model']
        Y_pred = model.predict(X)
        Y_pred_prob = model.predict_proba(X)
        print(f"predicted Y: {Y_pred}")
        print(f"unique values and counts: {np.unique(Y_pred, return_counts=True)}")
        print(f"true Y: {Y}")
        print(f"unique values and counts: {np.unique(Y, return_counts=True)}")

        # compute performance metric values for test subject
        test_acc = accuracy_score(y_true=Y, y_pred=Y_pred)
        test_prec = precision_score(y_true=Y, y_pred=Y_pred, average="weighted")
        test_rec = recall_score(y_true=Y, y_pred=Y_pred, average="weighted")
        test_f1 = f1_score(y_true=Y, y_pred=Y_pred, average="weighted")
        test_roc_auc = roc_auc_score(y_true=Y, y_score=Y_pred_prob[:, 1], average="weighted", multi_class="ovo")
        test_conf_matrix = confusion_matrix(Y, Y_pred).tolist()
        test_true_neg = test_conf_matrix[0][0]
        test_false_pos = test_conf_matrix[0][1]
        test_false_neg = test_conf_matrix[1][0]
        test_true_pos = test_conf_matrix[1][1]
        test_tpr = test_true_pos / (test_true_pos + test_false_neg)
        test_tnr = test_true_neg / (test_true_neg + test_false_pos)
        test_fpr = test_false_pos / (test_false_pos + test_true_neg)
        test_fnr = test_false_neg / (test_false_neg + test_true_pos)

        print(f"test acc: {test_acc} \
            \ntest prec: {test_prec} \
            \ntest rec: {test_rec} \
            \ntest f1: {test_f1} \
            \ntest roc_auc: {test_roc_auc} \
            \ntest conf_matrix: {test_conf_matrix} \
            \ntest tpr: {test_tpr} \
            \ntest tnr: {test_tnr} \
            \ntest fpr: {test_fpr} \
            \ntest fnr: {test_fnr}")

    elif selector_config == "jurado" or (selector_config == "cueva" and estimator_name == "lstm-fe"):
        # pass
        subject_signals, subject_labels = charge_raw_data(subject_eda_data, x_col="raw_signal", y_col='label', scale=True, verbose=True)
        print(f'signals {subject_signals}, shape: {subject_signals.shape}')
        print(f'labels {subject_labels}, shape: {subject_labels.shape}')

        # signals and labels are already numpy matrices
        # assign to X and Y variable for readability
        X = subject_signals
        Y = subject_labels

        # assign model
        model = models[model_name]['model']

        # depending on dl model Y_pred will either be unactivated logits 
        # or sigmoid probabilities
        Y_pred_prob = model.predict(X)

        # when our predictions is 0.2, 0.15, and below which is <= 0.2 then y_pred will be 0
        # when our predictions is 1, 0.5, 0.4, 0.3, 0.21, and above which is > 0.2 then y_pred will be 1
        # why we do this is because of the imbalance of our dataset, and we
        # want to place a threshold of 20% since there our dataset only consists
        # of 20% of positive classes. Note this conversion is to be used in precision and recall metrics
        Y_pred = tf.cast(Y_pred_prob >= 0.2, tf.int64)

        print(f"predicted Y: {Y_pred}")
        print(f"unique values and counts: {np.unique(Y_pred, return_counts=True)}")
        print(f"true Y: {Y}")
        print(f"unique values and counts: {np.unique(Y, return_counts=True)}")

        # compute performance metric values for test subject
        test_acc = accuracy_score(y_true=Y, y_pred=Y_pred)
        test_prec = precision_score(y_true=Y, y_pred=Y_pred, average="weighted")
        test_rec = recall_score(y_true=Y, y_pred=Y_pred, average="weighted")
        test_f1 = f1_score(y_true=Y, y_pred=Y_pred, average="weighted")
        test_roc_auc = roc_auc_score(y_true=Y, y_score=Y_pred_prob, average="weighted", multi_class="ovo")
        test_conf_matrix = confusion_matrix(Y, Y_pred).tolist()
        test_true_neg = test_conf_matrix[0][0]
        test_false_pos = test_conf_matrix[0][1]
        test_false_neg = test_conf_matrix[1][0]
        test_true_pos = test_conf_matrix[1][1]
        test_tpr = test_true_pos / (test_true_pos + test_false_neg)
        test_tnr = test_true_neg / (test_true_neg + test_false_pos)
        test_fpr = test_false_pos / (test_false_pos + test_true_neg)
        test_fnr = test_false_neg / (test_false_neg + test_true_pos)

        print(f"test acc: {test_acc} \
            \ntest prec: {test_prec} \
            \ntest rec: {test_rec} \
            \ntest f1: {test_f1} \
            \ntest roc_auc: {test_roc_auc} \
            \ntest conf_matrix: {test_conf_matrix} \
            \ntest tpr: {test_tpr} \
            \ntest tnr: {test_tnr} \
            \ntest fpr: {test_fpr} \
            \ntest fnr: {test_fnr}")
        
    # this condition is triggered whenever user picks the cueva but uses the lstm-svm as estimator name
    else:
        # extract lower order features of the test data akin to previous ml models
        subject_lof, subject_labels = extract_features(subject_eda_data, extractor_fn=extract_features_hybrid)
        # subject_lof = pd.read_csv(f'./modelling/data/Hybrid Artifact Detection Data/test/{spreadsheet_fname}_lof.csv', index_col=0)
        # subject_labels = pd.read_csv(f'./modelling/data/Hybrid Artifact Detection Data/test/{spreadsheet_fname}_labels.csv', index_col=0)
        print(f'lower order features shape: {subject_lof.shape}')
        print(f'labels shape: {subject_labels.shape}')

        # load test signals and use it to extract the higher order features from it
        subject_signals, _ = charge_raw_data(subject_eda_data, x_col="raw_signal", y_col='label', scale=True, verbose=True)
        print(f'signals {subject_signals}, shape: {subject_signals.shape}')
        print(f'labels {subject_labels}, shape: {subject_labels.shape}')

        # extract higher features
        lstm_fe_main = models[f"{selector_config}-lstm-fe"]['feature_extractor']
        subject_hof_arr = lstm_fe_main.predict(subject_signals)
        columns = [f'HOF_{i}' for i in range(1, subject_hof_arr.shape[1] + 1)]
        subject_hof = pd.DataFrame(subject_hof_arr, columns=columns)
        # subject_hof = pd.read_csv(f'./modelling/data/Hybrid Artifact Detection Data/test/{spreadsheet_fname}_hof.csv', index_col=0)
        print(f'higher order features shape: {subject_hof.shape}')

        # concatenate both dataframes of higher and lower features 
        subject_hof_lof = pd.concat([subject_hof, subject_lof], axis=1)
        print(f'full subject_hof_lof shape: {subject_hof_lof.shape}')

        # once features are extracted features selected during
        # tuning will be used in testing as done also during training
        selected_feats = models[model_name]['selected_feats']
        subject_hof_lof = subject_hof_lof[selected_feats]
        print(f'reduced subject_hof_lof shape: {subject_hof_lof.shape}')

        X = subject_hof_lof.to_numpy()
        Y = subject_labels.to_numpy().ravel()

        # if hossain is the researcher chosen the scaler used during training
        # will be used to scale the test subject features
        if selector_config == "cueva":    
            scaler = models[model_name]['scaler']
            X = scaler.transform(X)

        # assign model
        model = models[model_name]['model']

        # use model for prediction
        Y_pred = model.predict(X)
        Y_pred_prob = model.predict_proba(X)
        print(f"predicted Y: {Y_pred}")
        print(f"unique values and counts: {np.unique(Y_pred, return_counts=True)}")
        print(f"true Y: {Y}")
        print(f"unique values and counts: {np.unique(Y, return_counts=True)}")

        # compute performance metric values for test subject
        test_acc = accuracy_score(y_true=Y, y_pred=Y_pred)
        test_prec = precision_score(y_true=Y, y_pred=Y_pred, average="weighted")
        test_rec = recall_score(y_true=Y, y_pred=Y_pred, average="weighted")
        test_f1 = f1_score(y_true=Y, y_pred=Y_pred, average="weighted")
        test_roc_auc = roc_auc_score(y_true=Y, y_score=Y_pred_prob[:, 1], average="weighted", multi_class="ovo")
        test_conf_matrix = confusion_matrix(Y, Y_pred).tolist()
        test_true_neg = test_conf_matrix[0][0]
        test_false_pos = test_conf_matrix[0][1]
        test_false_neg = test_conf_matrix[1][0]
        test_true_pos = test_conf_matrix[1][1]
        test_tpr = test_true_pos / (test_true_pos + test_false_neg)
        test_tnr = test_true_neg / (test_true_neg + test_false_pos)
        test_fpr = test_false_pos / (test_false_pos + test_true_neg)
        test_fnr = test_false_neg / (test_false_neg + test_true_pos)

        print(f"test acc: {test_acc} \
            \ntest prec: {test_prec} \
            \ntest rec: {test_rec} \
            \ntest f1: {test_f1} \
            \ntest roc_auc: {test_roc_auc} \
            \ntest conf_matrix: {test_conf_matrix} \
            \ntest tpr: {test_tpr} \
            \ntest tnr: {test_tnr} \
            \ntest fpr: {test_fpr} \
            \ntest fnr: {test_fnr}")

    # once predictions have been extracted from respective models
    # pass to the correct_signals() function
    corrected_df, dict_metrics = correct_signals(Y_pred, subject_eda_data, selector_config, estimator_name)
    # print(f'dict metrics: {dict_metrics}')

    # use dataframe to obtain phasic and tonic components of corrected signal
    # and then from it compute features that will be used by the trained stress
    # detection model
    corrected_stress_feats = prep_stress_feats(corrected_df=corrected_df)

    # remove label column 
    corrected_stress_feats = corrected_stress_feats.drop(columns=['label']).to_numpy()
    
    # assign variables to stress detection scaler and model 
    xgb_scaler = models['stress-detector']['scaler']
    stress_detector = models['stress-detector']['model']

    # use scaler to transform features and to predict
    # the stress levels of a subject
    corrected_stress_feats_scaled = xgb_scaler.transform(corrected_stress_feats)
    stress_labels = stress_detector.predict(corrected_stress_feats_scaled)

    # resultant df will now contain stress levels. Why we set the target size to 640
    # is because even though we trained the model on 4hz its target size frequency or
    # window size we chose was still 5 seconds or 20 rows per 5 seconds and because
    # we want a window size of 5 seconds also for 128hz this means 128 * 5 which is 640
    # rows per 5 seconds. This will somehow reinterpolate our data to that of 128hz even
    # if the predicted labels are at 4hz
    res_test_df = mark_signals(stress_labels, corrected_df, target_size_freq=640, freq_signal=128)
    # res_test_df.to_csv(f'./modelling/results/{spreadsheet_fname}.csv')
    
    # corrected df is automatically converted to an array of records e.g.
    # {'time': 0.0, 'raw_signal': 42.1234, 'new_signal': 23.123}
    return jsonify({'corrected_df': res_test_df.to_dict("records")})