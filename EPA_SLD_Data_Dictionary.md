# EPA Smart Location Database - Complete Data Dictionary

## Dataset Information
- **Source**: U.S. Environmental Protection Agency (EPA)
- **Version**: 3.0 (January 2021)
- **Geographic Level**: Census Block Groups
- **Coverage**: All 50 states + DC + Puerto Rico
- **Total Variables**: 117 original columns

---

## Understanding the 5D Framework

The EPA Smart Location Database is organized around the **5D's of the Built Environment**:

1. **D1 - Density**: How many people, jobs, and housing units per acre
2. **D2 - Diversity**: Mix of land uses and jobs-housing balance  
3. **D3 - Design**: Street network characteristics and walkability
4. **D4 - Distance to Transit**: Proximity and frequency of public transit
5. **D5 - Destination Accessibility**: Regional employment/worker reachability

These metrics are used to calculate the **National Walkability Index (NatWalkInd)**.

---

## Column Categories


### Geographic

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `OBJECTID` | Object Identifier | Unique record identifier | Integer |
| `GEOID10` | Geographic Identifier 2010 | Unique 12-digit census block group identifier (2010 Census) | String (FIPS Code) |
| `GEOID20` | Geographic Identifier 2020 | Unique 12-digit census block group identifier (2020 Census) | String (FIPS Code) |
| `STATEFP` | State FIPS Code | 2-digit state identifier | String (01-56) |
| `COUNTYFP` | County FIPS Code | 3-digit county identifier within state | String |
| `TRACTCE` | Census Tract Code | 6-digit census tract identifier | String |
| `BLKGRPCE` | Block Group Code | 1-digit block group identifier | String (1-9) |
| `CBSA` | Core Based Statistical Area Code | Metropolitan/Micropolitan Statistical Area identifier | Numeric |
| `CBSA_Name` | CBSA Name | Name of Core Based Statistical Area | Text |
| `CSA` | Combined Statistical Area Code | Larger combined metropolitan area identifier | Numeric |
| `CSA_Name` | CSA Name | Name of Combined Statistical Area | Text |

### Regional Context

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `CBSA_POP` | CBSA Population | Total population in the CBSA | Count |
| `CBSA_EMP` | CBSA Employment | Total employment in the CBSA | Count |
| `CBSA_WRK` | CBSA Workers | Total workers in the CBSA | Count |

### Demographic

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `TotPop` | Total Population | Total population in block group | Count |
| `HH` | Households | Total number of households | Count |
| `P_WrkAge` | Working Age Population | Population aged 16+ years | Proportion |
| `CountHU` | Housing Units | Total number of housing units | Count |

### Geography

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `Ac_Total` | Total Acres | Total area of block group including water | Acres |
| `Ac_Land` | Land Area | Land area of block group (excluding water) | Acres |
| `Ac_Water` | Water Area | Water area within block group | Acres |
| `Ac_Unpr` | Unprotected Land Area | Land area excluding protected/prohibited development areas | Acres |

### Employment - Residential

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `Workers` | Workers | Number of workers (employed residents) | Count |
| `R_LowWageWk` | Low-Wage Workers (Residential) | Workers earning ≤$1,250/month living in block group | Count |
| `R_MedWageWk` | Medium-Wage Workers (Residential) | Workers earning $1,251-$3,333/month living in block group | Count |
| `R_HiWageWk` | High-Wage Workers (Residential) | Workers earning >$3,333/month living in block group | Count |
| `R_PCTLOWWAGE` | Percent Low-Wage Workers (Residential) | Percentage of workers earning low wages | Proportion |

