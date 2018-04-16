import pandas as pd
import numpy as np
from time import gmtime, strftime
import json
import os
# -------- BATCH -----------
def completeness_missing(df):
    """
    This function calculate the completeness considering the number of missing values

    :param df: The Dataframe to evaluate
    :return: The completeness of the provided Dataframe
    """

    tot_values = df.count().sum()
    completeness = 1 - ((pd.isna(df).sum().sum()) / tot_values)

    return completeness




def accuracy_evaluation_boolean_categ(attribute, values_range):
    """
    This function calculate the accuracy considering if each value is in the provided range.

    :param attribute: The attribute to evaluate
    :param values_range: The range of values admitted for each attribute in analysis
            e.g.:  values_range={'type': 'categ', 'interval': ['e','p']}

    :return: The accuracy of the provided attribute
    """

    accuracy_bool = []
    for row in attribute:
        if row in values_range['interval']:
            accuracy_bool.append(True)
        else:
            accuracy_bool.append(False)
    return accuracy_bool.count(True) / len(accuracy_bool)



def accuracy_evaluation_boolean_float(attribute, values_range):
    """
    This function calculate the accuracy considering if each value is in the provided range.

    :param df: The attribute to evaluate
    :param values_range: The range of values admitted for the attribute in analysis
            e.g.:  values_range={"type": "float", "interval": {"min": 5, "max": 100} }

    :return: The accuracy of the provided attribute
    """

    accuracy_bool=[]
    for row in attribute:
        if (row >=values_range['interval']['min']) & (row <= values_range['interval']['max']):
            accuracy_bool.append(True)
        else:
            accuracy_bool.append(False)
    return accuracy_bool.count(True) / len(accuracy_bool)



def accuracy_evaluation_distance(attribute, values_range):
    """
    This function calculate the accuracy considering the distance between the expected interval

    :param df: The Dataframe to evaluate
    :param eMean: The expected mean of each attribute to evaluate
    :param eInterval: the expected interval of each attribute to evaluate
    :return: The accuracy of the provided Dataframe
    """
    minV = values_range['interval']['min']
    maxV=values_range['interval']['max']
    eMean=values_range['interval']['mean']
    eInterval=maxV-minV

    accuracy_distance = []
    # accuracy max(0, 1-|(x-eMean)/(eInterval*0.5)|)    eInterval= 2*std
    for row in attribute:
        accuracy_distance.append(max(0, 1 - abs((row - eMean) / (eInterval * 0.5))))

    return np.mean(accuracy_distance)


def consistency_evaluation(df, rules):
    """
    This function calculate the consistency considering the support of the association rules provided.
    :param df: The Dataframe to evaluate
    :param rules: The association rules to use for the evaluation
    :return: The consistency of the provided Dataframe
    """

    #remove rules about not present columns
    rules_to_delete=[]
    for r in rules:
        for el in r:
            for a in el:
                if a not in df.columns:
                    rules_to_delete.append(r)
    for rul in rules_to_delete:
        try:
            rules.remove(rul)
        except:
            pass

    #if there are not association rules, return 0
    if len(rules)==0:
        print('Impossibile to evaluate consistency dimension without rules')
        return 0


    rules_consistency = []

    for r in rules:
        ant_values = []
        weighted_consistency = []
        antec = r[0]
        cons = r[1]
        for col in antec:
            ant_values.append(df[col].unique())

        # single antecedent
        if len(ant_values) == 1:
            for a1 in ant_values[0]:
                if not pd.isna(a1):
                    subset = df.loc[df[antec[0]] == a1]
                    denom = subset.shape[0]
                    numerat = max(subset[cons[0]].value_counts())
                    consistency = numerat / denom
                    weighted_consistency.append(consistency * len(subset) / len(df))

            #  print("ANTEC: ", antec[0], " = ", a1, "   consistency: ", consistency)
        # two antecedents
        else:
            for a1 in ant_values[0]:
                for a2 in ant_values[1]:
                    subset = df.loc[df[antec[0]] == a1].loc[df[antec[1]] == a2]
                    if not subset.empty:
                        denom = len(subset)
                        numerat = max(subset[cons[0]].value_counts())
                        consistency = numerat / denom
                        weighted_consistency.append(consistency * len(subset) / len(df))

                        # print("ANTEC: ", antec[0], " = ", a1, "  ", antec[1], " = ", a2, "   consistency: ",consistency)

        # consistency delle combinizioni di valori degli antecedenti di una data regola
        # print("Rule ", r, "weighted consistency: ", weighted_consistency)

        # consistency della regola (somma delle consistency pesate)
        # print("Rule ", r, "consistency: ", sum(weighted_consistency), "\n")

        rules_consistency.append(sum(weighted_consistency))

    # elenco delle consistency delle varie regole
    # print("Rules consistency: ", rules_consistency)


    consistency_dataset = sum(rules_consistency) / len(rules_consistency)

    return consistency_dataset


