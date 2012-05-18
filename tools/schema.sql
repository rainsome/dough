CREATE TABLE `regions` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
 
CREATE TABLE `items` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
 
CREATE TABLE `item_types` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
 
CREATE TABLE `payment_types` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `interval_unit` varchar(255) NOT NULL,
  `interval_size` int(11) NOT NULL,
  `is_prepaid` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
 
CREATE TABLE `products` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `item_type_id` int(11) NOT NULL,
  `payment_type_id` int(11) NOT NULL,
  `order_unit` varchar(255) NOT NULL,  # e.g) hours / days / months / KBytes / requests
  `order_size` int(11) NOT NULL,
  `price` float NOT NULL,
  `currency` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `region_id` (`region_id`),
  KEY `item_id` (`item_id`),
  KEY `item_type_id` (`item_type_id`),
  KEY `payment_type_id` (`payment_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
 
CREATE TABLE `subscriptions` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` varchar(64) NOT NULL,
  `product_id` int(11) NOT NULL,
  `resource_uuid` varchar(36) NOT NULL,
  `resource_name` varchar(255) NOT NULL,
  `expires_at` datetime DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,  # comfirmed, creating, deleting
  PRIMARY KEY (`id`),
  KEY `project_id` (`project_id`),
  KEY `product_id` (`product_id`),
  KEY `resource_uuid` (`resource_uuid`),
  KEY `expires_at` (`expires_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
 
CREATE TABLE `purchases` (
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `deleted` tinyint(1) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subscription_id` int(11) NOT NULL,
  `quantity` float NOT NULL,
  `line_total` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `subscription_id` (`subscription_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
