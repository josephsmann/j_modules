import pandas as pd
import numpy as np
from pandas import MultiIndex as MI
#
# this currently nukes the existing orthogonal index, pls fix
def weave_from_d(df_label_d, axis = 0):
    """df_label_d should be a dictionary of labels and dataframes
    if axis is 0 then rows are interleaved otherwise
    columns are interleaved
    returns a dataframe where each row is the has a subindex for
    each of dataframes in df_label_d with the label from the same."""

    assert( axis in [0,1])
    shape_l = np.array([df.shape[1-axis] for df in df_label_d.values()])
    index_l = [df.axes[1-axis] for df in df_label_d.values()]
#     assert(all([idx == index_l[0] for idx in index_l]))
    assert (shape_l.max() == shape_l.min())

    ndx_l = [(pd.MultiIndex.from_product([df.axes[axis], [label]]), df)
             for label, df in df_label_d.items()]

    if axis==0:
        df_l = [pd.DataFrame(df.values, index=ndx, columns=index_l[0]) for ndx, df in ndx_l]
    else:
        df_l = [pd.DataFrame(df.values, columns=ndx, index=index_l[0]) for ndx, df in ndx_l]

    return pd.concat(df_l, axis=axis).sortlevel(axis=axis)
