import tabula

# extract table
dfs = tabula.read_pdf("05082025 USD.pdf", pages="1", multiple_tables=True)

for i, df in enumerate(dfs):
    print(df)
    df.to_excel("USD.xlsx", sheet_name=f"Table_{i+1}", index=False)

print("Saved to output.xlsx")
