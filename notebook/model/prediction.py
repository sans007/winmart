import numpy as np
import pandas as pd
import pickle

encoder = pickle.load(open("./notebook/model/dataencoder.pkl", "rb"))
scale = pickle.load(open("./notebook/model/datascaler.pkl", "rb"))
modal = pickle.load(open("./notebook/model/model.pkl", "rb"))
dfdata = pickle.load(open("./notebook/model/dfdata.pkl", "rb"))


def dataPrep(df):

    def create_item_type(df):
        df["Item_Type"] = df["Item_Identifier"].str[:2]
        df["Item_Type"] = df["Item_Type"].map(
            {"FD": "Food", "NC": "Non-Consumable", "DR": "Drinks"}
        )

        return df

    def fill_missing_value_Item_weight(df):
        Item_Id_Weight_Map = dfdata["Item_Id_Weight_Map"]
        Item_Type_Weight_Map = dfdata["Item_Type_Weight_Map"]

        # if missing fill 0 value ------------------------------------------

        zero_mask = df["Item_Weight"] == 0
        df.loc[zero_mask, "Item_Weight"] = df.loc[zero_mask, "Item_Type"].map(
            Item_Type_Weight_Map
        )

        df.loc[zero_mask, "Item_Weight"] = df.loc[zero_mask, "Item_Identifier"].map(
            Item_Id_Weight_Map
        )

        # if missing fill nan value ------------------------------------------

        df["Item_Weight"] = df["Item_Weight"].fillna(
            df["Item_Identifier"].map(Item_Id_Weight_Map)
        )

        df["Item_Weight"] = df["Item_Weight"].fillna(
            df["Item_Type"].map(Item_Type_Weight_Map)
        )

        return df

    def fill_missing_value_Outlet_size(df):
        mode_outlet_size_Map = dfdata["mode_outlet_size_Map"]

        df.loc[df["Outlet_Size"] == "", "Outlet_Size"] = df.loc[
            df["Outlet_Size"] == "", "Outlet_Type"
        ].map(mode_outlet_size_Map)

        df.loc[:, "Outlet_Size"] = df.loc[:, "Outlet_Size"].fillna(
            df.loc[:, "Outlet_Type"].map(mode_outlet_size_Map)
        )

        return df

    def standerize_fat_content(df):
        df["Item_Fat_Content"] = df["Item_Fat_Content"].replace(
            {"LF": "Low Fat", "low fat": "Low Fat", "reg": "Regular"}
        )
        return df

    def correct_fat_content(df):
        df.loc[df["Item_Type"] == "Non-Consumable", "Item_Fat_Content"] = "Non-Edible"
        return df

    original_columns = dfdata["columns"]

    df = pd.DataFrame([df])
    df = df[original_columns]
    df = create_item_type(df)
    df = fill_missing_value_Item_weight(df)
    df = fill_missing_value_Outlet_size(df)
    df = standerize_fat_content(df)
    df = correct_fat_content(df)

    return df


def catEncoder(df, encoder):

    # drop Item_Identifier as it has too mani category
    dropColumns = dfdata["drop_columns"]
    encoded_features_names = dfdata["encoded_features_names"]

    df = df.drop(columns=dropColumns)

    cat_feats = df.select_dtypes(include=["object"])

    num_feats = df.select_dtypes(exclude=["object"]).reset_index(drop=True)

    X_train_cat_encoder = pd.DataFrame(
        encoder.transform(cat_feats).toarray(), columns=encoded_features_names
    )
    df_final = pd.concat([num_feats, X_train_cat_encoder], axis=1)

    return df_final


def Prediction(df):
    data_prep = dataPrep(df)
    data_encode = catEncoder(data_prep, encoder)
    data_scale = scale.transform(data_encode)
    prediction = modal.predict(data_scale)[0]

    return round(prediction, 3)
