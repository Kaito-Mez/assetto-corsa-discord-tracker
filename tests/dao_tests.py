import pandas as pd

def load_dataframe_test(dao):
    df = dao.get_dataframe()

    #print(df)
    print(df[(df["car"] == "ks_toyota_supra_mkiv") | (df["laptime"] < 100000)])
    gtr = df[df["car"] == "bksy_nissan_skyline_r34_z_tune"]
    print(gtr)
    print(gtr[gtr["laptime"] == gtr.laptime.min()])
    