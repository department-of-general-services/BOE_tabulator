-- For SQLite DBs
-- conn.executescript(sql_script_string)
-- By Rob Nunn Sep 6, 2020
-- minutes DB schema planning

CREATE TABLE IF NOT EXISTS minutes(
    min_id INTEGER CONSTRAINT min_id_pk PRIMARY KEY AUTOINCREMENT,
    min_filename TEXT NOT NULL,
    min_date TEXT NOT NULL,
    min_text, TEXT NOT NULL  
)

CREATE TABLE IF NOT EXISTS contractors(
    con_id INTEGER CONSTRAINT con_id_pk PRIMARY KEY AUTOINCREMENT,
    con_name TEXT NOT NULL,
    con_acc_id TEXT NOT NULL,
    con_state TEXT NOT NULL,
    con_address TEXT NOT NULL,
    con_notes TEXT,
    con_type_id INTEGER NOT NULL,
    con_mwbe INTEGER,  -- 0 for no, 1 for yes; allows further specification into the future (e.g., 0 for no, 1+ for different kinds)
    CONSTRAINT con_type_id_fk FOREIGN KEY (con_type_id) REFERENCES contractor_types(con_type_id),
    CONSTRAINT con_acc_id_fk FOREIGN KEY (con_acc_id) REFERENCES accounts (acc_id)
);

CREATE TABLE IF NOT EXISTS contractor_types(
    con_type_id INTEGER CONSTRAINT con_type_id_pk PRIMARY KEY AUTOINCREMENT,
    con_type_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS departments(
    dept_id INTEGER CONSTRAINT dept_id_pk PRIMARY KEY AUTOINCREMENT,
    dept_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS applicants(
    appl_id INTEGER CONSTRAINT app_id_pk PRIMARY KEY AUTOINCREMENT,
    appl_name TEXT NOT NULL,
    appl_address TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS permits(
    perm_id INTEGER CONSTRAINT perm_id_pk PRIMARY KEY AUTOINCREMENT,
    perm_address TEXT NOT NULL,
    perm_payment INTEGER NOT NULL,
    perm_date TEXT,
    perm_grant_date TEXT NOT NULL,
    perm_appl_id INTEGER NOT NULL,
    perm_desc TEXT NOT NULL,
    perm_notes TEXT,
    perm_objections TEXT,
    CONSTRAINT perm_appl_id_fk FOREIGN KEY (appl_id) REFERENCES applicants (appl_id)
);

CREATE TABLE IF NOT EXISTS prequal(
    prq_id INTEGER CONSTRAINT prq_id_pk PRIMARY KEY AUTOINCREMENT,
    min_date TEXT NOT NULL,
    prq_amount INTEGER,
    con_type_id INTEGER NOT NULL,
    con_id INTEGER NOT NULL,
    prq_objections TEXT,
    CONSTRAINT prq_con_type_id_fk FOREIGN KEY (con_type_id) REFERENCES contractor_types (con_type_id),
    CONSTRAINT prq_con_id_fk FOREIGN KEY (con_id) REFERENCES contractors (con_id),
    CONSTRAINT prq_min_date FOREIGN KEY (min_date) REFERENCES minutes (min_date)
);

CREATE TABLE IF NOT EXISTS payments(
    pay_id INTEGER CONSTRAINT pay_id_pk PRIMARY KEY AUTOINCREMENT,
    from_acc_id TEXT NOT NULL,
    to_acc_id TEXT NOT NULL,
    pay_amount INTEGER NOT NULL,
    pay_date TEXT NOT NULL,
    pay_chargeback INTEGER,
    CONSTRAINT pay_from_acc_id_fk FOREIGN KEY (from_acc_id) REFERENCES accounts (acc_id),
    CONSTRAINT pay_to_acc_id_fk FOREIGN KEY (to_acc_id) REFERENCES accounts (acc_id)
);

CREATE TABLE IF NOT EXISTS accounts(
    acc_id TEXT CONSTRAINT acc_id PRIMARY KEY AUTOINCREMENT,
    acc_name TEXT NOT NULL,

);