### Employment - Workplace

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `TotEmp` | Total Employment | Total number of jobs in block group | Count |
| `E5_Ret` | Retail Employment (5-Tier) | Retail trade jobs | Count |
| `E5_Off` | Office Employment (5-Tier) | Office-based jobs | Count |
| `E5_Ind` | Industrial Employment (5-Tier) | Industrial sector jobs | Count |
| `E5_Svc` | Service Employment (5-Tier) | Service sector jobs | Count |
| `E5_Ent` | Entertainment Employment (5-Tier) | Entertainment and recreation jobs | Count |
| `E8_Ret` | Retail Employment (8-Tier) | Retail trade jobs (alternative classification) | Count |
| `E8_off` | Office Employment (8-Tier) | Office-based jobs (alternative classification) | Count |
| `E8_Ind` | Industrial Employment (8-Tier) | Industrial sector jobs (alternative classification) | Count |
| `E8_Svc` | Service Employment (8-Tier) | Service sector jobs (alternative classification) | Count |
| `E8_Ent` | Entertainment Employment (8-Tier) | Entertainment and recreation jobs (alternative) | Count |
| `E8_Ed` | Education Employment (8-Tier) | Education sector jobs | Count |
| `E8_Hlth` | Healthcare Employment (8-Tier) | Healthcare and social assistance jobs | Count |
| `E8_Pub` | Public Administration Employment (8-Tier) | Government and public administration jobs | Count |
| `E_LowWageWk` | Low-Wage Jobs (Workplace) | Jobs paying ≤$1,250/month in block group | Count |
| `E_MedWageWk` | Medium-Wage Jobs (Workplace) | Jobs paying $1,251-$3,333/month in block group | Count |
| `E_HiWageWk` | High-Wage Jobs (Workplace) | Jobs paying >$3,333/month in block group | Count |
| `E_PctLowWage` | Percent Low-Wage Jobs (Workplace) | Percentage of jobs that are low-wage | Proportion |

### Density (D1)

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `D1A` | Gross Population Density | Population per acre on total land | People/Acre |
| `D1B` | Gross Employment Density | Employment per acre on total land | Jobs/Acre |
| `D1C` | Gross Activity Density | Combined population + employment per acre | Activity/Acre |
| `D1C5_RET` | Retail Employment Density (5-Tier) | Retail jobs per acre | Jobs/Acre |
| `D1C5_OFF` | Office Employment Density (5-Tier) | Office jobs per acre | Jobs/Acre |
| `D1C5_IND` | Industrial Employment Density (5-Tier) | Industrial jobs per acre | Jobs/Acre |
| `D1C5_SVC` | Service Employment Density (5-Tier) | Service jobs per acre | Jobs/Acre |
| `D1C5_ENT` | Entertainment Employment Density (5-Tier) | Entertainment/recreation jobs per acre | Jobs/Acre |
| `D1C8_RET` | Retail Employment Density (8-Tier) | Retail jobs per acre (alternative) | Jobs/Acre |
| `D1C8_OFF` | Office Employment Density (8-Tier) | Office jobs per acre (alternative) | Jobs/Acre |
| `D1C8_IND` | Industrial Employment Density (8-Tier) | Industrial jobs per acre (alternative) | Jobs/Acre |
| `D1C8_SVC` | Service Employment Density (8-Tier) | Service jobs per acre (alternative) | Jobs/Acre |
| `D1C8_ENT` | Entertainment Employment Density (8-Tier) | Entertainment jobs per acre (alternative) | Jobs/Acre |
| `D1C8_ED` | Education Employment Density (8-Tier) | Education jobs per acre | Jobs/Acre |
| `D1C8_HLTH` | Healthcare Employment Density (8-Tier) | Healthcare jobs per acre | Jobs/Acre |
| `D1C8_PUB` | Public Admin Employment Density (8-Tier) | Government jobs per acre | Jobs/Acre |
| `D1D` | Net Population Density | Population per acre on unprotected land only | People/Acre |
| `D1_FLAG` | Density Calculation Flag | Indicates if density calculated on total or unprotected land | Flag (0/1) |

### Diversity (D2)

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `D2A_EPHHM` | Employment-Household Entropy | Entropy measure of jobs-housing balance (0-1) | 0-1 Scale |
| `D2A_JPHH` | Jobs Per Household | Ratio of jobs to households | Ratio |
| `D2A_WRKEMP` | Workers Per Job | Ratio of resident workers to jobs | Ratio |
| `D2B_E5MIX` | 5-Tier Employment Entropy | Employment mix across 5 sectors (0-1) | 0-1 Scale |
| `D2B_E5MIXA` | 5-Tier Employment Entropy (Adjusted) | Adjusted employment entropy for small areas | 0-1 Scale |
| `D2B_E8MIX` | 8-Tier Employment Entropy | Employment mix across 8 sectors (0-1) | 0-1 Scale |
| `D2B_E8MIXA` | 8-Tier Employment Entropy (Adjusted) | Adjusted employment entropy for small areas | 0-1 Scale |
| `D2C_TRPMX1` | Trip Generation Mix 1 | Land use mix based on trip generation | Index |
| `D2C_TRPMX2` | Trip Generation Mix 2 | Alternative land use mix measure | Index |
| `D2C_TRIPEQ` | Trip Equivalency Mix | Trip-weighted land use diversity | Index |
| `D2R_JOBPOP` | Jobs-Population Balance | Jobs-to-population balance measure | Index |
| `D2R_WRKEMP` | Workers-Employment Balance | Workers-to-employment balance measure | Index |
| `D2C_WRKEMLX` | Workers-Employment Land Use Mix | Land use mix based on workers and employment | Index |
| `D2A_Ranked` | Jobs-Housing Balance Rank | Percentile ranking of jobs-housing balance | Percentile |
| `D2B_Ranked` | Employment Mix Rank | Percentile ranking of employment diversity | Percentile |

