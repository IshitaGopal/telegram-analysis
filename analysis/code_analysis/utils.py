import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def make_subplots(
    num_subplots,
    ncols,
    nrows,
    figsize,
    df,
    grouping_var,
    x,
    y,
    logy=False,
    y_limit_same=True,
    xlabel="",
    ylabel="",
    title="",
):

    N = num_subplots
    fig, axs = plt.subplots(
        ncols=ncols, nrows=nrows, layout="constrained", figsize=figsize
    )
    # Set y_lim for subplots
    if y_limit_same == True:
        ylim = (df[y].min(), df[y].max())
    else:
        ylim = None

    for (gp_name, gp_df), ax in zip(df.groupby(grouping_var), axs.flat):
        gp_df.plot(
            # sharex=True,
            x=x,
            y=y,
            ax=ax,
            subplots=True,
            logy=logy,
            xlim=(df[x].min(), df[x].max()),
            ylim=ylim,
            xlabel="",
            legend=False,
        )
        ax.set_title(f"{gp_name}")
    for axis in axs.flatten():
        plt.sca(axis)
        plt.xticks(rotation=45)

    fig.suptitle(title, fontsize=16)
