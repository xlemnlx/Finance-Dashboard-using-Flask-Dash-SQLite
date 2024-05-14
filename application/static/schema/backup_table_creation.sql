CREATE TABLE IF NOT EXISTS "backup_table" (
	"backup_id" INTEGER NOT NULL,
	"backup_name" VARCHAR(100) NOT NULL,
	"backup_date"	DATETIME,
	"note" VARCHAR(200),
	PRIMARY KEY("backup_id")
);