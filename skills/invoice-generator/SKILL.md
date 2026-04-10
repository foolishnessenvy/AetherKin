---
name: aetherkin-invoice-generator
description: "Generate professional HTML invoices from project data. Include line items, totals, tax, payment terms, and company info. Print to PDF from any browser."
---

# Invoice Generator

Create clean, professional invoices without paying for invoicing software. Give the agent your project details, get back an HTML invoice you can print to PDF from any browser. Handles line items, tax calculations, payment terms, and your business info.

## How It Works

The user provides project details and client info. The agent generates a complete HTML invoice file styled for print. Open it in a browser, hit Print, choose "Save as PDF." Done.

## When To Use

Trigger phrases:
- "Create an invoice"
- "Generate an invoice for..."
- "I need to bill [client name]"
- "Make an invoice"
- "Invoice this project"
- "Bill for [amount]"
- "Create a receipt"
- "I need to send an invoice"
- "Help me invoice [client]"

## How To Execute

### Step 1: Gather Invoice Details

Collect from the user (or pull from context):

**Your info (save this for reuse):**
- Business name
- Address
- Email
- Phone (optional)
- Logo URL (optional)
- Payment details (bank info, PayPal, etc.)

**Client info:**
- Client name / company
- Client address
- Client email

**Invoice details:**
- Invoice number (auto-generate if not provided: INV-YYYYMMDD-001)
- Invoice date (default: today)
- Due date (default: 30 days from today)
- Payment terms (Net 30, Due on Receipt, etc.)

**Line items:**
- Description
- Quantity
- Unit price
- Amount (qty x price)

**Tax:** Rate percentage if applicable (0% if none)

If the user gives minimal info like "Invoice Sarah at Acme Corp $2,500 for web design", fill in reasonable defaults and confirm.

### Step 2: Calculate Totals

```
Subtotal = sum of all line item amounts
Tax = subtotal * tax rate
Total = subtotal + tax
```

### Step 3: Generate the HTML Invoice

Create a complete, self-contained HTML file with inline CSS. The invoice should look professional when printed.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Invoice [NUMBER]</title>
<style>
  @media print {
    body { margin: 0; }
    .no-print { display: none; }
  }
  body {
    font-family: 'Segoe UI', Arial, sans-serif;
    max-width: 800px;
    margin: 40px auto;
    padding: 20px;
    color: #333;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 40px;
  }
  .company-name {
    font-size: 24px;
    font-weight: bold;
    color: #2c3e50;
  }
  .invoice-title {
    font-size: 32px;
    color: #2c3e50;
    text-align: right;
  }
  .invoice-number {
    text-align: right;
    color: #7f8c8d;
  }
  .addresses {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px;
  }
  .addresses div { width: 45%; }
  .label {
    font-weight: bold;
    color: #7f8c8d;
    font-size: 12px;
    text-transform: uppercase;
    margin-bottom: 5px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 30px;
  }
  th {
    background: #2c3e50;
    color: white;
    padding: 12px;
    text-align: left;
    font-size: 13px;
    text-transform: uppercase;
  }
  td {
    padding: 12px;
    border-bottom: 1px solid #ecf0f1;
  }
  tr:hover { background: #f9f9f9; }
  .totals {
    width: 300px;
    margin-left: auto;
  }
  .totals table { margin-bottom: 0; }
  .totals td {
    padding: 8px 12px;
    border: none;
  }
  .totals .total-row {
    font-size: 18px;
    font-weight: bold;
    color: #2c3e50;
    border-top: 2px solid #2c3e50;
  }
  .payment-info {
    margin-top: 40px;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 4px;
  }
  .footer {
    margin-top: 40px;
    text-align: center;
    color: #bdc3c7;
    font-size: 12px;
  }
  .print-btn {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 10px 20px;
    background: #2c3e50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
  }
</style>
</head>
<body>

<button class="print-btn no-print" onclick="window.print()">Print / Save PDF</button>

<div class="header">
  <div>
    <div class="company-name">[YOUR BUSINESS NAME]</div>
    <div>[Your Address Line 1]</div>
    <div>[Your Address Line 2]</div>
    <div>[Your Email]</div>
    <div>[Your Phone]</div>
  </div>
  <div>
    <div class="invoice-title">INVOICE</div>
    <div class="invoice-number">
      <strong>#[INVOICE-NUMBER]</strong><br>
      Date: [INVOICE-DATE]<br>
      Due: [DUE-DATE]
    </div>
  </div>
</div>

<div class="addresses">
  <div>
    <div class="label">Bill To</div>
    <div><strong>[CLIENT NAME]</strong></div>
    <div>[Client Address Line 1]</div>
    <div>[Client Address Line 2]</div>
    <div>[Client Email]</div>
  </div>
  <div>
    <div class="label">Payment Terms</div>
    <div>[NET 30 / DUE ON RECEIPT / etc.]</div>
  </div>
</div>

<table>
  <thead>
    <tr>
      <th>Description</th>
      <th style="text-align:center">Qty</th>
      <th style="text-align:right">Unit Price</th>
      <th style="text-align:right">Amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Item description]</td>
      <td style="text-align:center">[qty]</td>
      <td style="text-align:right">$[price]</td>
      <td style="text-align:right">$[amount]</td>
    </tr>
    <!-- Repeat for each line item -->
  </tbody>
