import pandas as pd
import json
import io
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file_bytes = req.get_body()
        df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=0)

        schema = []
        for col in df.columns:
            dtype = str(df[col].dropna().infer_objects().dtype)
            schema.append({"ColumnName": col, "DataType": dtype})

        return func.HttpResponse(json.dumps(schema), mimetype="application/json")

    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
