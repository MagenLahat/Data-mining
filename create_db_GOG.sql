-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema GOG_SCRAPPER_DB
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema GOG_SCRAPPER_DB
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `GOG_SCRAPPER_DB` DEFAULT CHARACTER SET utf8 ;
USE `GOG_SCRAPPER_DB` ;

-- -----------------------------------------------------
-- Table `GOG_SCRAPPER_DB`.`game_titles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GOG_SCRAPPER_DB`.`game_titles` (
  `title_sku` BIGINT NOT NULL,
  `title_name` VARCHAR(255) NOT NULL,
  `clean_title_name` VARCHAR(255) NOT NULL,
  `title_release_date` DATE NULL,
  `title_supported_os` VARCHAR(512) NULL,
  `title_company` VARCHAR(255) NULL,
  `title_size_mb` DECIMAL NULL,
  `title_url` VARCHAR(512) NULL,
  PRIMARY KEY (`title_sku`))
ENGINE = myisam;


-- -----------------------------------------------------
-- Table `GOG_SCRAPPER_DB`.`game_scores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GOG_SCRAPPER_DB`.`game_scores` (
  `score_id` INT NOT NULL AUTO_INCREMENT,
  `title_sku` BIGINT NOT NULL,
  `score_quote_datetime` DATETIME NOT NULL,
  `score` DECIMAL(3,2) NOT NULL COMMENT 'between 0 - 5',
  PRIMARY KEY (`score_id`, `title_sku`),
  INDEX `fk_game_scores_game_titles_idx` (`title_sku` ASC) VISIBLE,
  CONSTRAINT `fk_game_scores_game_titles`
    FOREIGN KEY (`title_sku`)
    REFERENCES `GOG_SCRAPPER_DB`.`game_titles` (`title_sku`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = myisam;


-- -----------------------------------------------------
-- Table `GOG_SCRAPPER_DB`.`game_prices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GOG_SCRAPPER_DB`.`game_prices` (
  `price_id` INT NOT NULL AUTO_INCREMENT,
  `title_sku` BIGINT NOT NULL,
  `price_quote_datetime` DATETIME NOT NULL,
  `price_base` DECIMAL(10,2) NULL,
  `price_final` DECIMAL(10,2) NULL,
  `discount` DECIMAL(4,2) NULL,
  PRIMARY KEY (`price_id`, `title_sku`),
  INDEX `fk_game_prices_game_titles1_idx` (`title_sku` ASC) VISIBLE,
  CONSTRAINT `fk_game_prices_game_titles1`
    FOREIGN KEY (`title_sku`)
    REFERENCES `GOG_SCRAPPER_DB`.`game_titles` (`title_sku`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = myisam;


-- -----------------------------------------------------
-- Table `GOG_SCRAPPER_DB`.`game_genres`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `GOG_SCRAPPER_DB`.`game_genres` (
  `title_sku` BIGINT NOT NULL,
  `genre_name` VARCHAR(150) NULL,
  PRIMARY KEY (`title_sku`),
  INDEX `fk_game_gneres_game_titles1_idx` (`title_sku` ASC) VISIBLE,
  CONSTRAINT `fk_game_gneres_game_titles1`
    FOREIGN KEY (`title_sku`)
    REFERENCES `GOG_SCRAPPER_DB`.`game_titles` (`title_sku`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = myisam;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
