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
    url_id BIGINT AUTO_INCREMENT PRIMARY KEY, -- New primary key (auto-increment)
    url VARCHAR(2083) NOT NULL,               -- URL field (non-NULL)
    port_number INT NOT NULL,                 -- Port number (non-NULL)
    title VARCHAR(255),                       -- Nullable to handle cases where title is unavailable
    domain_name VARCHAR(255) NOT NULL,        -- Foreign key in DOMAINS table
    application_name VARCHAR(255),            -- Foreign key in APPLICATION_DEFINITION table
    FOREIGN KEY (domain_name) REFERENCES DOMAINS(domain_name) ON DELETE CASCADE,
    FOREIGN KEY (application_name) REFERENCES APPLICATION_DEFINITION(application_name) ON DELETE SET NULL
);

-- USER_CREDENTIALS TABLE
CREATE TABLE IF NOT EXISTS USER_CREDENTIALS (
    username VARCHAR(255) NOT NULL,       -- Username (non-NULL)
    password VARCHAR(255) NOT NULL,       -- Password (non-NULL)
    url_id BIGINT NOT NULL,               -- Foreign key in URLS table (using url_id)
    PRIMARY KEY (username, password, url_id), -- Composite primary key
    FOREIGN KEY (url_id) REFERENCES URLS(url_id) ON DELETE CASCADE
);

-- TAGS_DEFINITION TABLE
CREATE TABLE IF NOT EXISTS TAGS_DEFINITION (
    tag_name VARCHAR(255) PRIMARY KEY     -- Primary key, non-NULL
);

-- TAGS TABLE
CREATE TABLE IF NOT EXISTS TAGS (
    url_id BIGINT NOT NULL,               -- Foreign key in URLS table (using url_id)
    tag_name VARCHAR(255) NOT NULL,       -- Foreign key in TAGS_DEFINITION table
    PRIMARY KEY (url_id, tag_name),       -- Composite primary key
    FOREIGN KEY (url_id) REFERENCES URLS(url_id) ON DELETE CASCADE,
    FOREIGN KEY (tag_name) REFERENCES TAGS_DEFINITION(tag_name) ON DELETE CASCADE
);
