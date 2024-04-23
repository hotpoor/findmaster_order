database: test
```
CREATE TABLE `index_login` (
  `login` varchar(255) NOT NULL,
  `entity_id` char(32) NOT NULL,
  `search` varchar(255) DEFAULT '',
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `app` varchar(255) DEFAULT NULL,
  `about` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `entity_id` (`entity_id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

database: test1
```
CREATE TABLE `entities` (
  `id` char(32) NOT NULL DEFAULT '',
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `body` longblob NOT NULL,
  `auto_increment` int NOT NULL AUTO_INCREMENT COMMENT 'basicly never used',
  PRIMARY KEY (`auto_increment`),
  UNIQUE KEY `id` (`id`),
  KEY `updated` (`updated`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

database: test2
```
CREATE TABLE `entities` (
  `id` char(32) NOT NULL DEFAULT '',
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `body` longblob NOT NULL,
  `auto_increment` int NOT NULL AUTO_INCREMENT COMMENT 'basicly never used',
  PRIMARY KEY (`auto_increment`),
  UNIQUE KEY `id` (`id`),
  KEY `updated` (`updated`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```