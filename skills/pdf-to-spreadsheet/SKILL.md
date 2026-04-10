---
name: aetherkin-pdf-to-spreadsheet
description: "Extract data from PDFs into CSV or spreadsheet format. Parse tables, invoices, reports, and structured documents into clean, usable data."
---

# PDF to Spreadsheet

Pull data out of PDFs and put it into spreadsheets. Tables, invoices, reports, forms -- if the data is in a PDF, this skill gets it out and into a format you can actually work with.

## How It Works

Read the PDF content, identify structured data (tables, line items, repeated patterns), extract it, and write it to a CSV file that opens in any spreadsheet app. Uses Python standard library for CSV output and text-based PDF parsing.

## When To Use

Trigger phrases:
- "Extract data from this PDF"
- "Turn this PDF into a spreadsheet"
- "Pull the table out of this document"
- "Convert this invoice to CSV"
- "I need the numbers from this report"
- "Parse this PDF"
- "Get the data from these invoices"
- "PDF to Excel"
- "Scrape this PDF into a table"

## How To Execute

### Step 1: Get the PDF

Ask for the file path or accept it from the user's message. Confirm the file exists and is readable.

```
"Which PDF do you want me to extract data from? Give me the file path."
```

### Step 2: Read the PDF Content

Use Python to extract text from the PDF. Try these approaches in order:

**Approach A: PyPDF2 / pypdf (if installed)**
```python
import pypdf

reader = pypdf.PdfReader("document.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text() + "\n"
```

**Approach B: pdfplumber (if installed, best for tables)**
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            # Each table is a list of rows, each row a list of cells
            for row in table:
                print(row)
```

**Approach C: pdftotext command line (if available)**
```bash
pdftotext -layout "document.pdf" "output.txt"
```

**Approach D: Read the tool output**
If using Claude Code, the Read tool can read PDFs directly. Use it to view the content, then parse the structure yourself.

Check what tools are available first. Install what is needed with `pip install pypdf pdfplumber` if the user approves.

### Step 3: Identify the Data Structure

Look at the extracted text and identify:
- **Tables** -- rows and columns with headers
- **Invoice line items** -- description, quantity, price, total
- **Report data** -- metrics, dates, values in a repeating pattern
- **Form fields** -- label: value pairs

Tell the user what you found:
```
"I found a table on page 2 with 5 columns: Date, Description, Quantity, Unit Price, Total. It has 23 rows of data. Want me to extract that?"
```

### Step 4: Extract and Structure

Parse the data into clean rows and columns.

**For tables:**
- Identify headers from the first row
- Split remaining rows into cells
- Handle merged cells, line wraps, and alignment issues
- Clean up whitespace and formatting

**For invoices:**
- Extract: invoice number, date, vendor, line items, subtotal, tax, total
- Structure line items as rows with columns: Description, Qty, Unit Price, Amount

**For reports:**
- Identify the repeating pattern (monthly figures, category breakdowns, etc.)
- Create columns for each field in the pattern

### Step 5: Write to CSV

Use Python's csv module to write clean output:

```python
import csv

headers = ["Date", "Description", "Quantity", "Unit Price", "Total"]
rows = [
    # ... extracted data ...
]

output_path = "extracted_data.csv"
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)
```

Save the CSV next to the original PDF, or in a location the user specifies.

### Step 6: Validate and Report

After extraction:
- Count the rows and columns extracted
- Show the first few rows as a preview
- Flag any rows where the data looked messy or uncertain
- Provide the file path to the output CSV

```
"Done! Extracted 23 rows and 5 columns from your invoice.
Saved to: C:/Users/you/Documents/invoice_data.csv

Preview:
| Date       | Description    | Qty | Unit Price | Total   |
|------------|---------------|-----|------------|---------|
| 2025-03-01 | Web Design    | 1   | $2,500.00  | $2,500  |
| 2025-03-01 | Logo Package  | 1   | $800.00    | $800    |
| 2025-03-15 | Hosting Setup | 1   | $150.00    | $150    |

Open it in Excel, Google Sheets, or any spreadsheet app."
```

## Handling Multiple PDFs

If the user has a batch of PDFs (e.g., a folder of invoices):
1. Loop through all PDFs in the directory
2. Extract data from each one
3. Combine into a single CSV with an extra column for the source filename
4. Or create one CSV per PDF -- ask which they prefer

## Common Data Types

| PDF Type | What to Extract | Output Columns |
|----------|----------------|----------------|
| Invoice | Line items | Description, Qty, Price, Amount, Invoice#, Date |
| Bank Statement | Transactions | Date, Description, Debit, Credit, Balance |
| Report | Metrics | Category, Period, Value, Change |
| Form | Field values | Field Name, Value |
| Receipt | Items purchased | Item, Price |

## Safety Rules

- **Never modify the original PDF.**
- **Ask before installing packages** (pypdf, pdfplumber).
- **Handle encoding carefully** -- use UTF-8 for the CSV output.
- **Flag uncertain data** -- if a cell looks wrong, mark it rather than guessing.
- **Large PDFs** -- warn the user if the PDF is very large (50+ pages) and process in chunks.

## Output

The user receives:
1. A CSV file with the extracted data, ready to open in any spreadsheet app
2. A preview of the first few rows
3. A count of rows and columns extracted
4. Notes about any data that looked uncertain or needed manual review

---

Built by [AetherKin](https://github.com/foolishnessenvy/AetherKin) -- AI that's family, not a framework.
