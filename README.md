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

4. Create a `.env` file with your API key:
```
ANTHROPIC_API_KEY=your-api-key-here
```

5. Review and customize `config.yaml` if needed:
```yaml
categories:
  - "Automotive/Storage/Roof Trays/Alpha Platform"
  - "Automotive/Storage/Roof Trays/Beta Platform"
  # ... other categories ...

brands:
  - "LoadMaster"
  - "RackTec"
  # ... other brands ...
```

## Configuration

The generator uses two configuration sources:

### Environment Variables (`.env`)
- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)

### Product Configuration (`config.yaml`)
- `categories`: List of available product categories
- `brands`: List of available brand names

You can modify the `config.yaml` file to customize the available categories and brands without changing the code.

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
# Run with default settings (50 products, batch size 5)
python generator.py

# Or specify custom parameters
python generator.py --num-products 10 --output-file products.csv
```

Or use the generator programmatically with custom parameters:

```python
generator = ProductGenerator(batch_size=10)
await generator.generate_products(
    num_products=100,
    output_file='custom_products.csv'
)
```

### Parameters

- `batch_size`: Number of products to generate in parallel (default: 5)
- `num_products`: Total number of products to generate (default: 50)
- `output_file`: Path to output CSV file (default: 'generated_products.csv')

## Notes

- The script uses Claude 3 Haiku for cost-effective text generation
- Products are generated in batches to respect API rate limits
- Generated data follows specified rules for prices, categories, and inventory
- Each run creates unique SKUs and product names
- Configuration can be customized via `config.yaml`