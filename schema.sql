-- This SQL is not used. Instead alembic is using to handle migration

CREATE TABLE IF NOT EXISTS `financial_data` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `symbol` varchar(32) COLLATE utf8mb4_bin NOT NULL,
  `date` date NOT NULL,
  `open_price` decimal(19,2) NOT NULL,
  `close_price` decimal(19,2) NOT NULL,
  `volume` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_symbol_date_unique` (`symbol`,`date`),
  KEY `ix_financial_data_date` (`date`),
  KEY `ix_financial_data_symbol` (`symbol`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin