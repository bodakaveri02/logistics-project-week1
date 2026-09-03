import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_logistics_dataset(n_samples=3000, random_seed=42):
    np.random.seed(random_seed)
    
    start_date = datetime(2026, 8, 1, 6, 0, 0)
    order_ids = [f"ORD-2026-{10000 + i}" for i in range(n_samples)]
    customer_ids = [f"CUST-{np.random.randint(1000, 9999)}" for _ in range(n_samples)]
    
    minutes_offset = np.random.uniform(0, 30 * 24 * 60, n_samples)
    order_timestamps = [start_date + timedelta(minutes=float(m)) for m in minutes_offset]
    
    warehouses = [
        {"id": "RDC-NORTH", "name": "Regional DC North", "lat": 40.8500, "lon": -73.9200, "type": "RDC"},
        {"id": "RDC-SOUTH", "name": "Regional DC South", "lat": 40.6500, "lon": -74.1500, "type": "RDC"},
        {"id": "MFC-CENTRAL", "name": "Micro-Fulfillment Central", "lat": 40.7580, "lon": -73.9855, "type": "MFC"},
        {"id": "MFC-EAST", "name": "Micro-Fulfillment East", "lat": 40.7282, "lon": -73.7949, "type": "MFC"}
    ]
    warehouse_indices = np.random.choice(len(warehouses), size=n_samples, p=[0.25, 0.25, 0.30, 0.20])
    warehouse_choices = [warehouses[i] for i in warehouse_indices]
    warehouse_ids = [w["id"] for w in warehouse_choices]
    warehouse_types = [w["type"] for w in warehouse_choices]
    
    dest_lats = np.random.normal(loc=40.75, scale=0.08, size=n_samples)
    dest_lons = np.random.normal(loc=-73.98, scale=0.09, size=n_samples)
    
    shipping_modes = np.random.choice(
        ["Same-Day Express", "Next-Day Priority", "Standard Ground (2-3 Days)"],
        size=n_samples,
        p=[0.25, 0.45, 0.30]
    )
    
    sla_hours_map = {
        "Same-Day Express": 6.0,
        "Next-Day Priority": 24.0,
        "Standard Ground (2-3 Days)": 60.0
    }
    promised_hours = np.array([sla_hours_map[m] for m in shipping_modes])
    
    categories = ["Consumer Electronics", "Apparel & Fashion", "Perishable Grocery", "Home & Living", "Health & Personal Care"]
    product_categories = np.random.choice(categories, size=n_samples, p=[0.20, 0.30, 0.20, 0.15, 0.15])
    
    package_weight_kg = np.round(np.random.gamma(shape=2.5, scale=1.8, size=n_samples), 2)
    package_volume_m3 = np.round(package_weight_kg * np.random.uniform(0.003, 0.008, size=n_samples), 4)
    item_count = np.random.randint(1, 6, size=n_samples)
    order_value_usd = np.round(np.random.lognormal(mean=4.2, sigma=0.7, size=n_samples), 2)
    
    w_lats = np.array([w["lat"] for w in warehouse_choices])
    w_lons = np.array([w["lon"] for w in warehouse_choices])
    
    d_lat = (dest_lats - w_lats) * 111.0
    d_lon = (dest_lons - w_lons) * 85.0
    direct_distance_km = np.round(np.sqrt(d_lat**2 + d_lon**2), 2)
    circuity_factor = np.random.uniform(1.28, 1.55, size=n_samples)
    route_distance_km = np.round(direct_distance_km * circuity_factor, 2)
    
    traffic_congestion_index = np.round(np.random.beta(a=2.5, b=2.5, size=n_samples) * 9 + 1, 2)
    weather_severity_index = np.round(np.random.exponential(scale=1.5, size=n_samples) + 1.0, 2)
    weather_severity_index = np.clip(weather_severity_index, 1.0, 10.0)
    
    driver_experience_years = np.round(np.random.uniform(0.5, 12.0, size=n_samples), 1)
    delivery_attempts = np.random.choice([1, 2, 3], size=n_samples, p=[0.87, 0.10, 0.03])
    
    avg_speed_kmh = np.clip(35.0 - (traffic_congestion_index * 1.8), 10.0, 50.0)
    driving_time_hours = route_distance_km / avg_speed_kmh
    
    warehouse_dwell_hours = np.where(
        np.array(warehouse_types) == "MFC",
        np.random.uniform(0.3, 1.2, size=n_samples),
        np.random.uniform(1.5, 4.0, size=n_samples)
    )
    
    delay_factors = (weather_severity_index > 5.0) * np.random.uniform(1.0, 4.5, size=n_samples) + \
                    (delivery_attempts - 1) * np.random.uniform(6.0, 18.0, size=n_samples)
    
    actual_transit_hours = np.round(warehouse_dwell_hours + driving_time_hours + delay_factors, 2)
    
    promised_delivery_time = [ts + timedelta(hours=float(h)) for ts, h in zip(order_timestamps, promised_hours)]
    actual_delivery_time = [ts + timedelta(hours=float(h)) for ts, h in zip(order_timestamps, actual_transit_hours)]
    
    is_late = np.array([act > prom for act, prom in zip(actual_delivery_time, promised_delivery_time)]).astype(int)
    delivery_status = np.where(is_late == 1, "Late Delivery", "On-Time")
    
    in_full_flag = np.random.choice([1, 0], size=n_samples, p=[0.97, 0.03])
    otif_flag = ((is_late == 0) & (in_full_flag == 1)).astype(int)
    
    fuel_cost_per_km = 0.32
    driver_wage_per_hr = 25.50
    base_stop_fee = 4.20
    
    delivery_cost_usd = np.round(
        base_stop_fee + 
        (route_distance_km * fuel_cost_per_km) + 
        (driving_time_hours * driver_wage_per_hr) + 
        (delivery_attempts - 1) * 6.50 +
        (package_weight_kg * 0.18),
        2
    )
    
    df = pd.DataFrame({
        "Order_ID": order_ids,
        "Customer_ID": customer_ids,
        "Order_Timestamp": [ts.strftime("%Y-%m-%d %H:%M:%S") for ts in order_timestamps],
        "Promised_Delivery_Time": [ts.strftime("%Y-%m-%d %H:%M:%S") for ts in promised_delivery_time],
        "Actual_Delivery_Time": [ts.strftime("%Y-%m-%d %H:%M:%S") for ts in actual_delivery_time],
        "Shipping_Mode": shipping_modes,
        "Product_Category": product_categories,
        "Order_Value_USD": order_value_usd,
        "Item_Count": item_count,
        "Package_Weight_kg": package_weight_kg,
        "Package_Volume_m3": package_volume_m3,
        "Origin_Warehouse_ID": warehouse_ids,
        "Origin_Warehouse_Type": warehouse_types,
        "Dest_Latitude": np.round(dest_lats, 5),
        "Dest_Longitude": np.round(dest_lons, 5),
        "Direct_Distance_km": direct_distance_km,
        "Route_Distance_km": route_distance_km,
        "Traffic_Congestion_Index": traffic_congestion_index,
        "Weather_Severity_Index": weather_severity_index,
        "Driver_Experience_Years": driver_experience_years,
        "Delivery_Attempts": delivery_attempts,
        "Actual_Transit_Hours": actual_transit_hours,
        "Promised_SLA_Hours": promised_hours,
        "Is_Late": is_late,
        "In_Full_Flag": in_full_flag,
        "OTIF_Flag": otif_flag,
        "Delivery_Cost_USD": delivery_cost_usd,
        "Delivery_Status": delivery_status
    })
    return df

if __name__ == "__main__":
    df = generate_logistics_dataset(n_samples=3000, random_seed=42)
    os.makedirs("data", exist_ok=True)
    csv_path = os.path.join("data", "logistics_operational_data.csv")
    df.to_csv(csv_path, index=False)
    print(f"Generated {len(df)} records in {csv_path}")
    print(f"OTIF Rate: {df['OTIF_Flag'].mean()*100:.2f}% | Late Rate: {df['Is_Late'].mean()*100:.2f}% | Avg Cost: ${df['Delivery_Cost_USD'].mean():.2f}")