### Design (D3)

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `D3A` | Road Network Density | Miles of road per square mile | Miles/Sq Mile |
| `D3AAO` | Auto-Oriented Road Density | Miles of auto-oriented roads per square mile | Miles/Sq Mile |
| `D3AMM` | Multi-Modal Road Density | Miles of multi-modal roads per square mile | Miles/Sq Mile |
| `D3APO` | Pedestrian-Oriented Road Density | Miles of pedestrian-oriented roads per square mile | Miles/Sq Mile |
| `D3B` | Street Intersection Density | Intersections per square mile | Intersections/Sq Mile |
| `D3BAO` | Auto-Oriented Intersection Density | Auto-oriented intersections per square mile | Intersections/Sq Mile |
| `D3BMM3` | 3-Way Multi-Modal Intersection Density | 3-way multi-modal intersections per square mile | Intersections/Sq Mile |
| `D3BMM4` | 4-Way Multi-Modal Intersection Density | 4+ way multi-modal intersections per square mile | Intersections/Sq Mile |
| `D3BPO3` | 3-Way Pedestrian Intersection Density | 3-way pedestrian intersections per square mile | Intersections/Sq Mile |
| `D3BPO4` | 4-Way Pedestrian Intersection Density | 4+ way pedestrian intersections per square mile | Intersections/Sq Mile |
| `D3B_Ranked` | Intersection Density Rank | Percentile ranking of intersection density | Percentile |

### Transit Distance (D4)

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `D4A` | Distance to Nearest Transit Stop | Distance to nearest fixed-route transit stop | Meters |
| `D4B025` | Aggregate Transit Frequency (0.25 mi) | Transit trips within 0.25 mile | Trips/Day |
| `D4B050` | Aggregate Transit Frequency (0.5 mi) | Transit trips within 0.5 mile | Trips/Day |
| `D4C` | Aggregate Transit Frequency | Total transit trips within walking distance | Trips/Day |
| `D4D` | Distance to Nearest Rail Station | Distance to nearest rail/ferry station | Meters |
| `D4E` | Distance to Nearest Major Transit Stop | Distance to major transit hub | Meters |
| `D4A_Ranked` | Transit Stop Distance Rank | Percentile ranking of transit proximity | Percentile |

### Destination Access (D5)

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `D5AR` | Jobs Accessible via Auto (45 min) - Residential | Regional employment accessibility from residence | Jobs |
| `D5AE` | Jobs Accessible via Auto (45 min) - Employment | Regional employment accessibility from workplace | Jobs |
| `D5BR` | Jobs Accessible via Transit (45 min) - Residential | Regional employment accessibility via transit from residence | Jobs |
| `D5BE` | Jobs Accessible via Transit (45 min) - Employment | Regional employment accessibility via transit from workplace | Jobs |
| `D5CR` | Workers Accessible via Auto (45 min) - Residential | Regional worker accessibility from residence | Workers |
| `D5CRI` | Workers Accessible via Auto Index - Residential | Indexed worker accessibility from residence | Index |
| `D5CE` | Workers Accessible via Auto (45 min) - Employment | Regional worker accessibility from workplace | Workers |
| `D5CEI` | Workers Accessible via Auto Index - Employment | Indexed worker accessibility from workplace | Index |
| `D5DR` | Workers Accessible via Transit (45 min) - Residential | Regional worker accessibility via transit from residence | Workers |
| `D5DRI` | Workers Accessible via Transit Index - Residential | Indexed transit worker accessibility from residence | Index |
| `D5DE` | Workers Accessible via Transit (45 min) - Employment | Regional worker accessibility via transit from workplace | Workers |
| `D5DEI` | Workers Accessible via Transit Index - Employment | Indexed transit worker accessibility from workplace | Index |

