# Product Data Generator

Generates sample product data for automotive storage products using the Anthropic Claude API. The script creates a CSV file with realistic product names, descriptions, and other attributes according to specified business rules.

## Setup

1. Clone this repository:
```bash
git clone [repository-url]
cd product-generator
```

2. Create a Python virtual environment:
```bash
# On macOS/Linux:
python -m venv .venv
source .venv/bin/activate

# On Windows:
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your Anthropic API key:
```
ANTHROPIC_API_KEY=your-api-key-here
BATCH_SIZE=5               # Optional (default: 5)
NUM_PRODUCTS=50           # Optional (default: 50)
OUTPUT_FILE=products.csv  # Optional (default: generated_products.csv)
```

## Usage

1. Activate the virtual environment (if not already activated):
```bash
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

2. Run the script:
```bash
python generator.py
```

The script will generate products according to the specifications and save them to a CSV file.

## Notes

- The script uses Claude 3 Haiku for cost-effective text generation
- Products are generated in batches to respect API rate limits
- Generated data follows specified rules for prices, categories, and inventory
- Each run creates unique SKUs and product names