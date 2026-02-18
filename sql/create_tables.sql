-- =========================================================
-- DDL for Dimensional Data Warehouse (Star Schema)
-- Lab 3 - ETL & BI
-- =========================================================

-- -----------------------------------------------------
-- Table `customer` (Dimension)
-- -----------------------------------------------------
-- Stores demographic information about customers.
CREATE TABLE IF NOT EXISTS `customer` (
  `id_customer` INT NOT NULL,     -- Surrogate Key (matches source ID)
  `name` VARCHAR(100) NOT NULL,   -- Full customer name
  `city` VARCHAR(45) NOT NULL,    -- City of residence
  `country` VARCHAR(45) NOT NULL, -- Country
  `age` INT NOT NULL,             -- Customer age
  PRIMARY KEY (`id_customer`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `product` (Dimension)
-- -----------------------------------------------------
-- Stores product catalog details including costs and prices.
CREATE TABLE IF NOT EXISTS `product` (
  `id_product` INT NOT NULL,        -- Surrogate Key (matches source ID)
  `name` VARCHAR(100) NOT NULL,     -- Product name
  `category` VARCHAR(45) NOT NULL,  -- Product category
  `brand` VARCHAR(45) NOT NULL,     -- Brand manufacturer
  `unit_price` DECIMAL(10,2) NOT NULL, -- List price
  `unit_cost` DECIMAL(10,2) NOT NULL,  -- Acquisition cost
  PRIMARY KEY (`id_product`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `channel` (Dimension)
-- -----------------------------------------------------
-- Captures the sales channel (e.g., Physical Store vs. Online).
CREATE TABLE IF NOT EXISTS `channel` (
  `id_channel` INT NOT NULL,        -- Surrogate Key (matches source ID)
  `channel` VARCHAR(100) NOT NULL,  -- Channel name
  PRIMARY KEY (`id_channel`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `date` (Dimension)
-- -----------------------------------------------------
-- A dedicated time dimension for temporal analysis.
CREATE TABLE IF NOT EXISTS `date` (
  `id_date` INT NOT NULL,         -- Surrogate Key (YYYYMMDD)
  `day` TINYINT(2) NOT NULL,      -- Day of month (1-31)
  `month` TINYINT(2) NOT NULL,    -- Month number (1-12)
  `year` INT NOT NULL,            -- 4-digit Year
  `quarter` TINYINT(1) NOT NULL,  -- Quarter (1-4)
  PRIMARY KEY (`id_date`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sale` (Fact Table)
-- -----------------------------------------------------
-- The central fact table storing quantitative transactional data.
-- It links to all dimensions via Foreign Keys.
CREATE TABLE IF NOT EXISTS `sale` (
  `id_sale` INT NOT NULL,           -- Transaction Identifier
  `quantity` INT NOT NULL,          -- Units sold
  `unit_price_sale` DECIMAL(10,2) NOT NULL, -- Actual sale price per unit
  `total_amount` DECIMAL(10,2) NOT NULL,    -- Total Revenue (Qty * Price)
  `profit` DECIMAL(10,2) NOT NULL,          -- Net Profit (Revenue - Cost)
  
  -- Foreign Keys
  `customer_idcustomer` INT NOT NULL,
  `product_idproduct` INT NOT NULL,
  `channel_idchannel` INT NOT NULL,
  `date_iddate` INT NOT NULL,
  
  -- Primary Key (Composite)
  PRIMARY KEY (`id_sale`, `customer_idcustomer`, `product_idproduct`, `channel_idchannel`, `date_iddate`),
  
  -- Referential Integrity Constraints
  CONSTRAINT `fk_sale_customer`
    FOREIGN KEY (`customer_idcustomer`)
    REFERENCES `customer` (`id_customer`),
  CONSTRAINT `fk_sale_product1`
    FOREIGN KEY (`product_idproduct`)
    REFERENCES `product` (`id_product`),
  CONSTRAINT `fk_sale_channel1`
    FOREIGN KEY (`channel_idchannel`)
    REFERENCES `channel` (`id_channel`),
  CONSTRAINT `fk_sale_date1`
    FOREIGN KEY (`date_iddate`)
    REFERENCES `date` (`id_date`))
ENGINE = InnoDB;