### Walkability

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `NatWalkInd` | National Walkability Index | Composite walkability score (higher = more walkable) | 1-20 Scale |

### Auto Ownership

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `AutoOwn0` | Zero-Vehicle Households | Number of households with no vehicles | Count |
| `Pct_AO0` | Percent Zero-Vehicle Households | Percentage of households with no vehicles | Proportion |
| `AutoOwn1` | One-Vehicle Households | Number of households with 1 vehicle | Count |
| `Pct_AO1` | Percent One-Vehicle Households | Percentage of households with 1 vehicle | Proportion |
| `AutoOwn2p` | Two+ Vehicle Households | Number of households with 2+ vehicles | Count |
| `Pct_AO2p` | Percent Two+ Vehicle Households | Percentage of households with 2+ vehicles | Proportion |

### Spatial

| Column | Full Name | Description | Unit/Scale |
|--------|-----------|-------------|------------|
| `Shape_Length` | Shape Length | Perimeter length of block group boundary | Meters |
| `Shape_Area` | Shape Area | Area of block group polygon | Square Meters |


---

## Key Metric Interpretations

### Density Metrics (D1)
- **Higher values** = More urban, compact development
- **Lower values** = More rural, spread-out development
- **Typical urban**: >10 people/acre
- **Typical suburban**: 1-10 people/acre
- **Typical rural**: <1 person/acre

### Diversity Metrics (D2)
- **Entropy scores (0-1)**: Higher = more diverse mix
  - 0 = Single use (e.g., all residential)
  - 1 = Perfect balance across all uses
- **Jobs-Housing Balance**: 
  - 1.0 = perfect balance
  - Values >1: Job-rich area (net commuter inflow)
  - Values <1: Housing-rich area (net commuter outflow)

### Design Metrics (D3)
- **Intersection Density**: Higher = more connected street network
  - >100 intersections/sq mi = highly walkable
  - <50 intersections/sq mi = auto-oriented
- **Road Network Density**: Higher = more route options
- Pedestrian-oriented streets encourage walking and reduce VMT

### Transit Metrics (D4)
- **Distance**: Lower = better transit access
  - <400m (0.25 mi) = Good pedestrian access
  - >800m (0.5 mi) = Poor pedestrian access
- **Frequency**: Higher = more transit service
  - >50 trips/day = High frequency
  - <10 trips/day = Low frequency

### Accessibility Metrics (D5)
- **Higher values** = More regional job/worker access
- Auto accessibility typically 5-10x higher than transit
- Important for understanding regional connectivity and economic opportunity
- Values in tens or hundreds of thousands

### National Walkability Index
- **Scale**: 1-20 (higher = more walkable)
- **1-5**: Low walkability (car-dependent)
- **6-10**: Below average walkability
- **11-15**: Above average walkability  
- **16-20**: High walkability (most walk-friendly)
- Based on combination of all 5D metrics

---

## Employment Classifications

### 5-Tier Classification (E5)
1. **Retail**: Stores, restaurants, consumer services
2. **Office**: Professional, technical, management
3. **Industrial**: Manufacturing, warehousing, construction
4. **Service**: Personal services, repair, maintenance
5. **Entertainment**: Arts, recreation, accommodation

### 8-Tier Classification (E8)
Expands the 5-tier to separate:
6. **Education**: Schools, colleges, training
7. **Healthcare**: Hospitals, clinics, social assistance
8. **Public Administration**: Government offices and services

---

## New Columns Added During Cleaning

### Normalized Metrics (suffix: _normalized)
All continuous metrics scaled to 0-1 range for machine learning:
- **TotPop_normalized** - Population (0-1 scale)
- **TotEmp_normalized** - Employment (0-1 scale)
- **Workers_normalized** - Workers (0-1 scale)
- **D1A_normalized** - Population Density (0-1 scale)
- **D1B_normalized** - Employment Density (0-1 scale)
- **D1C_normalized** - Activity Density (0-1 scale)
- **D2A_JPHH_normalized** - Jobs-Housing Balance (0-1 scale)
- **D3B_normalized** - Intersection Density (0-1 scale)
- **D4A_normalized** - Transit Distance (0-1 scale)
- **D5AR_normalized** - Auto Accessibility (0-1 scale)
- **D5AE_normalized** - Employment Accessibility (0-1 scale)

