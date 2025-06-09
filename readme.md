# This repository contains all generalized code snippets and templates relating to model experimentation, training, evaluation, testing, server-side loading, client-side requests, usage documentation, loaders, evaluators, visualizers, and preprocessor utilities, and the model architectures, figures, and final folder. You can visit the full application at https://aristodemus8-eda-denoiser-stress-detector.hf.space/

# Requirements:
1. git
2. conda
3. python

# Source code usage
1. assuming git is installed clone repository by running `git clone https://github.com/08Aristodemus24/thesis-writing-1`
2. assuming conda is also installed run `conda create -n <environment name e.g. thesis-writing-1> python=3.12.3`. Note python version should be `3.12.3` for the to be created conda environment to avoid dependency/package incompatibility.
3. run `conda activate thesis-writing-1` or `activate thesis-writing-1`.
4. run `conda list -e` to see list of installed packages. If pip is not yet installed run conda install pip, otherwise skip this step and move to step 5.
5. navigate to directory containing the `requirements.txt` file.
5. run `pip install -r requirements.txt` inside the directory containing the `requirements.txt` file
6. after installing packages/dependencies run `python index.py` while in this directory to run app locally

# App usage:
1. control panel of app will have ff. inputs: raw eda signals

# File structure:
```
|- client-side
    |- public
    |- src
        |- assets
            |- mediafiles
        |- boards
            |- *.png/jpg/jpeg/gig
        |- components
            |- *.svelte/jsx
        |- App.svelte/jsx
        |- index.css
        |- main.js
        |- vite-env.d.ts
    |- index.html
    |- package.json
    |- package-lock.json
    |- ...
|- server-side
    |- modelling
        |- data
            |- Artifact Detection Data
                |- test
                    |- *_features.csv
                    |- *_labels.csv
                |- train
                    |- *_features.csv
                    |- *_labels.csv
                |- reduced_cueva_second_phase_svm_feature_set1.txt
                |- reduced_cueva_second_phase_svm_feature_set.txt
                |- hossain_feature_set.txt
                |- reduced_hossain_lr_feature_set.txt
                |- reduced_hossain_gbt_feature_set.txt
                |- reduced_hossain_svm_feature_set.txt
                |- taylor_feature_set.txt
                |- reduced_taylor_lr_feature_set.txt
                |- reduced_taylor_rf_feature_set.txt
                |- reduced_taylor_svm_feature_set.txt
            |- Electrodermal Activity artifact correction BEnchmark (EDABE)
                |- Train
                    |- *.csv
                |- Test
                    |- *.csv
            |- Hybrid Artifact Detection Data
                |- train
                    |- *_hof.csv
                    |- *_lof.csv
                    |- *_labels.csv
                |- test
                    |- *_hof.csv
                    |- *_lof.csv
                    |- *_labels.csv
                |- dummy.txt
            |- Hosseini_Stress_Dataset
            |- Stress Detection Features
            |- dummy.txt
            |- EDABE dataset.zip
            |- Stress_dataset.zip
        |- figures & images
            |- *.png/jpg/jpeg/gif
        |- models
            |- __init__.py
            |- cueva.py
            |- llanes_jurado.py
        |- results
            |- all_models_results.json
            |- hossain_gbt_results.json
            |- hossain_lr_results.json
            |- hossain_svm_results.json
            |- taylor_rf_results.json
            |- taylor_lr_results.json
            |- taylor_svm_results.json
            |- pqbqpr_expert2_corrected.csv
        |- saved
            |- misc
                |- cueva_lstm-fe_meta_data.json
                |- jurado_lstm-cnn_meta_data.json
                |- hossain_lr_scaler.pkl
                |- hossain_svm_scaler.pkl
                |- hossain_gbt_scaler.pkl
                |- xgb_scaler.pkl
                |- dummy.pkl
            |- models
                |- cueva_second_phase_svm_clf1.pkl
                |- cueva_second_phase_svm_clf.pkl
                |- hossain_lr_clf.pkl
                |- hossain_svm_clf.pkl
                |- hossain_gbt_clf.pkl
                |- taylor_lr_clf.pkl
                |- taylor_svm_clf.pkl
                |- taylor_rf_clf.pkl
                |- stress_detector.pkl
                |- dummy.pkl
            |- weights
                |- *.weights.h5
        |- utilities
            |- __init__.py
            |- loaders.py
            |- preprocessors.py
            |- visualizers.py
            |- evaluators.py
            |- feature_extractors.py
            |- stress_feature_extractors.py
        |- __init__.py
        |- experimentation.ipynb
        |- feature_engineering.ipynb
        |- data_analysis.ipynb
        |- summarization.ipynb
        |- evaluation.ipynb
        |- visualization.ipynb
        |- stress_detection.py
        |- tuning_ml.py
        |- tuning_dl.py
        |- *.sbatch
    |- static
        |- assets
            |- *.js
            |- *.css
        |- index.html
    |- index.py
    |- server.py
    |- requirements.txt
|- demo-video.mp5
|- .gitignore
|- readme.md
```

**"Larry, Taline, Deseree, and Wana will <s>graduate</s>graduated in 2025"**