# -*- coding: utf-8 -*-
"""Final Project - Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CuwnIDqOfxRcGmZ1m0QzzCm-ns9OzFb6
"""

!pip install streamlit --quiet
!pip install pyngrok --quiet

pip install codecarbon

!pip install -U scikit-learn

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# import pandas as pd
# import numpy as np
# import seaborn as sns
# import timeit
# import statsmodels.api as sm
# from tabulate import tabulate
# import matplotlib.pyplot as plt
# from PIL import Image
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split
# from sklearn import metrics as mt
# from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, roc_auc_score, auc
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.decomposition import PCA
# from sklearn.preprocessing import LabelEncoder
# from codecarbon import OfflineEmissionsTracker
# from scipy.special import expit
# 
# 
# 
# ### Titles and sidebar
# st.title("Hotel Bookings - Predictions")
# model_mode = st.sidebar.selectbox('📈 Select Prediction Model', ['Logistic Regression', 'K-Nearest Neighbors Algorithm']) 
# 
# ### Dataframe cleaning - encode categorical variables to numerical
# df = pd.read_csv("df.csv")
# categorical_columns = ['hotel','meal', 'arrival_date_year', 'arrival_date_month', 'country', 'market_segment', 'distribution_channel', 'deposit_type', 'customer_type', 'reservation_status']
# for col in categorical_columns:
#     encoder = LabelEncoder()
#     df[col] = encoder.fit_transform(df[col])
# df.dropna()
# columns_to_drop = ['company', 'reservation_status_date', 'reserved_room_type', 'arrival_date_day_of_month', 'assigned_room_type']
# df.drop(columns = columns_to_drop, inplace=True)
# 
# column_labels = {'hotel': 'Hotel Type',
#                 'is_canceled': 'Is Canceled',
#                 'lead_time': 'Lead Time',
#                 'arrival_date_year': 'Arrival Year',
#                 'arrival_date_month': 'Arrival Month',
#                 'arrival_date_week_number': 'Arrival Week Number',
#                 'stays_in_weekend_nights': 'Stays in Weekend Nights',
#                 'stays_in_week_nights': 'Stays in Week Nights',
#                 'adults': 'Adults',
#                 'children': 'Children',
#                 'babies': 'Babies',
#                 'meal': 'Meal',
#                 'country': 'Country',
#                 'market_segment': 'Market Segment',
#                 'distribution_channel': 'Distribution Channel',
#                 'is_repeated_guest': 'Is Repeated Guest',
#                 'previous_cancellations': 'Previous Cancellations',
#                 'previous_bookings_not_canceled': 'Previous Bookings Not Canceled',
#                 'booking_changes': 'Booking Changes',
#                 'deposit_type': 'Deposit Type',
#                 'agent': 'Agent',
#                 'days_in_waiting_list': 'Days in Waiting List',
#                 'customer_type': 'Customer Type',
#                 'adr': 'ADR',
#                 'required_car_parking_spaces': 'Required Car Parking Spaces',
#                 'total_of_special_requests': 'Total of Special Requests',
#                 'reservation_status_date': 'Reservation Status Date'}
# 
# df = df.rename(columns=column_labels)
# 
# 
# ### Select the dependent variable
# list_dependent = ['Hotel Type', 'Is Canceled']
# selected_dependent = st.sidebar.selectbox('🧩  Select Variable to Predict', list_dependent)
# 
# if model_mode == 'Logistic Regression':
#   
#   train_size = st.sidebar.number_input("Train Set Size", min_value=0.00, step=0.01, max_value=1.00, value=0.70)
#   
#   df_without_dependent = df.drop(list_dependent, axis=1) 
#   list_explanatory = df_without_dependent.columns
# 
#   try:
#     selected_explanatory = st.multiselect("##### Select Explanatory Variables", list_explanatory, default = ['Market Segment','Booking Changes'])
# 
#     df_explanatory = df_without_dependent[selected_explanatory]
#     X =  df_explanatory
#     y = df[selected_dependent]
# 
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= train_size, random_state= 42)
# 
#     log_model = LogisticRegression()
#     log_model.fit(X_train, y_train)
# 
#     y_pred = log_model.predict(X_test)
#     
#     
#     # Display model accuracy
#     accuracy = accuracy_score(y_test, y_pred)
#     st.write("#### 🎯 Model Accuracy:", np.round(accuracy, 2))
# 
#     # Convert classification report dictionary to a DataFrame
#     classification_rep = classification_report(y_test, y_pred, output_dict=True)
#     table_df = pd.DataFrame(classification_rep).transpose()
#     
#     # Convert float values to string with 2 decimal places for formatting
#     table_df['precision'] = table_df['precision'].apply(lambda x: f"{x:.2f}")
#     table_df['recall'] = table_df['recall'].apply(lambda x: f"{x:.2f}")
#     table_df['f1-score'] = table_df['f1-score'].apply(lambda x: f"{x:.2f}")
#     
#     # Display the classification report as a table
#     st.markdown("#### 📊 Classification Report:")
#     st.table(table_df.style.set_caption("").hide_index())
# 
#     if selected_dependent == 'Hotel Type':
#       st.info("Note that value **0** corresponds to **City Hotel**, and value **1** corresponds to **Resort Hotel**")
# 
#       ## P-values table
#       st.markdown("##### P-values of predictor variables:")
#       logit_model = sm.Logit(y, X)
#       result = logit_model.fit()
#       p_values = result.pvalues
#       st.table(p_values)
#       
#       ## Confusion matrix
#       cm = confusion_matrix(y_test, y_pred)
#       label_names = ['City Hotel', 'Resort Hotel']
#       sns.heatmap(cm, annot = True, fmt = 'g', xticklabels = label_names, yticklabels = label_names)
#       plt.xlabel('Predicted')
#       plt.ylabel('Actual')
#       plt.title('Confusion Matrix')
# 
#       info_text = '''
#       **Interpreting the confusion matrix:**
# 
#       The confusion matrix summarizes the performance of a classification model by
#       showing the number of true and false positives and negatives for each class.
# 
#       - True positives: the number of instances that were correctly predicted as positive.
#       - False positives: the number of instances that were incorrectly predicted as positive.
#       - True negatives: the number of instances that were correctly predicted as negative.
#       - False negatives: the number of instances that were incorrectly predicted as negative.
# 
#       The confusion matrix can be used to calculate various performance metrics for the model,
#       such as accuracy, precision, recall, and F1 score. These metrics can help to evaluate
#       the overall effectiveness of the model and identify areas for improvement.
#       '''
#       st.markdown("#### ⚙️ Logistic regression confusion matrix:")
#       st.info(info_text)
#       st.pyplot(plt.gcf())
# 
#       ## ROC curve
#       probas = log_model.predict_proba(X)[:, 1]
#       auc = roc_auc_score(y, probas)
#       fpr, tpr, thresholds = roc_curve(y, probas)
#       fig, ax = plt.subplots()
#       ax.plot(fpr, tpr, label='ROC curve (AUC = %0.2f)' % auc)
#       ax.plot([0, 1], [0, 1], 'k--')
#       ax.set_xlabel('False Positive Rate')
#       ax.set_ylabel('True Positive Rate')
#       ax.set_title('Receiver Operating Characteristic')
#       ax.legend(loc='lower right')
#       st.markdown("#### ⚙️ ROC curve:")
#       st.info("The ROC curve is a graphical representation of the performance of a binary classifier at different decision thresholds. It is created by plotting the true positive rate (TPR) against the false positive rate (FPR) at various threshold settings. AUC (Area Under the Curve) is a single number that summarizes the ROC curve performance. AUC ranges from 0 to 1, with higher values indicating better performance. AUC of 0.5 represents a random guess, while an AUC of 1.0 represents a perfect classifier. You can use the ROC curve to compare the performance of different classifiers or to choose the best threshold for your classifier based on your specific needs.")
#       st.pyplot(fig)
# 
#     else:
#       st.info("Note that value **0** corresponds to **Is Not Canceled**, and value **1** corresponds to **Is Canceled**")
# 
#       ## P-values table
#       st.markdown("##### P-values of predictor variables:")
#       logit_model = sm.Logit(y, X)
#       result = logit_model.fit()
#       p_values = result.pvalues
#       st.table(p_values)
#       
#       ## Confusion matrix
#       cm = confusion_matrix(y_test, y_pred)
#       label_names = ['Is Not Canceled', 'Is Canceled']
#       sns.heatmap(cm, annot = True, fmt = 'g', xticklabels = label_names, yticklabels = label_names)
#       plt.xlabel('Predicted')
#       plt.ylabel('Actual')
#       plt.title('Confusion Matrix')
# 
#       info_text = '''
#       **Interpreting the confusion matrix:**
# 
#       The confusion matrix summarizes the performance of a classification model by
#       showing the number of true and false positives and negatives for each class.
# 
#       - True positives: the number of instances that were correctly predicted as positive.
#       - False positives: the number of instances that were incorrectly predicted as positive.
#       - True negatives: the number of instances that were correctly predicted as negative.
#       - False negatives: the number of instances that were incorrectly predicted as negative.
# 
#       The confusion matrix can be used to calculate various performance metrics for the model,
#       such as accuracy, precision, recall, and F1 score. These metrics can help to evaluate
#       the overall effectiveness of the model and identify areas for improvement.
#       '''
#       st.markdown("#### ⚙️ Logistic regression confusion matrix:")
#       st.info(info_text)
#       st.pyplot(plt.gcf())
# 
#       ## ROC curve
#       probas = log_model.predict_proba(X)[:, 1]
#       auc = roc_auc_score(y, probas)
#       fpr, tpr, thresholds = roc_curve(y, probas)
#       fig, ax = plt.subplots()
#       ax.plot(fpr, tpr, label='ROC curve (AUC = %0.2f)' % auc)
#       ax.plot([0, 1], [0, 1], 'k--')
#       ax.set_xlabel('False Positive Rate')
#       ax.set_ylabel('True Positive Rate')
#       ax.set_title('Receiver Operating Characteristic')
#       ax.legend(loc='lower right')
#       st.markdown("#### ⚙️ ROC curve:")
#       st.info("The ROC curve is a graphical representation of the performance of a binary classifier at different decision thresholds. It is created by plotting the true positive rate (TPR) against the false positive rate (FPR) at various threshold settings. AUC (Area Under the Curve) is a single number that summarizes the ROC curve performance. AUC ranges from 0 to 1, with higher values indicating better performance. AUC of 0.5 represents a random guess, while an AUC of 1.0 represents a perfect classifier. You can use the ROC curve to compare the performance of different classifiers or to choose the best threshold for your classifier based on your specific needs.")
#       st.pyplot(fig)
# 
# 
#   except ValueError:
#     st.error("Please select at least one explanatory variable!")
# 
# ## KNN
# else: 
# 
#   ## Sidebar
#   train_size = st.sidebar.number_input("Train Set Size", min_value=0.00, step=0.01, max_value=1.00, value=0.70)
#   df_without_dependent = df.drop(list_dependent, axis=1) 
#   list_explanatory = df_without_dependent.columns
#   k_parameter = st.sidebar.slider("Input K",5,1,10)
#   distance_metric = st.sidebar.radio("Select a distance metric:",("euclidean", "manhattan", "chebyshev"))
# 
#   try:
#     selected_explanatory = st.multiselect("##### Select Explanatory Variables", list_explanatory, default = ['Market Segment','Booking Changes'])
#     df_explanatory = df_without_dependent[selected_explanatory]
#     X =  df_explanatory
#     y = df[selected_dependent]
# 
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= train_size, random_state= 42)
#     knn = KNeighborsClassifier(n_neighbors = k_parameter, metric=distance_metric)
#     knn.fit(X_train,y_train)
#     y_pred = knn.predict(X_test)
# 
#       # Display model accuracy
#     accuracy = accuracy_score(y_test, y_pred)
#     st.write("#### 🎯 Model Accuracy:", np.round(accuracy, 2))
# 
#       # Convert classification report dictionary to a DataFrame
#     classification_rep = classification_report(y_test, y_pred, output_dict=True)
#     table_df = pd.DataFrame(classification_rep).transpose()
#       
#       # Convert float values to string with 2 decimal places for formatting
#     table_df['precision'] = table_df['precision'].apply(lambda x: f"{x:.2f}")
#     table_df['recall'] = table_df['recall'].apply(lambda x: f"{x:.2f}")
#     table_df['f1-score'] = table_df['f1-score'].apply(lambda x: f"{x:.2f}")
#       
#       # Display the classification report as a table
#     st.markdown("#### 📊 Classification Report:")
#     st.table(table_df.style.set_caption("").hide_index())
#     
#     if selected_dependent == 'Hotel Type':
#       st.info("Note that value **0** corresponds to **City Hotel**, and value **1** corresponds to **Resort Hotel**.")
#     else:
#         st.info("Note that value **0** corresponds to **Is Not Canceled**, and value **1** corresponds to **Is Canceled**.")
# 
#     error_rate = []
# 
#     for i in range(1,40):
#       knn = KNeighborsClassifier(n_neighbors=i)
#       knn.fit(X_train,y_train)
#       pred_i = knn.predict(X_test)
#       error_rate.append(np.mean(pred_i != y_test))
# 
#     ## Error rate
#     st.write('##### Displaying error rate with a line chart') 
#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.plot(range(1, 40), error_rate, color='blue', linestyle='dashed', marker='o', markerfacecolor='red', markersize=10)
#     ax.set_title('Error Rate vs. K Value')
#     ax.set_xlabel('K')
#     ax.set_ylabel('Error Rate')
#     st.pyplot(fig)
#     st.warning('Adjust your input K according to this model to get a better accuracy score. **Hint**: Use the elbow method to select the optimal number of clusters for KNN clustering!')
#     
#     st.markdown("##### P-values of predictor variables:")
#     logit_model = sm.Logit(y, X)
#     result = logit_model.fit()
#     p_values = result.pvalues
#     st.table(p_values)
# 
#     if selected_dependent == 'Hotel Type':
# 
#       ## Confusion matrix
#       cm = confusion_matrix(y_test, y_pred)
#       label_names = ['City Hotel', 'Resort Hotel']
#       sns.heatmap(cm, annot = True, fmt = 'g', xticklabels = label_names, yticklabels = label_names)
#       plt.xlabel('Predicted')
#       plt.ylabel('Actual')
#       plt.title('Confusion Matrix')
# 
# 
#       info_text = '''
#       **Interpreting the confusion matrix:**
# 
#       The confusion matrix summarizes the performance of a classification model by
#       showing the number of true and false positives and negatives for each class.
# 
#       - True positives: the number of instances that were correctly predicted as positive.
#       - False positives: the number of instances that were incorrectly predicted as positive.
#       - True negatives: the number of instances that were correctly predicted as negative.
#       - False negatives: the number of instances that were incorrectly predicted as negative.
# 
#       The confusion matrix can be used to calculate various performance metrics for the model,
#       such as accuracy, precision, recall, and F1 score. These metrics can help to evaluate
#       the overall effectiveness of the model and identify areas for improvement.
#       '''
#       st.markdown(f'#### ⚙️ Confusion matrix with KNN algorithm and {distance_metric} distance metric:')
#       st.info(info_text)
#       st.pyplot(plt.gcf())
# 
#     else:
# 
#       ## Confusion matrix
#       cm = confusion_matrix(y_test, y_pred)
#       label_names = ['Is Not Canceled', 'Is Canceled']
#       sns.heatmap(cm, annot = True, fmt = 'g', xticklabels = label_names, yticklabels = label_names)
#       plt.xlabel('Predicted')
#       plt.ylabel('Actual')
#       plt.title('Confusion Matrix')
# 
#       info_text = '''
#       **Interpreting the confusion matrix:**
# 
#       The confusion matrix summarizes the performance of a classification model by
#       showing the number of true and false positives and negatives for each class.
# 
#       - True positives: the number of instances that were correctly predicted as positive.
#       - False positives: the number of instances that were incorrectly predicted as positive.
#       - True negatives: the number of instances that were correctly predicted as negative.
#       - False negatives: the number of instances that were incorrectly predicted as negative.
# 
#       The confusion matrix can be used to calculate various performance metrics for the model,
#       such as accuracy, precision, recall, and F1 score. These metrics can help to evaluate
#       the overall effectiveness of the model and identify areas for improvement.
#       '''
#       st.markdown(f'#### ⚙️ Confusion matrix with KNN algorithm and {distance_metric} distance metric:')
#       st.info(info_text)
#       st.pyplot(plt.gcf())
# 
#     ## ROC curve
#     probas = knn.predict_proba(X_test)[:, 1]
#     fpr, tpr, thresholds = roc_curve(y_test, probas)
#     roc_auc = auc(fpr, tpr)
#     fig, ax = plt.subplots()
#     ax.plot(fpr, tpr, lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
#     ax.plot([0, 1], [0, 1], 'k--', lw=2)
#     ax.set_xlim([0.0, 1.0])
#     ax.set_ylim([0.0, 1.05])
#     ax.set_xlabel('False Positive Rate')
#     ax.set_ylabel('True Positive Rate')
#     ax.set_title('Receiver Operating Characteristic')
#     ax.legend(loc="lower right")
#     st.markdown("#### ⚙️ ROC curve:")
#     st.info("The ROC curve is a graphical representation of the performance of a binary classifier at different decision thresholds. It is created by plotting the true positive rate (TPR) against the false positive rate (FPR) at various threshold settings. AUC (Area Under the Curve) is a single number that summarizes the ROC curve performance. AUC ranges from 0 to 1, with higher values indicating better performance. AUC of 0.5 represents a random guess, while an AUC of 1.0 represents a perfect classifier. You can use the ROC curve to compare the performance of different classifiers or to choose the best threshold for your classifier based on your specific needs.")
#     st.pyplot(fig)
# 
#   except ValueError:
#     st.error("Please select at least one explanatory variable!")
# 
# 
# ## Performance metrics
# st.write('#### 🚀 Execution Time:')
# start_time = timeit.default_timer()
# end_time = timeit.default_timer()
# elapsed_time = end_time - start_time
# st.success(f'{elapsed_time:.4f} seconds')
# 
# st.write('#### 🌱 Emissions Tracker:')
# tracker = OfflineEmissionsTracker(country_iso_code="FRA") # FRA = France
# tracker.start()
# results = tracker.stop()
# st.success('%.12f kWh' % results)
# 
# 
# 
# 
#

!streamlit run app.py & npx localtunnel --port 8501

!pip freeze > requirements.txt