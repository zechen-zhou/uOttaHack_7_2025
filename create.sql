-- DOMAINS TABLE
CREATE TABLE IF NOT EXISTS DOMAINS (
    domain_name VARCHAR(255) PRIMARY KEY, -- Primary key, non-NULL
    ip_address VARCHAR(45),              -- IP address (nullable for unresolved domains)
    routable BOOLEAN NOT NULL            -- Boolean to indicate if the domain is routable
);

-- APPLICATION_DEFINITION TABLE
CREATE TABLE IF NOT EXISTS APPLICATION_DEFINITION (
    application_name VARCHAR(255) PRIMARY KEY -- Primary key, non-NULL
);

-- URLS TABLE
CREATE TABLE IF NOT EXISTS URLS (
    url VARCHAR(2083) PRIMARY KEY,        -- Primary key, non-NULL (max URL length: 2083 characters)
    port_number INT NOT NULL,             -- Port number (non-NULL)
    title VARCHAR(255),                   -- Nullable to handle cases where title is unavailable
    domain_name VARCHAR(255) NOT NULL,    -- Foreign key in DOMAINS table
    application_name VARCHAR(255),        -- Foreign key in APPLICATION_DEFINITION table
    FOREIGN KEY (domain_name) REFERENCES DOMAINS(domain_name) ON DELETE CASCADE,
    FOREIGN KEY (application_name) REFERENCES APPLICATION_DEFINITION(application_name) ON DELETE SET NULL
);

-- USER_CREDENTIALS TABLE
CREATE TABLE IF NOT EXISTS USER_CREDENTIALS (
    username VARCHAR(255) NOT NULL,       -- Username (non-NULL)
    password VARCHAR(255) NOT NULL,       -- Password (non-NULL)
    url VARCHAR(2083) NOT NULL,           -- Foreign key in URLS table
    PRIMARY KEY (username, password, url),-- Composite primary key
    FOREIGN KEY (url) REFERENCES URLS(url) ON DELETE CASCADE
);

-- TAGS_DEFINITION TABLE
CREATE TABLE IF NOT EXISTS TAGS_DEFINITION (
    tag_name VARCHAR(255) PRIMARY KEY     -- Primary key, non-NULL
);

-- TAGS TABLE
CREATE TABLE IF NOT EXISTS TAGS (
    url VARCHAR(2083) NOT NULL,           -- Foreign key in URLS table
    tag_name VARCHAR(255) NOT NULL,       -- Foreign key in TAGS_DEFINITION table
    PRIMARY KEY (url, tag_name),          -- Composite primary key
    FOREIGN KEY (url) REFERENCES URLS(url) ON DELETE CASCADE,
    FOREIGN KEY (tag_name) REFERENCES TAGS_DEFINITION(tag_name) ON DELETE CASCADE
);
