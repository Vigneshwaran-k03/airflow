import polars as pl

def transform_teract_translations_data(lf: pl.LazyFrame) -> pl.LazyFrame:
    lf = lf.with_columns(
        [
            pl.col("id").cast(pl.Utf8),
            pl.col("fr").fill_null(""),
            pl.col("en").fill_null(""),
            pl.col("es").fill_null(""),
            pl.col("po").fill_null(""),
            pl.col("de").fill_null(""),
            pl.col("gr").fill_null(""),
            pl.col("cn").fill_null(""),
            pl.col("ru").fill_null(""),
            pl.col("ne").fill_null(""),
            pl.col("it").fill_null(""),
            pl.col("pl").fill_null(""),
            pl.col("hu").fill_null(""),
            pl.col("sk").fill_null(""),
            pl.col("cs").fill_null(""),
            pl.col("hr").fill_null(""),
            pl.col("ro").fill_null(""),
            pl.col("bg").fill_null(""),
            pl.col("id_type").cast(pl.Int32),
            pl.col("table").fill_null(""),
            pl.col("field").fill_null(""),
            pl.col("status").fill_null(""),
            pl.col("target").cast(pl.Utf8).fill_null(""),
        ]
    )
    return lf
