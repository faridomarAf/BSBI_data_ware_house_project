
CREATE DATABASE EC_MARKETPLACE;

CREATE TABLE Customer (
    customer_id VARCHAR(30) PRIMARY KEY, -- DE-CUST-2024-XXXXXXXXX
    first_name  VARCHAR(100) NOT NULL,
    last_name   VARCHAR(100) NOT NULL,
    email       VARCHAR(150) NOT NULL UNIQUE,
    phone       VARCHAR(20),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------
-- Seller
-- ------------------------
CREATE TABLE Seller (
    seller_id INT AUTO_INCREMENT PRIMARY KEY,
    seller_name VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ------------------------
-- Category
-- ------------------------
CREATE TABLE Category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- ------------------------
-- Product
-- ------------------------
CREATE TABLE Product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Category(category_id)
) ENGINE=InnoDB;

-- ------------------------
-- Product_Seller
-- ------------------------
CREATE TABLE Product_Seller (
    product_id INT NOT NULL,
    seller_id INT NOT NULL,
    supply_price DECIMAL(10,2) CHECK (supply_price >= 0),
    PRIMARY KEY (product_id, seller_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    FOREIGN KEY (seller_id) REFERENCES Seller(seller_id)
) ENGINE=InnoDB;

-- ------------------------
-- Orders
-- ------------------------
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(30) NOT NULL, -- matches Customer PK
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    order_status VARCHAR(30) DEFAULT 'Pending',
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
) ENGINE=InnoDB;

-- ------------------------
-- Order_Item
-- ------------------------
CREATE TABLE Order_Item (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
) ENGINE=InnoDB;

-- ------------------------
-- Payment
-- ------------------------
CREATE TABLE Payment (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL CHECK (amount >= 0),
    payment_method VARCHAR(50),
    payment_status VARCHAR(30) DEFAULT 'Completed',
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
) ENGINE=InnoDB;

-- ------------------------
-- Warehouse
-- ------------------------
CREATE TABLE Warehouse (
    warehouse_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(150) NOT NULL
) ENGINE=InnoDB;

-- ------------------------
-- Inventory
-- ------------------------
CREATE TABLE Inventory (
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    stock_quantity INT NOT NULL CHECK (stock_quantity >= 0),
    PRIMARY KEY (product_id, warehouse_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id)
) ENGINE=InnoDB;

-- ------------------------
-- Shipment
-- ------------------------
CREATE TABLE Shipment (
    shipment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    courier VARCHAR(100),
    shipped_date DATETIME,
    delivery_status VARCHAR(50) DEFAULT 'Processing',
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (warehouse_id) REFERENCES Warehouse(warehouse_id)
) ENGINE=InnoDB;

-- ------------------------
-- Review
-- ------------------------
CREATE TABLE Review (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    customer_id VARCHAR(30) NOT NULL, -- matches Customer PK
    rating INT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    review_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES Product(product_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
) ENGINE=InnoDB;

-- ------------------------
-- Promotion
-- ------------------------
CREATE TABLE Promotion (
    promotion_id INT AUTO_INCREMENT PRIMARY KEY,
    promo_code VARCHAR(50) NOT NULL UNIQUE,
    discount_percent INT CHECK (discount_percent BETWEEN 1 AND 90)
) ENGINE=InnoDB;

-- ------------------------
-- Customer_Promotion
-- ------------------------
CREATE TABLE Customer_Promotion (
    customer_id VARCHAR(30) NOT NULL, -- matches Customer PK
    promotion_id INT NOT NULL,
    used_date DATETIME,
    PRIMARY KEY (customer_id, promotion_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
    FOREIGN KEY (promotion_id) REFERENCES Promotion(promotion_id)
) ENGINE=InnoDB;





