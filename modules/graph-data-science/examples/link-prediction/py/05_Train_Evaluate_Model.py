# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Training the machine learning model
#
# In this notebook we're going to create a machine learning model and train it against the features that we engineered in the previous notebook.
#
# We’ll be using a random forest classifier. This method is well suited as our data set will be comprised of a mix of strong and weak features. While the weak features will sometimes be helpful, the random forest method will ensure we don’t create a model that only fits our training data.

# +
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
pd.set_option('display.float_format', lambda x: '%.3f' % x)

# tag::imports[]
from sklearn.ensemble import RandomForestClassifier
# end::imports[]
# -

# Let's first load the features that we engineered in the previous notebook:

# +
# Load the CSV files saved in the train/test notebook

df_train_under = pd.read_csv("data/df_train_under_all.csv")
df_test_under = pd.read_csv("data/df_test_under_all.csv")
# -

df_train_under.sample(5)

df_test_under.sample(5)

# We can create our random forest classifier with the following code:

# tag::create-classifier[]
classifier = RandomForestClassifier(n_estimators=30, max_depth=10, random_state=0)
# end::create-classifier[]

# And now let's train the model:

# +
# tag::train-model[]
columns = [
    "cn", "pa", "tn", # graph features
    "minTriangles", "maxTriangles", "minCoefficient", "maxCoefficient", # triangle features  
    "sp", "sl" # community features
]

X = df_train_under[columns]
y = df_train_under["label"]
classifier.fit(X, y)
# end::train-model[]
# -

# Next we're going to evaluate our model and see which features are the most influential. The following two functions will help us do this:

# +
# tag::evaluation-imports[]
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
# end::evaluation-imports[]

# tag::evaluation-functions[]
def evaluate_model(predictions, actual):
    return pd.DataFrame({
        "Measure": ["Accuracy", "Precision", "Recall"],
        "Score": [accuracy_score(actual, predictions), 
                  precision_score(actual, predictions), 
                  recall_score(actual, predictions)]
    })
# end::evaluation-functions[]

def feature_importance(columns, classifier):        
    display("Feature Importance")
    df = pd.DataFrame({
        "Feature": columns,
        "Importance": classifier.feature_importances_
    })
    df = df.sort_values("Importance", ascending=False)    
    ax = df.plot(kind='bar', x='Feature', y='Importance', legend=None)
    ax.xaxis.set_label_text("")
    plt.tight_layout()
    plt.show()


# -

# Now let's see how well our model does against the test set:

# +
# tag::test-model[]
predictions = classifier.predict(df_test_under[columns])
y_test = df_test_under["label"]

evaluate_model(predictions, y_test)
# end::test-model[]
# -

evaluate_model(predictions, y_test).to_csv("data/model-eval.csv", index=False)

# 96% on all the metrics, not bad. And finally we can see which features are having the most influence:

feature_importance(columns, classifier)
