USE `cyber_parking_db_test`;

DELETE FROM `car_movements` WHERE 1=1;
DELETE FROM `car_plates` WHERE 1=1;
INSERT INTO `car_plates` (`car_plate_id`, `plate_number`) VALUES
(5, 'E0PARK'),
(3, 'EPI05142'),
(4, 'EPIMS25'),
(2, 'EZG2AC5'),
(1, 'WE600SC');

DELETE FROM `parking_spaces`  WHERE 1=1;
INSERT INTO `parking_spaces` (`parking_space_id`) VALUES
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10),
(11),
(12),
(13),
(14),
(15);
-- DELETE FROM  WHERE 1=1;
