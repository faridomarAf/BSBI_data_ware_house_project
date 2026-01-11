# Design and Implementation of a Data Warehouse for an E-Commerce Marketplace

**Student:** Farid Ahmad Omar (ID: Q1109076)  
**Module:** Enterprise Data Warehouses and Database Management Systems  
**Lecturer:** Dr. Roman Bhuiyan  
**Institution:** Berlin School of Business and Innovation (BSBI), in partnership with University for the Creative Arts (UCA), UK  
**Submission Date:** 02/01/2026  

---

## Project Overview

This project implements a **data warehouse** for an e-commerce marketplace to support operational data management, analytics, and business intelligence. The warehouse integrates core entities such as **Customer, Seller, Product, Order, Payment, Shipment, Inventory, Promotion, Review**, and related junction tables.  

Key points:  
- Data is organized following **Third Normal Form (3NF)** to avoid redundancy.  
- Supports **realistic sample data ingestion** for testing and analytics.  
- Prepares the database for **large-scale operational and analytical queries**.  

---

## Database Setup

**1. Create Database:**

```sql
CREATE DATABASE EC_MARKETPLACE;
```

**2. Create Tables:**

All tables follow 3NF design with proper **primary and foreign keys, constraints, and data types**.  

Tables include:  
- `Customer`, `Seller`, `Category`, `Product`  
- `Product_Seller` (many-to-many relationship)  
- `Orders`, `Order_Item`, `Payment`  
- `Warehouse`, `Inventory`, `Shipment`  
- `Review`, `Promotion`, `Customer_Promotion`  

> Full `CREATE TABLE` scripts are provided in `/sql/` folder.

---

## CSV Generation & Data Loading

### CSV Generation

- Scripts generate realistic batch CSVs for all entities.  
- Data is partitioned into manageable files for **efficient bulk loading**.  

### Data Loading

- Bash loader scripts import CSVs into MySQL.  
- Features include:
  - **Transactional loads** (`START TRANSACTION ... COMMIT`)  
  - **Batch processing**  
  - **Logging** of success and errors  
  - **Automatic file handling** (`processed/` and `error/` directories)  

**Important:** All commands should be run **from the project root directory** where generators, loaders, and `data/` folders exist.

---

## Quick Start Commands

Make loader scripts executable:

```bash
chmod +x loaders/load_customer_part_bulk.sh
chmod +x loaders/load_seller_part_bulk.sh
chmod +x loaders/load_category_part_bulk.sh
chmod +x loaders/load_product_part_bulk.sh
chmod +x loaders/load_warehouse_part_bulk.sh
chmod +x loaders/load_promotion_part_bulk.sh
chmod +x loaders/load_product_seller_part_bulk.sh
chmod +x loaders/load_inventory_part_bulk.sh
chmod +x loaders/load_customer_promotion_part_bulk.sh
chmod +x loaders/load_orders_part_bulk.sh
chmod +x loaders/load_order_items_part_bulk.sh
chmod +x loaders/load_payments_part_bulk.sh
chmod +x loaders/load_shipments_part_bulk.sh
chmod +x loaders/load_review_part_bulk.sh
```

Run loaders sequentially in **relational order**:

```bash
./loaders/load_customer_part_bulk.sh
./loaders/load_seller_part_bulk.sh
./loaders/load_category_part_bulk.sh
./loaders/load_product_part_bulk.sh
./loaders/load_warehouse_part_bulk.sh
./loaders/load_promotion_part_bulk.sh
./loaders/load_product_seller_part_bulk.sh
./loaders/load_inventory_part_bulk.sh
./loaders/load_customer_promotion_part_bulk.sh
./loaders/load_orders_part_bulk.sh
./loaders/load_order_items_part_bulk.sh
./loaders/load_payments_part_bulk.sh
./loaders/load_shipments_part_bulk.sh
./loaders/load_review_part_bulk.sh
```

> This ensures all tables are populated **correctly respecting foreign key dependencies**.

---

## Folder Structure

```
project-root/
├── data/                     # Generated CSV files (batched)
│   ├── customers/
│   ├── sellers/
│   ├── category/
│   ├── product/
│   ├── warehouse/
│   ├── promotion/
│   ├── product_seller/
│   ├── inventory/
│   ├── customer_promotion/
│   ├── orders/
│   ├── order_items/
│   ├── payments/
│   ├── shipments/
│   └── reviews/
├── generators/               # CSV generation scripts
├── loaders/                  # CSV bulk loader scripts
├── sql/                      # CREATE TABLE scripts
└── README.md
```

---

## Workflow Overview

```
┌─────────────────────┐
│  CSV Generators     │
└─────────┬──────────┘
          │
          ▼
┌─────────────────────┐
│  CSV Files (Batches)│
└─────────┬──────────┘
          │
          ▼
┌─────────────────────┐
│  CSV Loaders        │
└─────────┬──────────┘
          │
          ▼
┌─────────────────────┐
│  MySQL Data Warehouse│
│  EC_MARKETPLACE      │
└─────────────────────┘
```

- Data is loaded in **entity dependency order** to maintain **referential integrity**.  
- Loader scripts log all operations and manage processed/error files automatically.  

---

## Notes for Future Steps

- This README contains only the **essential operational instructions**.  
- Additional analytics queries, views, and optimizations will be **added in later steps**.  
- Ensure MySQL credentials in scripts match your environment before running loaders.

