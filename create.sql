-- Domains Table
CREATE TABLE Domains (
    domain_name VARCHAR(255) PRIMARY KEY, -- Primary key, non-NULL
    ip_address VARCHAR(45),              -- IP address (nullable for unresolved domains)
    routable BOOLEAN NOT NULL            -- Boolean to indicate if the domain is routable
);

-- Application Definition Table
CREATE TABLE ApplicationDefinition (
    application_name VARCHAR(255) PRIMARY KEY -- Primary key, non-NULL
);

-- URLs Table
CREATE TABLE URLs (
    url VARCHAR(2083) PRIMARY KEY,        -- Primary key, non-NULL (max URL length: 2083 characters)
    port_number INT NOT NULL,             -- Port number (non-NULL)
    title VARCHAR(255),                   -- Nullable to handle cases where title is unavailable
    domain_name VARCHAR(255) NOT NULL,    -- Foreign key in Domains table
    application_name VARCHAR(255),        -- Foreign key in ApplicationDefinition table
    FOREIGN KEY (domain_name) REFERENCES Domains(domain_name) ON DELETE CASCADE,
    FOREIGN KEY (application_name) REFERENCES ApplicationDefinition(application_name) ON DELETE SET NULL
);

-- Username and Password Table
CREATE TABLE UserCredentials (
    username VARCHAR(255) NOT NULL,       -- Username (non-NULL)
    password VARCHAR(255) NOT NULL,       -- Password (non-NULL)
    url VARCHAR(2083) NOT NULL,           -- Foreign key in URLs table
    PRIMARY KEY (username, password, url),-- Composite primary key
    FOREIGN KEY (url) REFERENCES URLs(url) ON DELETE CASCADE
);

-- Tags Definition Table
CREATE TABLE TagsDefinition (
    tag_name VARCHAR(255) PRIMARY KEY     -- Primary key, non-NULL
);

-- Tags Table
CREATE TABLE Tags (
    url VARCHAR(2083) NOT NULL,           -- Foreign key in URLs table
    tag_name VARCHAR(255) NOT NULL,       -- Foreign key in TagsDefinition table
    PRIMARY KEY (url, tag_name),          -- Composite primary key
    FOREIGN KEY (url) REFERENCES URLs(url) ON DELETE CASCADE,
    FOREIGN KEY (tag_name) REFERENCES TagsDefinition(tag_name) ON DELETE CASCADE
);
