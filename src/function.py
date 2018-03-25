import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

def standard_confusion_matrix(y_true,y_predict):
    tp = np.sum((y_predict == 1) & (y_predict == y_true))
    fp = np.sum((y_predict == 1) & (y_true == 0))
    fn = np.sum((y_predict == 0) & (y_true == 1))
    tn = np.sum((y_predict == 0) & (y_true == y_predict))
    confusion_matrix = np.array([[tp,fn],[fp,tn]])
    return confusion_matrix,fp,tp
    # """Make confusion matrix with format:
    #               -----------
    #               | TP | FP |
    #               -----------
    #               | FN | TN |
    #               -----------
    # Parameters
    # ----------
    # y_true : ndarray - 1D
    # y_pred : ndarray - 1D
    # Returns
    # -------
    # ndarray - 2D
    # """
    # [[tn, fp], [fn, tp]] = confusion_matrix(y_true, y_pred)
    # return np.array([[tp, fp], [fn, tn]])

def profit_curve(cost_benefit, predicted_probs, labels):
    '''
    INPUTS:
    cost_benefit: your cost-benefit matrix
    predicted_probs: predicted probability for each datapoint (between 0 and 1)
    labels: true labels for each data point (either 0 or 1)

    OUTPUTS:
    array of profits and their associated thresholds
    '''
    idx = np.argsort(predicted_probs)
    predicted_probs= predicted_probs[idx]
    #predicted_probs = np.insert(predicted_probs,-1,1)

    labels = labels[idx]
    pred_temp = np.zeros(len(labels))
    thresholds = predicted_probs
    thresholds = np.insert(predicted_probs,0,0)

    cost = []
    for thresh in thresholds:

        pred_temp = np.zeros(len(labels))
        pred_temp[predicted_probs > thresh] = 1
        pred_temp[predicted_probs <= thresh] = 0
        conf, fpr,tpr,= standard_confusion_matrix(np.array(labels),np.array(pred_temp))

        cost.append(np.sum((conf*cost_benefit))/len(labels))


    return (np.array([cost,thresholds]))

def plot_profit_curve(model, cost_benefit, X_train, X_test, y_train, y_test,ax):
    model = model
    model.fit(X_train,y_train)
    test_probs = model.predict_proba(X_test)
    profits = profit_curve(cost_benefit, test_probs[:,1], y_test.values)
    profits = list(reversed(profits[0,:]))
    p = np.linspace(0,len(profits)/8,len(profits))

    ax.plot(p,profits,label=model.__class__.__name__)
    ax.grid(alpha = .4,color = 'r',linestyle = ':')
    ax.set_xlabel('Percentage of Test instances (decreasing by score)')
    ax.set_ylabel('Profit')
    ax.set_title('Profit Curves')
    return model.predict(X_test),profits,p
<<<<<<< HEAD
=======
    
>>>>>>> de88450e8033c88d78f22cdf1a90fb544486e31e
