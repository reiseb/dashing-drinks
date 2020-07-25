# dashing-drinks

A dashboard to visualize purchases with the [barcodeRaspi](https://github.com/matthiasroos/barcodeRaspi) project by [matthiasroos](https://github.com/matthiasroos).

Requires access to the files `produkt.txt` and `purchase.txt` created by barcodeRaspi.

## Installation

1. Clone
```bash
git clone https://github.com/reiseb/dashing-drinks.git
cd dashing-drinks
```

2. Install dependencies
```bash
conda env create -n drinks -f environment.yml
conda activate drinks
```

3. Create file `.env` containing the path to the data files created by [barcodeRaspi](https://github.com/matthiasroos/barcodeRaspi)
```bash
PRODUCT_FILE="/path/to/produkt.txt"
PURCHASE_FILE="/path/to/purchase.txt"
```

4. Start the server
```bash
python index.py
```
