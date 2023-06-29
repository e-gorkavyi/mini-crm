﻿CREATE TABLE `FederalDistricts` (
	`ID` INT NOT NULL,
	`Name` NVARCHAR(100) NOT NULL
);

CREATE TABLE `Oktmo` (
	`ID` INT NOT NULL,
	`Kod` NVARCHAR(14) NOT NULL,
	`Kod2` NVARCHAR(11) NOT NULL,
	`SubKod1` NVARCHAR(2) NOT NULL,
	`SubKod2` NVARCHAR(3) NOT NULL,
	`SubKod3` NVARCHAR(3) NOT NULL,
	`SubKod4` NVARCHAR(3) NULL,
	`P1` NVARCHAR(1) NOT NULL,
	`P2` NVARCHAR(1) NOT NULL,
	`Kch` NVARCHAR(1) NOT NULL,
	`Name` NVARCHAR(500) NOT NULL,
	`Name2` NVARCHAR(500) NULL,
	`Notes` NVARCHAR(500) NULL,
	`FederalDistrictID` INT NOT NULL,
	`FederalDistrictName` NVARCHAR(100) NOT NULL,
	`RegionID` INT NOT NULL,
	`RegionName` NVARCHAR(50) NOT NULL,
	`SettlementTypeID` INT NULL,
	`SettlementTypeName` NVARCHAR(100) NULL,
	`WhenAdd` DATETIME NOT NULL,
	`Source` VARCHAR(15) NOT NULL
);

CREATE TABLE `Regions` (
	`ID` INT NOT NULL,
	`OKTMO_ID` INT NULL,
	`Name` NVARCHAR(100) NULL,
	`FederalDistrictID` INT NULL,
	`FederalDistrictName` NVARCHAR(100) NULL
);

CREATE TABLE `SettlementTypes` (
	`ID` INT NOT NULL,
	`ShortName` NVARCHAR(50) NOT NULL,
	`Name` NVARCHAR(200) NOT NULL
);

