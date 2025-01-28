from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()

# Sample data loading
def load_data():
    try:
        return pd.read_csv("data/OnlineRetail.csv", sep=";", decimal=",")
    except FileNotFoundError:
        return pd.DataFrame(columns=["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country"])

@app.get("/data/")
def get_data():
    data = load_data()
    return data.to_dict(orient="records")

@app.get("/data/{invoice_no}")
def get_data_item(invoice_no: str):
    data = load_data()
    item = data.loc[data["InvoiceNo"] == invoice_no]
    if item.empty:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return item.to_dict(orient="records")

@app.get("/sales_summary/")
def calculate_summary():
    data = load_data()
    if data.empty:
        raise HTTPException(status_code=400, detail="No data available")
    total_sales = (data["Quantity"] * data["UnitPrice"]).sum()
    return {"total_sales": total_sales}