def completeness_frequency(time_column, frequency):
    recordCount=len(time_column)

    for time in time_column:
        time = pd.to_datetime(time)

    interval=max(time_column)-min(time_column)
    interval=interval.total_seconds()
    completeness_frequency= min(1, recordCount/(frequency*interval))

    return completeness_frequency
# ------------- STREAM ---------------

def separe_windows(df, window_size):
    number_of_windows = (df.shape[0] + (window_size - 1)) // window_size
    subsets = []
    for i in range(number_of_windows):  # create subsets of the sliding windows
        subsets.append(df.iloc[i * window_size:(i + 1) * window_size])
    return subsets


def stream_completeness_missing(df, window_size=10):

    number_of_windows = (df.shape[0] + (window_size - 1)) // window_size
    subsets=separe_windows(df, window_size)

    completeness_subsets = []
    for i in range(number_of_windows):  # completeness
        tot_values = subsets[i].count().sum()
        completeness_subset = (1 - ((pd.isna(subsets[i]).sum().sum()) / tot_values))
        weighted_completeness = (completeness_subset * (i + 1)) / number_of_windows
        completeness_subsets.append(weighted_completeness)
    completeness = 1 / (number_of_windows - ((number_of_windows - 1) / 2)) * sum(completeness_subsets)

    return completeness


def stream_accuracy_boolean_categ(attribute,values_range, window_size=10):
    number_of_windows = (attribute.shape[0] + (window_size - 1)) // window_size
    subsets=separe_windows(attribute, window_size)

    accuracy_subsets = []
    for i in range(number_of_windows):
        accuracy_subset = accuracy_evaluation_boolean_categ(subsets[i], values_range)
        weighted_accuracy = (accuracy_subset * (i + 1)) / number_of_windows
        accuracy_subsets.append(weighted_accuracy)
    accuracy = 1 / (number_of_windows - ((number_of_windows - 1) / 2)) * sum(accuracy_subsets)

    return accuracy


def stream_accuracy_boolean_float(attribute,values_range, window_size=10):
    number_of_windows = (attribute.shape[0] + (window_size - 1)) // window_size
    subsets=separe_windows(attribute, window_size)

    accuracy_subsets = []
    for i in range(number_of_windows):
        accuracy_subset = accuracy_evaluation_boolean_float(subsets[i], values_range)
        weighted_accuracy = (accuracy_subset * (i + 1)) / number_of_windows
        accuracy_subsets.append(weighted_accuracy)
    accuracy = 1 / (number_of_windows - ((number_of_windows - 1) / 2)) * sum(accuracy_subsets)

    return accuracy

def timeliness_evaluation(time_column, volatility):
    current_time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    current_time=pd.to_datetime(str(current_time))
    currencies=[]

    for time in time_column:
        time=pd.to_datetime(time)
        currencies.append(current_time-time)
    timeliness=[]
    for currency in currencies:
        timeliness.append(max(0,1-currency.total_seconds()/volatility))

    return np.mean(timeliness)



