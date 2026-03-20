-- MySQL doesn't use BEGIN TRANSACTION for schema creation in the same way; 
-- you can just run these statements directly.

-- 1. Create the Category Table
CREATE TABLE IF NOT EXISTS `category_table` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL UNIQUE,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;

-- 2. Create the Product Table (Core Table)
CREATE TABLE IF NOT EXISTS `product_table` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `sku` VARCHAR(100) NOT NULL UNIQUE,
    `name` VARCHAR(255) NOT NULL,
    `category_id` INT NOT NULL,
    `price` DECIMAL(10, 2) NOT NULL, -- DECIMAL is better than REAL/FLOAT for currency
    `quantity` INT NOT NULL DEFAULT 0,
    `shelf_number` VARCHAR(50),
    `barcode_path` VARCHAR(500) NOT NULL,
    `reorder_level` INT NOT NULL DEFAULT 10,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    -- Adding a Foreign Key constraint ensures data integrity
    CONSTRAINT `fk_category` 
        FOREIGN KEY (`category_id`) 
        REFERENCES `category_table` (`id`)
        ON DELETE CASCADE
) ENGINE=InnoDB;