-- -----------------------------------------------------
-- Schema ETL_LAB_3
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ETL_LAB_3` DEFAULT CHARACTER SET utf8 ;
USE `ETL_LAB_3` ;

-- -----------------------------------------------------
-- Table `customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `customer` (
  `id_customer` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `city` VARCHAR(45) NOT NULL,
  `country` VARCHAR(45) NOT NULL,
  `age` INT NOT NULL,
  PRIMARY KEY (`id_customer`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `product`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `product` (
  `id_product` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `category` VARCHAR(45) NOT NULL,
  `brand` VARCHAR(45) NOT NULL,
  `unit_price` DECIMAL(10,2) NOT NULL,
  `unit_cost` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_product`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `channel`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `channel` (
  `id_channel` INT NOT NULL,
  `channel` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_channel`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `date`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `date` (
  `id_date` INT NOT NULL,
  `day` TINYINT(2) NOT NULL,
  `month` TINYINT(2) NOT NULL,
  `year` INT NOT NULL,
  `quarter` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id_date`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sale`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sale` (
  `id_sale` INT NOT NULL,
  `quantity` INT NOT NULL,
  `unit_price_sale` DECIMAL(10,2) NOT NULL,
  `total_amount` DECIMAL(10,2) NOT NULL,
  `profit` DECIMAL(10,2) NOT NULL,
  `customer_idcustomer` INT NOT NULL,
  `product_idproduct` INT NOT NULL,
  `channel_idchannel` INT NOT NULL,
  `date_iddate` INT NOT NULL,
  PRIMARY KEY (`id_sale`, `customer_idcustomer`, `product_idproduct`, `channel_idchannel`, `date_iddate`),
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
