import numpy as np

from sklearn.metrics import accuracy_score
from catboost import CatBoostClassifier, Pool, cv


def cat_boost(X, y, X_train, y_train, X_validation, y_validation):
    model = CatBoostClassifier(
        custom_loss=['Accuracy'],
        random_seed=42,
        logging_level='Silent'
    )

    model.fit(
        X_train, y_train,
        # cat_features=categorical_features_indices,
        eval_set=(X_validation, y_validation),
        logging_level='Verbose',  # you can uncomment this for text output
        # plot=True
    )

    # CV
    cv_params = model.get_params()
    cv_params.update({
        'loss_function': 'Logloss'
    })
    cv_data = cv(
        Pool(X, y), #, cat_features=categorical_features_indices),
        cv_params,
        plot=True
    )

    print('Best validation accuracy score: {:.2f}±{:.2f} on step {}'.format(
        np.max(cv_data['test-Accuracy-mean']),
        cv_data['test-Accuracy-std'][np.argmax(cv_data['test-Accuracy-mean'])],
        np.argmax(cv_data['test-Accuracy-mean'])
    ))







