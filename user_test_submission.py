from __future__ import print_function
import pandas as pd
import numpy as np
from sklearn.model_selection import ShuffleSplit
import feature_extractor
import regressor
import time
if __name__ == '__main__':
    tic=time.time()
    print('Reading file ...')
    X_df = pd.read_csv('X_train.csv').values
    y_array = pd.read_csv('Y_train.csv').values

    skf = ShuffleSplit(n_splits=2, test_size=0.5, random_state=67)
    print('Training file ...')
    for train_is, test_is in skf.split(X_df, y_array):
        X_train_df = X_df.iloc[train_is]
        y_train_array = y_array[train_is]

        # Feature extraction
        fe = feature_extractor.FeatureExtractor()
        fe.fit(X_train_df, y_train_array)
        X_train_array = fe.transform(X_train_df)

        reg = regressor.Regressor()
        reg.fit(X_train_array, y_train_array)
        X_test_df = X_df.iloc[test_is]
        y_test_array = y_array[test_is]
        # Feature extraction
        X_test_array = fe.transform(X_test_df)

        # Regression
        y_pred_array = reg.predict(X_test_array)
        print('rmse = ', np.sqrt(
            np.mean(np.square(y_test_array - y_pred_array))))
    tac=time.time()
    print('time = ', tac-tic)
