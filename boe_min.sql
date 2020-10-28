-- For SQLite DBs
-- conn.executescript(sql_script_string)
-- minutes DB schema planning
-- SQLite is loosely typed, meaning you can put almost any data in any column,
--  regardless of the defined type. (Except for int PKs. I think.)
;

CREATE TABLE IF NOT EXISTS minutes(
    min_id INTEGER CONSTRAINT min_id_pk PRIMARY KEY AUTOINCREMENT,  -- id number for minutes since there have been multiple meetings on the same day
    min_filename TEXT NOT NULL,  -- the filename on disk of the minutes pdf
    min_date TEXT NOT NULL,  -- the meeting date
    min_text TEXT NOT NULL  -- the raw text of the minutes (with encoding corrections)
);

CREATE TABLE IF NOT EXISTS contractors(
    con_id INTEGER CONSTRAINT con_id_pk PRIMARY KEY AUTOINCREMENT,  -- id number for the contractor
    con_name TEXT NOT NULL,  -- the name of the contractor (used for human-readable outputs)
    con_acc_id TEXT NOT NULL,  -- the account number associated with this contractor
    con_state TEXT NOT NULL,  -- the state the contractor is based in (MD, VA, PA, DE, etc)
    con_address TEXT NOT NULL,  -- the address the contractor can be found at
    con_notes TEXT,  -- any notes made on this contractor
    con_type_id INTEGER NOT NULL,  -- id for what type of contractor they are (see TABLE contractor_types)
    con_mwbe INTEGER NOT NULL,  -- 0 for no, 1 for yes; allows further specification into the future (e.g., 0 for no, 1+ for different kinds)
    CONSTRAINT con_type_id_fk FOREIGN KEY (con_type_id) REFERENCES contractor_types(con_type_id),
    CONSTRAINT con_acc_id_fk FOREIGN KEY (con_acc_id) REFERENCES accounts (acc_id)
);

CREATE TABLE IF NOT EXISTS contractor_types(
    con_type_id INTEGER CONSTRAINT con_type_id_pk PRIMARY KEY AUTOINCREMENT,  -- id number for contractor type
    con_type_name TEXT NOT NULL  -- what the contractor type is (for human-readable outputs)
);

CREATE TABLE IF NOT EXISTS departments(
    dept_id INTEGER CONSTRAINT dept_id_pk PRIMARY KEY AUTOINCREMENT,  -- dept id number
    dept_name TEXT NOT NULL  -- name of the department (for human-readable outputs)
);

CREATE TABLE IF NOT EXISTS applicants(
    appl_id INTEGER CONSTRAINT app_id_pk PRIMARY KEY AUTOINCREMENT,  -- id number for applicants
    appl_name TEXT NOT NULL,  -- name of the person/org filing the application (they may not be a contractor)
    appl_address TEXT NOT NULL,  -- address of the person/org filing the application
    appl_con_id INTEGER,  -- the contractor id (if applicable, contractors can file applications too)
    CONSTRAINT appl_con_id_fk FOREIGN KEY (appl_con_id) REFERENCES contractors (con_id)
);

CREATE TABLE IF NOT EXISTS permits(
    perm_id INTEGER CONSTRAINT perm_id_pk PRIMARY KEY AUTOINCREMENT,  -- id number for the permit
    perm_address TEXT NOT NULL,  -- the address/location the permit is for
    perm_payment INTEGER NOT NULL,  -- the total cost of the permit
    perm_date TEXT,  -- the date the permit is for
    perm_grant_date TEXT NOT NULL,  -- the date the permit was granted
    perm_appl_date TEXT NOT NULL,  -- the date the permit was applied for
    perm_appl_id INTEGER NOT NULL,  -- the id number of the applicant (see TABLE applicants)
    perm_desc TEXT NOT NULL,  -- the text of the permit
    perm_notes TEXT,  -- any additional notes for this permit
    perm_objections TEXT,  -- any objections to the denial/issuance of the permit
    CONSTRAINT perm_appl_id_fk FOREIGN KEY (appl_id) REFERENCES applicants (appl_id)
);

CREATE TABLE IF NOT EXISTS prequal(
    prq_id INTEGER CONSTRAINT prq_id_pk PRIMARY KEY AUTOINCREMENT,  -- id number for a specific prequalification
    min_date TEXT NOT NULL,  -- the date the prequal was issued (also the date of the meeting when they were prequalified)
    prq_amount INTEGER,  -- the amount of money the prequal was for
    con_id INTEGER NOT NULL,  -- the id of the contractor being prequalified
    prq_objections TEXT,  -- any objections to the denial/approval of the prequalification
    CONSTRAINT prq_con_type_id_fk FOREIGN KEY (con_type_id) REFERENCES contractor_types (con_type_id),
    CONSTRAINT prq_con_id_fk FOREIGN KEY (con_id) REFERENCES contractors (con_id),
    CONSTRAINT prq_min_date FOREIGN KEY (min_date) REFERENCES minutes (min_date)
);

CREATE TABLE IF NOT EXISTS payments(
    pay_id INTEGER CONSTRAINT pay_id_pk PRIMARY KEY AUTOINCREMENT,  -- id number for a specific payment
    pay_from_acc_id TEXT NOT NULL,  -- the account the money comes from
    pay_to_acc_id TEXT NOT NULL,  -- the account the money goes to
    pay_amount INTEGER NOT NULL,  -- how much money moved
    pay_date TEXT NOT NULL,  -- date of the transaction
    pay_chargeback INTEGER,  -- if the payment was reversed (optionally, how much was refunded)
    CONSTRAINT pay_from_acc_id_fk FOREIGN KEY (from_acc_id) REFERENCES accounts (acc_id),
    CONSTRAINT pay_to_acc_id_fk FOREIGN KEY (to_acc_id) REFERENCES accounts (acc_id)
);

CREATE TABLE IF NOT EXISTS accounts(
    acc_id TEXT CONSTRAINT acc_id PRIMARY KEY AUTOINCREMENT,  -- id number of the account
    acc_name TEXT NOT NULL  -- the name of the account (for human-readable outputs)
);