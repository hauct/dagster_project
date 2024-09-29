import duckdb

# Kết nối đến cơ sở dữ liệu
conn = duckdb.connect(database="data/staging/data.duckdb") # assumes you're writing to the same destination as specified in .env.example

# Thực hiện các truy vấn
result_1 = conn.execute("select count(*) from trips").fetchall()
print(result_1)

result_2 = conn.execute("select count(*) from zones").fetchall()
print(result_2)

# Ngắt kết nối
conn.close()