def DQEvaluator(method, attribute_list=None, filter=None):
    """
    This function evaluate the DQ of the provided dataframe wrt the dq metadata specification

    :return: the DQ dimensions evaluated
    """
    metrics = {
        'batch': {
            'global': {
                'consistency': consistency_evaluation,
                'completeness_missing': completeness_missing
            },
            'attribute': {
                'float': {
                    'accuracy': accuracy_evaluation_boolean_float},
                'timestamp': {
                    'timeliness': timeliness_evaluation},
                'categ': {
                    'accuracy': accuracy_evaluation_boolean_categ}
            }
        },
        'stream': {
            'global': {
                'completeness_missing': stream_completeness_missing,
                'consistency': consistency_evaluation
            },
            'attribute': {
                'float': {
                    'accuracy': stream_accuracy_boolean_float},
                'timestamp': {
                    'timeliness': timeliness_evaluation,
                    'completeness_frequency': completeness_frequency},
                'categ':
                    {'accuracy': stream_accuracy_boolean_categ}
            }
        }
    }






    config_dict = json.load(open("config_files/config_dictionary.json"))
    config = json.load(open("config_files/"+config_dict[method]))

    df=pd.read_csv(method)
    source_type=config['source_type']
    datatypes=config['datatypes']
    rules=config['association_rules']
    values_range=config['values_range']
    volatility=0

    try:
        volatility = config['volatility']
    except:
        pass
    try:
        frequency = config['update_frequency']
    except:
        pass


    if filter is not None:
        #   selection
        for p in filter:
            values = filter[p]
            df = df.loc[df[p].isin(values)]

    if attribute_list is not None:
        #	projection
        df = df[attribute_list]

    completeness=0
    consistency=0
    accuracy = []
    accuracy_mean = 0
    accuracy_min = 0
    accuracy_max = 0
    timeliness=0
    complet_freq=0

    # DIM GLOBALI
    for i in metrics[source_type]['global']:
        if i == 'completeness_missing':
            parameters = {'df': df}
            completeness_metric = metrics[source_type]['global'][i]
            completeness=completeness_metric(**parameters)
        if i == 'consistency':
            parameters = {'df': df, 'rules': rules}
            consistency_metric = metrics[source_type]['global'][i]
            consistency=consistency_metric(**parameters)

    #delete attribute not present in the df, from the datatypes dictionary
    attr_to_delete=[]
    for attr in datatypes:
        if attr not in df.columns:
            attr_to_delete.append(attr)
    for attr in attr_to_delete:
        try:
            datatypes.pop(attr)
        except:
            pass


    if datatypes :
        for attr in datatypes:  #cicla sugli attributi
            for dim in metrics[source_type]['attribute'][datatypes[attr]]:  #cicla sulle dimensioni da valutare sull'attributo
                if dim=='accuracy':
                    accuracy_metric = metrics[source_type]['attribute'][datatypes[attr]]['accuracy']
                    parameters = {'attribute': df[attr], 'values_range': values_range[attr]}
                    accuracy.append(accuracy_metric(**parameters))
                if dim=='timeliness':
                    if volatility!= 0:
                        time_column=pd.to_datetime(df[attr])
                        timeliness_metric = metrics[source_type]['attribute'][datatypes[attr]][
                            'timeliness']
                        parameters= {'time_column': time_column, 'volatility':volatility}
                        timeliness=timeliness_metric(**parameters)
                if dim=='completeness_frequency':
                    time_column=pd.to_datetime(df[attr])
                    completeness_frequency_metric=metrics[source_type]['attribute'][datatypes[attr]][
                        'completeness_frequency']
                    parameters = {'time_column': time_column, 'frequency': frequency}
                    complet_freq=completeness_frequency_metric(**parameters)


    if accuracy:
        accuracy_mean=np.mean(accuracy)

    if complet_freq:
        completeness=(completeness+complet_freq)/2
        
    results={'completeness': completeness,
             'consistency': consistency,
             'accuracy': accuracy_mean,
             'timeliness': timeliness
             }


    return results