</table>

<div class="totals">
  <table>
    <tr>
      <td>Subtotal</td>
      <td style="text-align:right">$[SUBTOTAL]</td>
    </tr>
    <tr>
      <td>Tax ([RATE]%)</td>
      <td style="text-align:right">$[TAX]</td>
    </tr>
    <tr class="total-row">
      <td>Total Due</td>
      <td style="text-align:right">$[TOTAL]</td>
    </tr>
  </table>
</div>

<div class="payment-info">
  <div class="label">Payment Information</div>
  <p>[Payment instructions -- bank details, PayPal, Venmo, etc.]</p>
</div>

<div class="footer">
  Thank you for your business.
</div>

</body>
</html>
```

### Step 4: Save the File

```bash
mkdir -p ~/Documents/invoices
# Save as: invoices/INV-20250410-001.html
```

Tell the user:
```
"Invoice created! Saved to: ~/Documents/invoices/INV-20250410-001.html

To get a PDF:
1. Open the file in your browser (double-click it)
2. Click the 'Print / Save PDF' button in the top right
3. Choose 'Save as PDF' as the printer
4. Done!"
```

### Step 5: Config for Repeat Use

If this is the user's first invoice, offer to save their business details for future use:

```bash
mkdir -p ~/.aetherkin
cat > ~/.aetherkin/invoice-config.json << 'CONFIG'
{
  "business_name": "Your Business Name",
  "address": "123 Main St, City, State ZIP",
  "email": "you@email.com",
  "phone": "555-0100",
  "payment_info": "Pay via Venmo @handle or bank transfer to...",
  "tax_rate": 0,
  "default_terms": "Net 30",
  "next_invoice_number": 2
}
CONFIG
```

On subsequent invoices, load this config automatically so the user only needs to provide the client and line items.

## Invoice Number Auto-Increment

Format: `INV-YYYYMMDD-NNN`

If a config file exists, read the next number, use it, and increment. If no config, start at 001.

## Safety Rules

- **Always show the invoice for review** before saving.
- **Double-check math** -- totals must add up correctly.
- **Never send invoices** on behalf of the user. Generate only.
- **Currency:** Default to USD ($). Ask if the user works in a different currency.

## Output

The user receives:
1. A professional HTML invoice file
2. Instructions on how to print it to PDF
3. A saved config for future invoices (first time only)
4. Correct math on all totals

---

Built by [AetherKin](https://github.com/foolishnessenvy/AetherKin) -- AI that's family, not a framework.
