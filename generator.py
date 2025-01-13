import csv
import random
import string
import os
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Optional
from anthropic import Anthropic
import slugify
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if not ANTHROPIC_API_KEY:
    raise ValueError("Please set ANTHROPIC_API_KEY in your .env file")

MODEL = "claude-3-haiku-20240307"
BATCH_SIZE = int(os.getenv('BATCH_SIZE', '5'))  # Default to 5 if not specified

# Constants from specification
BRANDS = ["LoadMaster", "RackTec", "CargoForce", "SkyMount", "TerraRack"]

CATEGORIES = [
    "Automotive/Storage/Roof Trays/Alpha Platform",
    "Automotive/Storage/Roof Trays/Beta Platform",
    "Automotive/Storage/Roof Trays/Platform Accessories",
    "Automotive/Storage/Roof Trays/Roof Top Tents",
    "Automotive/Storage/Roof Trays/Luggage Bags",
    "Automotive/Storage/Roof Trays/Roof Baskets",
    "Automotive/Storage/Roof Trays/Roof Boxes",
    "Automotive/Storage/Roof Trays/Complete Kits",
    "Automotive/Storage/Roof Racks/Cross Bar Roof Racks",
    "Automotive/Storage/Roof Racks/Canopy Roof Systems",
    "Automotive/Storage/Roof Racks/Load Securing",
    "Automotive/Storage/Ute Tub Racks/Sigma-Deck",
    "Automotive/Storage/Ute Tub Racks/Sigma-Deck Accessories",
    "Automotive/Storage/Sport & Awnings/Awnings",
    "Automotive/Storage/Sport & Awnings/Bike Carriers",
    "Automotive/Storage/Sport & Awnings/Water Sports",
    "Automotive/Storage/Sport & Awnings/Snow Sports",
    "Automotive/Storage/Work Solutions/Conduit & Carriers",
    "Automotive/Storage/Work Solutions/Complete Ladder Carriers",
    "Automotive/Storage/Work Solutions/Ladder Carrier Accessories",
    "Automotive/Storage/Work Solutions/Ladder Rack Rails",
    "Automotive/Storage/Work Solutions/Ladder & Roof Rack Rollers",
    "Automotive/Storage/Spares, Brackets & Components/Brackets",
    "Automotive/Storage/Spares, Brackets & Components/Fitting Kits",
    "Automotive/Storage/Spares, Brackets & Components/Spare Parts",
    "Automotive/Storage/Spares, Brackets & Components/Roof Rack Parts"
]

