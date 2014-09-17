BEGIN;
CREATE TABLE `iaq_sensornode` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `node_id` varchar(10) NOT NULL,
    `description` varchar(30) NOT NULL,
    `temp` double precision,
    `humi` double precision,
    `iaqengine` integer,
    `tgs2600` integer,
    `tgs2602` integer,
    `time` datetime NOT NULL
)
;
CREATE TABLE `iaq_sensordata` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `node_id` varchar(10) NOT NULL,
    `temp` double precision NOT NULL,
    `humi` double precision NOT NULL,
    `iaqengine` integer NOT NULL,
    `tgs2600` integer NOT NULL,
    `tgs2602` integer NOT NULL,
    `time` datetime NOT NULL
)
;
COMMIT;
