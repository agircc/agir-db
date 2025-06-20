# Organization Model

The Organization model provides comprehensive support for storing company information, Google Place API data, and managing hierarchical relationships between organizations.

## Features

### 1. Company Information Storage
- Basic company details (name, description, type)
- Contact information (email, phone, website)
- Address and location data
- Business verification status

### 2. Google Place API Integration
- Store Google Place ID for easy API integration
- Store complete Google Place API response data in JSONB format
- Support for business hours, ratings, price levels
- Geographic coordinates (latitude, longitude)

### 3. Hierarchical Relationships
- Self-referencing parent-child relationships
- Support for complex organizational structures (groups, subsidiaries, branches)
- Utility methods for hierarchy traversal

## Model Structure

### OrganizationType Enum
```python
class OrganizationType(str, enum.Enum):
    COMPANY = "company"
    BRANCH = "branch"
    SUBSIDIARY = "subsidiary"
    DEPARTMENT = "department"
    RESTAURANT = "restaurant"
    STORE = "store"
    MUSEUM = "museum"
    HOSPITAL = "hospital"
    SCHOOL = "school"
    HOTEL = "hotel"
    BANK = "bank"
    GAS_STATION = "gas_station"
    SHOPPING_MALL = "shopping_mall"
    ENTERTAINMENT = "entertainment"
    OTHER = "other"
```

### Key Fields

#### Basic Information
- `name`: Organization name (required)
- `description`: Detailed description
- `organization_type`: Type from OrganizationType enum

#### Contact & Location
- `email`, `phone`, `website`: Contact information
- `address`, `city`, `state`, `country`, `postal_code`: Address details
- `latitude`, `longitude`: Geographic coordinates

#### Google Place Integration
- `google_place_id`: Unique Google Place identifier
- `google_place_data`: Complete API response (JSONB)
- `business_hours`: Operating hours (JSONB)
- `rating`: Google rating (0-5)
- `price_level`: Price level (0-4)

#### Hierarchy
- `parent_id`: Reference to parent organization
- `parent`: Parent organization relationship
- `children`: List of child organizations

#### Metadata
- `is_active`: Active status
- `is_verified`: Verification status
- `metadata`: Additional flexible data (JSONB)
- `created_at`, `updated_at`: Timestamps
- `created_by`: User who created the organization

## Usage Examples

### Creating a Company with Subsidiaries

```python
# Create parent company
company = Organization(
    name="Tech Corp",
    description="Technology holding company",
    organization_type=OrganizationType.COMPANY,
    email="info@techcorp.com",
    website="https://techcorp.com",
    city="San Francisco",
    country="USA"
)

# Create subsidiary
subsidiary = Organization(
    name="Tech Corp AI Division",
    organization_type=OrganizationType.SUBSIDIARY,
    parent_id=company.id,
    city="New York",
    country="USA"
)

# Create branch office
branch = Organization(
    name="Tech Corp SF Office",
    organization_type=OrganizationType.BRANCH,
    parent_id=company.id,
    address="123 Market St, San Francisco, CA 94105",
    city="San Francisco",
    country="USA"
)
```

### Google Place Integration

```python
# Create restaurant from Google Place data
restaurant = Organization(
    name="The Italian Kitchen",
    organization_type=OrganizationType.RESTAURANT,
    google_place_id="ChIJN1t_tDeuEmsRUsoyG83frY4",
    google_place_data={
        "formatted_address": "123 Main St, City, State 12345",
        "international_phone_number": "+1 555-123-4567",
        "website": "https://italiankitchen.com",
        "photos": [...],
        "reviews": [...]
    },
    business_hours={
        "monday": {"open": "11:00", "close": "22:00"},
        "tuesday": {"open": "11:00", "close": "22:00"},
        # ... other days
    },
    rating=4.5,
    price_level=2,
    latitude=40.7128,
    longitude=-74.0060
)
```

### Hierarchy Traversal

```python
# Get full hierarchy path
path = organization.get_full_hierarchy_path()
# Returns: "Tech Corp > Tech Corp AI Division > ML Research Team"

# Get all descendants
descendants = company.get_all_descendants()
# Returns list of all child organizations recursively
```

## Schema Support

The model includes comprehensive Pydantic schemas:

- `OrganizationBase`: Base schema with common fields
- `OrganizationCreate`: For creation requests
- `OrganizationUpdate`: For update requests
- `OrganizationDTO`: Standard response schema
- `OrganizationDetail`: With hierarchical information
- `OrganizationBrief`: Minimal information for listings
- `OrganizationTree`: Tree representation
- `GooglePlaceInfo`: Google Place API data structure
- `OrganizationSearchFilters`: Search and filter options

## Database Migration

Run the migration to create the organizations table:

```bash
alembic upgrade head
```

The migration creates:
- `organizations` table with all fields
- Indexes on `id`, `name`, `google_place_id`, and `parent_id`
- Foreign key constraints for `parent_id` and `created_by`

## Use Cases

1. **Corporate Structure Management**: Model complex organizational hierarchies
2. **Location-Based Services**: Store and query business locations with Google Place data
3. **Directory Services**: Build comprehensive business directories
4. **Multi-tenant Applications**: Organize users and resources by organization
5. **Restaurant/Retail Chains**: Manage multiple locations with common branding
6. **Educational Institutions**: Model schools, departments, and administrative units

## Best Practices

1. **Hierarchy Depth**: Avoid overly deep hierarchies for performance
2. **Google Place Data**: Refresh periodically to keep data current
3. **Verification**: Implement verification workflows for business listings
4. **Search Optimization**: Use appropriate indexes for common query patterns
5. **Data Validation**: Validate Google Place IDs and coordinate ranges 