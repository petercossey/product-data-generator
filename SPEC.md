# Product Data Generation Specification

## Output Requirements
- Generate x number of products
- Format: CSV file
- Encoding: UTF-8
- No HTML allowed in any field

## Schema
```typescript
{
  "Product Name": string(3-50),
  "Product Code/SKU": string(unique),
  "Brand Name": enum(LoadMaster|RackTec|CargoForce|SkyMount|TerraRack),
  "Product Description": string(50-200),
  "Price": decimal(2),
  "Sale Price": decimal(2)|null,
  "Product Weight": decimal(kg),
  "Track Inventory": enum(Y|N),
  "Current Stock Level": integer|null,
  "Category": string,
  "Product URL": string,
  "Page Title": string,
  "Item Type": "Product",
  "Product Type": "P",
  "Allow Purchases?": "Y",
  "Product Visible?": "Y"
}
```

## Validation Rules

### 1. Price Rules
- All prices must round to nearest 0.05
- Sale Price must be 10-25% less than Price
- Price ranges:
  - 40% products: $10.00-$50.00
  - 40% products: $51.00-$200.00
  - 20% products: $201.00-$500.00

### 2. Inventory Rules
- 90% products: Track Inventory="Y", Stock Level=0-1000
- 10% products: Track Inventory="N", Stock Level=null
- Even distribution across categories (±10%)

### 3. Brand Distribution
- Each brand should represent ~20% of products

### 4. URL Formation
- Pattern: /products/{product-name-slugified}-{sku}
- All lowercase, hyphens for spaces
- Remove special characters

### 5. Category Assignment
- Most products (approximately 80%) should have a single category
- Multiple categories are allowed where logically appropriate (approximately 20% of products)
- When using multiple categories, separate them with semicolons (;)
- Example: "Automotive/Storage/Roof Trays/Roof Boxes;Automotive/Storage/Spares, Brackets & Components/Brackets"
- Common scenarios for multiple categories:
  - Universal fit components that work across multiple product lines
  - Spare parts that belong in both their primary category and "Spares, Brackets & Components"
  - Accessories that are compatible with multiple product lines
  - Cross-compatible mounting systems
- Never force multiple categories if it doesn't make logical sense for the product

## Available Categories
```
Automotive/Storage/Roof Trays/Alpha Platform
Automotive/Storage/Roof Trays/Beta Platform
Automotive/Storage/Roof Trays/Platform Accessories
Automotive/Storage/Roof Trays/Roof Top Tents
Automotive/Storage/Roof Trays/Luggage Bags
Automotive/Storage/Roof Trays/Roof Baskets
Automotive/Storage/Roof Trays/Roof Boxes
Automotive/Storage/Roof Trays/Complete Kits
Automotive/Storage/Roof Racks/Cross Bar Roof Racks
Automotive/Storage/Roof Racks/Canopy Roof Systems
Automotive/Storage/Roof Racks/Load Securing
Automotive/Storage/Ute Tub Racks/Sigma-Deck
Automotive/Storage/Ute Tub Racks/Sigma-Deck Accessories
Automotive/Storage/Sport & Awnings/Awnings
Automotive/Storage/Sport & Awnings/Bike Carriers
Automotive/Storage/Sport & Awnings/Water Sports
Automotive/Storage/Sport & Awnings/Snow Sports
Automotive/Storage/Work Solutions/Conduit & Carriers
Automotive/Storage/Work Solutions/Complete Ladder Carriers
Automotive/Storage/Work Solutions/Ladder Carrier Accessories
Automotive/Storage/Work Solutions/Ladder Rack Rails
Automotive/Storage/Work Solutions/Ladder & Roof Rack Rollers
Automotive/Storage/Spares, Brackets & Components/Brackets
Automotive/Storage/Spares, Brackets & Components/Fitting Kits
Automotive/Storage/Spares, Brackets & Components/Spare Parts
Automotive/Storage/Spares, Brackets & Components/Roof Rack Parts
```

## Example Products
```csv
Product Name,Product Code/SKU,Brand Name,Product Description,Price,Sale Price,Product Weight,Track Inventory,Current Stock Level,Category,Product URL,Page Title,Item Type,Product Type,Allow Purchases?,Product Visible?
"Alpha Platform X3","APX3001","LoadMaster","Heavy-duty aluminum roof platform with aerodynamic design and quick-mount system",299.95,249.95,12.5,Y,45,"Automotive/Storage/Roof Trays/Alpha Platform",/products/alpha-platform-x3-apx3001,"Alpha Platform X3","Product","P","Y","Y"
"Universal Mounting Bracket","UMB2001","RackTec","Universal fit mounting bracket compatible with all roof rack systems",45.95,39.95,0.8,Y,250,"Automotive/Storage/Roof Racks/Cross Bar Roof Racks;Automotive/Storage/Spares, Brackets & Components/Brackets",/products/universal-mounting-bracket-umb2001,"Universal Mounting Bracket","Product","P","Y","Y"
"Cargo Basket Pro","CBP2002","RackTec","Universal fit cargo basket with weather-resistant coating",89.95,,8.2,Y,122,"Automotive/Storage/Roof Trays/Roof Baskets",/products/cargo-basket-pro-cbp2002,"Cargo Basket Pro","Product","P","Y","Y"
```