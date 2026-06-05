import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("ETL_Engine")

def process_file(file_path, schema):
    logger.info("[►] PHASE 1: Extraction and Transformation (Pandas)")
    logger.info(f"   ├─ Reading file with format '{schema.get('file_type', 'csv')}'...")
    
    try:
        # =====================================================================
        # 0. READ LOGIC: Support for Excel and CSV
        # =====================================================================
        file_type = schema.get("file_type", "csv").lower()
        skip_rows = schema.get("skip_rows", 0)  # If not present in JSON, assume 0

        if file_type in ["xlsx", "xls"]:
            # 'sep' and 'encoding' are not normally used for Excel
            df = pd.read_excel(file_path, skiprows=skip_rows, dtype=str)
        else:
            # Traditional CSV reading
            df = pd.read_csv(
                file_path,
                sep=schema['separator'],
                encoding=schema['encoding'],
                skiprows=skip_rows,
                dtype=str
            )
            
        logger.info(f"   ├─ Dataset loaded into memory ({len(df):,} records detected). Skipping {skip_rows} rows.")
        # =====================================================================
        
        transformations = schema.get("transformations", {})

        # 1. Add dynamic columns (e.g., Date)
        if "add_columns" in transformations:
            for col_name, rules in transformations["add_columns"].items():
                if rules.get("type") == "current_date":
                    offset = rules.get("offset_days", 0)
                    calculated_date = datetime.now() + timedelta(days=offset)
                    df[col_name] = calculated_date.strftime("%Y-%m-%d")
            logger.info("   ├─ Dynamic columns generated (Dates).")

        # 2. Transform columns to standard Float
        if "column_float_list" in transformations:
            for col in transformations["column_float_list"]:
                if col in df.columns:
                    df[col] = df[col].str.replace(',', '.', regex=False)
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

        # 3. Transform columns to Integers (Int)
        if "column_int_list" in transformations:
            for col in transformations["column_int_list"]:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        # ----------------------------------------------------------------------
        # 4. Transform and round Decimal columns for SQL Server
        # ----------------------------------------------------------------------
        if "decimal_columns" in transformations:
            for col in transformations["decimal_columns"]:
                if col in df.columns:
                    # Clean commas in case numbers arrive as "1,000.50"
                    df[col] = df[col].str.replace(',', '.', regex=False)
                    # Convert to numeric, fill nulls with 0 and ROUND to 4
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0).round(4)
            logger.info("   ├─ Decimal rounding applied (Max 4 decimals).")

        # ----------------------------------------------------------------------
        # 5. Transform and standardize Dates
        # ----------------------------------------------------------------------
        if "date_columns" in transformations:
            for col in transformations["date_columns"]:
                if col in df.columns:
                    # Strip spaces and remove text nulls
                    df[col] = df[col].astype(str).str.strip()
                    df.loc[df[col] == 'nan', col] = None
                    df.loc[df[col] == '', col] = None
                    
                    # Smart conversion logic
                    try:
                        # 1. Try to force the standard YYYY-MM-DD format first
                        df[col] = pd.to_datetime(df[col], format='%Y-%m-%d', errors='raise')
                    except ValueError:
                        # 2. If it fails (e.g., comes as 25/03/2026), let Pandas infer it
                        # using the Latin format (Day first)
                        df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
                    
                    # Finally convert it to text in universal SQL format
                    df[col] = df[col].dt.strftime('%Y-%m-%d')
                    
            logger.info("   ├─ Date formatting applied (Smart detection).")
            
        # ----------------------------------------------------------------------
        # 6. Dynamic columns management (last 3 months)
        # ----------------------------------------------------------------------
        if "dynamic_columns" in transformations:
            if transformations["dynamic_columns"].get("unit_sales_last_3_months"):

                months_order = {
                    "January": 1, "February": 2, "March": 3,
                    "April": 4, "May": 5, "June": 6,
                    "July": 7, "August": 8, "September": 9,
                    "October": 10, "November": 11, "December": 12
                }

                sales_cols = [col for col in df.columns if col.startswith("UNIT_SALES_")]

                if sales_cols:
                    try:
                        # sort months
                        sorted_cols = sorted(
                            sales_cols,
                            key=lambda x: months_order.get(
                                x.replace("UNIT_SALES_", "").strip(), 0
                            )
                        )

                        # take last 3 months
                        last_3 = sorted_cols[-3:]

                        # map to fixed columns
                        df["UNIT_SALES_March"] = df[last_3[0]]
                        df["UNIT_SALES_April"] = df[last_3[1]]
                        df["UNIT_SALES_May"] = df[last_3[2]]

                        logger.info(f"   ├─ Dynamic columns processed: {last_3}")

                    except Exception as e:
                        logger.warning(f"   ├─ Error processing dynamic columns: {str(e)}")

                # guarantee columns
                # ----------------------------------------------------------------------
                for col in ["UNIT_SALES_March", "UNIT_SALES_April", "UNIT_SALES_May"]:
                    if col not in df.columns:
                        df[col] = None
                        logger.warning(f"   ├─ Missing column created: {col}")

        # Filter only the columns we are interested in according to the config
        final_columns = schema["name_columns"]
        final_df = df[final_columns].copy()
        
        # Rename columns to EXACTLY match SQL Server
        if "rename_columns" in schema:
            final_df.rename(columns=schema["rename_columns"], inplace=True)
            logger.info("   ├─ Schema Mapping applied (SQL column names).")
        
        logger.info(f"   └─ [✓] Transformation completed. Final dataset: {len(final_df):,} rows ready for injection.")
        return final_df

    except Exception as e:
        logger.error(f"   └─ [X] Data transformation failed: {str(e)}")
        raise