Formula: `(value - min) / (max - min)`

### Categorical Variables
Created for easy segmentation and visualization:

**PopDensity_Category** (from D1A):
- Very Low: 0-1 people/acre
- Low: 1-5 people/acre
- Medium: 5-10 people/acre
- High: 10-20 people/acre
- Very High: >20 people/acre

**EmpDensity_Category** (from D1B):
- Same classification structure as population density

**Walkability_Category** (from NatWalkInd):
- Low: 0-5
- Medium: 5-10
- High: 10-15
- Very High: 15-20

### Derived Metrics
Capture important relationships between variables:

**Emp_Pop_Ratio** = TotEmp ÷ TotPop
- Measures job availability relative to population
- <1: Net commuter outflow (bedroom community)
- >1: Net commuter inflow (employment center)
- ≈1: Balanced community

**Workers_Per_HH** = Workers ÷ Households
- Average workers per household
- Typical range: 1.0 - 2.0
- Indicates labor force participation

---

## Data Sources & Methodology

### Primary Data Sources:
1. **U.S. Census Bureau**: Population, housing, demographic data (2010 Census + ACS)
2. **LEHD (Longitudinal Employer-Household Dynamics)**: Employment data by location and industry
3. **NAVTEQ/HERE**: Street network and intersection data
4. **General Transit Feed Specification (GTFS)**: Transit stop/route data
5. **EPA EnviroAtlas**: Protected lands data

### Calculation Methods:
- **Densities**: Calculated using unprotected land area where appropriate
- **Transit metrics**: Use network distance (not straight-line Euclidean distance)
- **Accessibility**: Uses travel time impedance modeling (45-minute threshold)
- **Rankings**: Percentile-based within metropolitan areas (CBSA level)
- **Entropy**: Shannon entropy formula for measuring diversity

### Reference Year:
- Base data: 2017-2019 (varies by source)
- Population: 2010 Census + 2016-2020 ACS
- Employment: LEHD 2017
- Transit: GTFS feeds circa 2018-2019

---

## Usage Notes

### Best Practices:
1. **Always consider geographic context** - Rural vs urban areas have different baseline values
2. **Use CBSA/CSA for regional comparisons** - Metrics are ranked within metro areas
3. **Check for missing values** - Rural areas may lack transit/CSA data (24% of records)
4. **Combine multiple metrics** - No single metric tells the full story
5. **Understand the denominator** - Density metrics use land area, not population

### Common Analysis Use Cases:

**Urban Planning:**
- Identify areas for transit-oriented development (high D1, D2, D3)
- Evaluate job-housing balance (D2A_JPHH)
- Assess street connectivity for walkability (D3B)

**Public Health:**
- Link walkability to health outcomes (NatWalkInd)
- Analyze physical activity potential (D3, D4 metrics)
- Study built environment impacts on obesity, diabetes

**Transportation:**
- Assess multimodal accessibility (D4, D5 metrics)
- Predict travel mode choice
- Estimate vehicle miles traveled (VMT) reduction potential

**Climate & Sustainability:**
- Identify compact, transit-oriented areas
- Evaluate greenhouse gas reduction potential
- Support climate action planning

**Equity Analysis:**
- Compare access across demographics
- Identify transit deserts
- Analyze spatial mismatch between jobs and workers

### Known Limitations:
- **Temporal**: Data snapshot from 2017-2019 (pre-COVID)
- **Aggregation**: Block group level may mask within-area variation
- **Transit**: Based on scheduled service, not actual ridership or reliability
- **Networks**: Does not capture trail networks, informal paths, or sidewalk quality
- **Changes**: Does not reflect recent development or transit service changes
- **Rural areas**: Some metrics less meaningful in low-density areas

### Special Values:
- **-99999**: Indicates null/not applicable (common in transit distance fields for areas without transit)
- **0**: May indicate true zero or missing data depending on context
- **Ranked fields**: Only populated for areas within CBSAs

---

## Additional Resources

- **EPA Smart Location Mapping**: https://www.epa.gov/smartgrowth/smart-location-mapping
- **Technical Documentation**: https://www.epa.gov/smartgrowth/smart-location-database-technical-documentation-and-user-guide
- **Data Download**: https://www.epa.gov/smartgrowth/smart-location-mapping#SLD

---

*Data Dictionary Generated: November 11, 2025*
*Cleaned Dataset: November 10, 2025*
