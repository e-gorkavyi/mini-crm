SELECT
	`projects`.`id` AS `id`,
	DATE_FORMAT(`projects`.`create_dt`,'%y-%m-%d') AS `create_dt`,
	`partners`.`name` AS `partner_name`,
	`projects`.`partner_id` AS `partner_id`,
	`projects`.`project_name` AS `project_name`,
	`projects`.`quantity` AS `quantity`,`projects`.`amount` AS `amount`,
	DATE_FORMAT(`projects`.`deadline`,'%y-%m-%d') AS `deadline`,
	if((ISNULL(`projects`.`invoice_num`) OR (`projects`.`invoice_num` = '') OR (`projects`.`invoice_num` = ' ')),'', CONCAT(`projects`.`invoice_num`,'/', DATE_FORMAT(`projects`.`invoice_date`,'%y.%m.%d'))) AS `invoice_num`,
	`project_statuses`.`name` AS `status_name`,
	`projects`.`status_id` AS `status_id`
FROM ((`projects`
LEFT JOIN `partners` ON((`projects`.`partner_id` = `partners`.`id`)))
LEFT JOIN `project_statuses` ON((`projects`.`status_id` = `project_statuses`.`id`)))
ORDER BY `projects`.`create_dt`