class ProductGenerator:
    def __init__(self):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.used_skus = set()
        
    def round_to_nearest(self, value: Decimal, base: Decimal) -> Decimal:
        """Round a value to the nearest base (e.g., 0.05)."""
        return Decimal(base * round(float(value)/float(base))).quantize(Decimal('0.01'))
    
    def generate_sku(self, product_name: str, brand: str) -> str:
        """Generate a unique SKU based on product name and brand."""
        while True:
            # Take first 3 letters of brand and product name
            prefix = ''.join(c for c in brand[:3] if c.isalpha()).upper()
            name_part = ''.join(c for c in product_name[:3] if c.isalpha()).upper()
            
            # Add 4 random digits
            number = ''.join(random.choices(string.digits, k=4))
            
            sku = f"{prefix}{name_part}{number}"
            
            if sku not in self.used_skus:
                self.used_skus.add(sku)
                return sku
    
    def generate_price(self) -> Decimal:
        """Generate a price according to the specification rules."""
        range_selector = random.random()
        
        if range_selector < 0.4:  # 40% chance $10-$50
            price = random.uniform(10, 50)
        elif range_selector < 0.8:  # 40% chance $51-$200
            price = random.uniform(51, 200)
        else:  # 20% chance $201-$500
            price = random.uniform(201, 500)
            
        return self.round_to_nearest(Decimal(str(price)), Decimal('0.05'))
    
    def generate_sale_price(self, price: Decimal) -> Optional[Decimal]:
        """Generate a sale price 10-25% less than the original price."""
        if random.random() < 0.5:  # 50% chance of having a sale price
            discount = random.uniform(0.10, 0.25)
            sale_price = price * (1 - Decimal(str(discount)))
            return self.round_to_nearest(sale_price, Decimal('0.05'))
        return None
    
    def generate_product_text(self, category: str, brand: str) -> Dict[str, str]:
        """Generate product name and description using Claude."""
        prompt = f"""Create a product name (3-50 characters) and description (50-200 characters) for an automotive storage product.
Category: {category}
Brand: {brand}

Requirements:
- Product name should be concise and descriptive
- Description should highlight key features and benefits
- No HTML allowed
- Avoid special characters
- Keep it professional and technical

Format the response as:
Name: [product name]
Description: [product description]"""

        response = self.client.messages.create(
            model=MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        name_line = next(line for line in content.split('\n') if line.startswith('Name:'))
        desc_line = next(line for line in content.split('\n') if line.startswith('Description:'))
        
        return {
            'name': name_line.replace('Name:', '').strip(),
            'description': desc_line.replace('Description:', '').strip()
        }
    
    def should_have_multiple_categories(self, category: str) -> bool:
        """Determine if a product should have multiple categories."""
        # 20% chance of multiple categories, with logical constraints
        if random.random() > 0.2:
            return False
            
        # Check if the category is eligible for multiple categories
        if "Spares, Brackets & Components" in category or "Platform Accessories" in category:
            return True
            
        return False
    
    def get_additional_category(self, primary_category: str) -> str:
        """Get a logical additional category based on the primary category."""
        if "Spares, Brackets & Components" not in primary_category:
            return "Automotive/Storage/Spares, Brackets & Components/Spare Parts"
        
        # If already in spares, pick a relevant main category
        main_categories = [cat for cat in CATEGORIES if "Spares, Brackets & Components" not in cat]
        return random.choice(main_categories)
    
    async def generate_product(self) -> Dict:
        """Generate a single product entry."""
        brand = random.choice(BRANDS)
        category = random.choice(CATEGORIES)
        
        # Generate name and description using Claude
        text_content = self.generate_product_text(category, brand)
        name = text_content['name']
        description = text_content['description']
        
        # Generate price and sale price
        price = self.generate_price()
        sale_price = self.generate_sale_price(price)
        
        # Generate other fields
        track_inventory = 'Y' if random.random() < 0.9 else 'N'
        stock_level = random.randint(0, 1000) if track_inventory == 'Y' else None
        
        # Handle multiple categories
        if self.should_have_multiple_categories(category):
            additional_category = self.get_additional_category(category)
            category = f"{category};{additional_category}"
        
        # Generate SKU and URL
        sku = self.generate_sku(name, brand)
        url = f"/products/{slugify.slugify(name)}-{sku.lower()}"
        
        return {
            "Product Name": name,
            "Product Code/SKU": sku,
            "Brand Name": brand,
            "Product Description": description,
            "Price": float(price),
            "Sale Price": float(sale_price) if sale_price else "",
            "Product Weight": round(random.uniform(0.5, 20.0), 1),
            "Track Inventory": track_inventory,
            "Current Stock Level": stock_level if stock_level is not None else "",
            "Category": category,
            "Product URL": url,
            "Page Title": name,
            "Item Type": "Product",
            "Product Type": "P",
            "Allow Purchases?": "Y",
            "Product Visible?": "Y"
        }
    
    async def generate_products(self, num_products: int, output_file: str):
        """Generate multiple products and save to CSV."""
        print(f"Generating {num_products} products...")
        products = []
        
        # Process in batches to manage API rate limits
        async def process_batch(batch_size):
            batch_products = []
            tasks = [self.generate_product() for _ in range(batch_size)]
            results = await asyncio.gather(*tasks)
            batch_products.extend(results)
            return batch_products
        
        # Process all products in batches
        for i in range(0, num_products, BATCH_SIZE):
            batch_size = min(BATCH_SIZE, num_products - i)
            batch_products = await process_batch(batch_size)
            products.extend(batch_products)
            print(f"Generated {len(products)}/{num_products} products")
            
            # Add a small delay between batches to respect rate limits
            if i + BATCH_SIZE < num_products:
                await asyncio.sleep(1)
        
        # Write to CSV
        if products:
            fieldnames = products[0].keys()
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(products)
            print(f"Successfully wrote {len(products)} products to {output_file}")

async def main():
    try:
        generator = ProductGenerator()
        await generator.generate_products(
            num_products=int(os.getenv('NUM_PRODUCTS', '50')),  # Default to 50 if not specified
            output_file=os.getenv('OUTPUT_FILE', 'generated_products.csv')  # Default filename if not specified
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())