import typing as tp

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score
from catboost import CatBoostClassifier
from sklift.models import SoloModel, TwoModels


Model = tp.Literal["solo-model"] | tp.Literal["two-model"]


def get_data(train_size: float):
    df_features = pd.read_parquet("./data/df_features.parquet")
    df_train = pd.read_parquet("./data/df_train.parquet")

    indices_learn, indices_test = train_test_split(
        df_train.index, train_size=train_size, random_state=0
    )

    X_train = df_features.loc[indices_learn, :]
    y_train = df_train.loc[indices_learn, "target"]
    treat_train = df_train.loc[indices_learn, "treatment_flg"]

    X_test = df_features.loc[indices_test, :]
    y_test = df_train.loc[indices_test, "target"]
    treat_test = df_train.loc[indices_test, "treatment_flg"]

    return X_train, y_train, treat_train, X_test, y_test, treat_test


def train_model(m: Model, X_train, y_train, treat_train):
    params = {
        "iterations": 20,
        "thread_count": 2,
        "random_state": 42,
        "silent": True,
    }
    if m == "solo":
        init_model = SoloModel(estimator=CatBoostClassifier(**params))

        model = init_model.fit(
            X_train,
            y_train,
            treat_train,
            estimator_fit_params={"cat_features": ["gender"]},
        )
    elif m == "two":
        init_model = TwoModels(
            estimator_trmnt=CatBoostClassifier(**params),
            estimator_ctrl=CatBoostClassifier(**params),
            method="vanilla",
        )

        model = init_model.fit(
            X_train,
            y_train,
            treat_train,
            estimator_trmnt_fit_params={"cat_features": ["gender"]},
            estimator_ctrl_fit_params={"cat_features": ["gender"]},
        )

    return model


def get_precision_score(m: Model, train_size: float):
    X_train, y_train, treat_train, X_test, y_test, _ = get_data(train_size)
    model = train_model(m, X_train, y_train, treat_train)

    preds = model.predict(X_test)
    return precision_score(y_test, preds)
