import logging
import pandas as pd
from ast import literal_eval
from tabulate import tabulate
import re


class FwfConvertor:

    def __init__(self):
        pass

    @staticmethod
    def save_fwf_tr_data(data, text_col, labels_col, label_mapping=None):
        if label_mapping is not None:
            data[labels_col] = data[labels_col].apply(FwfConvertor.label_map_func, label_mapping=label_mapping)
        # Preprocessing df in format for fwf
        data[labels_col] = data[labels_col].apply(FwfConvertor.preprocess_fwf_func)
        # limiting only two columns in fwf file
        data = data[[labels_col, text_col]]
        # Converting to fwf format
        content = FwfConvertor.to_fwf(data)
        try:
            open('Model Training data.train', 'w').write(content)
            logging.info("FWF file saved")
        except Exception as exp:
            logging.error("File saving failed", exp)

    @staticmethod
    def label_map_func(element, label_mapping):
        return list((tag.replace(tag, label_mapping[tag])) for tag in element)

    @staticmethod
    def preprocess_fwf_func(element):
        return " ".join(element)

    @staticmethod
    def to_fwf(df):
        content = tabulate(list(df.values), list(df.columns), tablefmt="plain")
        content = content[(content.find('\n') + 1):]
        content = re.sub(' +', ' ', content)
        return content


if __name__ == '__main__':
    local_path = 'C:\\Users\\aimhe\\Text Classification Project\\Model Improvements\\data\\pizza emotion\\'
    train_data = pd.read_csv(local_path + 'train_data_pizza_emotions_df.csv', converters={"labels": literal_eval})
    label_mapping = {'joy': '__label__0',
                     'love': '__label__1',
                     'fear': '__label__2',
                     'anger': '__label__3',
                     'surprise': '__label__4',
                     'sadness': '__label__5'}
    FwfConvertor.save_fwf_tr_data(train_data, 'text', 'labels', label_mapping=None)
