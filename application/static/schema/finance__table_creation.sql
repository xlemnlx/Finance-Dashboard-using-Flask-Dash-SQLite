DROP TABLE finance__table;

CREATE TABLE "finance__table" (
	"transact_id"	INTEGER NOT NULL,
	"transact_type"	VARCHAR(10) NOT NULL,
	"transact_sub_type"	VARCHAR(100) NOT NULL,
	"transact_date"	DATETIME,
	"money"	NUMERIC NOT NULL,
	"note"	VARCHAR(200),
	PRIMARY KEY("transact_id")
);