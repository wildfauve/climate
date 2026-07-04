import marimo

__generated_with = "0.23.11"
app = marimo.App()


@app.cell
def _():
    import pendulum
    import polars as pl

    df = pl.read_parquet("./tmp/2.parquet").sort("RecordedFor")
    return df, pl


@app.cell
def _(df):
    df
    return


@app.cell
def _(df, pl):
    df.group_by(pl.col("Locale")).len()
    return


@app.cell
def _(df, pl):
    sirocco = "Siroccoscape"
    fydoro = "Fydoro Folly"
    portico = "Wivenhoe Garden Portico"
    # df.filter(pl.col('Locale') == sirocco)
    df.group_by(pl.col("RecordedFor")).len().filter(pl.col("len") != 3)
    # df.group_by(pl.col('RecordedFor')).len()
    # df.filter(pl.col('RecordedFor') == pendulum.parse("2026-06-09"))
    return


if __name__ == "__main__":
    app.run()
