import duckdb

def run_duckdb_query(sql: str):
    conn = duckdb.connect(database=":memory:")
    try:
        df = conn.execute(sql).fetchdf()
        return df.to_dict(orient="records")
    finally:
        conn.close()