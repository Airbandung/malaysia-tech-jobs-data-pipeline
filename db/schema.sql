--BRONZE LAYER
CREATE TABLE raw_jobs (
    raw_job_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    source VARCHAR(100) NOT NULL,
    external_job_id VARCHAR(255) NOT NULL,

    raw_data JSONB NOT NULL,

    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    processing_status VARCHAR(50) DEFAULT 'pending',
    processed_at TIMESTAMP,

    error_message TEXT,

    UNIQUE(source, external_job_id)
);

--SILVER LAYER
CREATE TABLE companies (
    company_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    name VARCHAR(255) NOT NULL UNIQUE,

    website_url TEXT,
    logo_url TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE locations (
    location_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),

    latitude NUMERIC,
    longitude NUMERIC,

    UNIQUE(city, state, country)
);

CREATE TABLE jobs (
    job_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    raw_job_id BIGINT REFERENCES raw_jobs(raw_job_id),

    source VARCHAR(100),
    external_job_id VARCHAR(255),

    company_id BIGINT REFERENCES companies(company_id),
    location_id BIGINT REFERENCES locations(location_id),

    title VARCHAR(255) NOT NULL,
    description TEXT,

    employment_type VARCHAR(50),

    salary_min NUMERIC,
    salary_max NUMERIC,
    salary_period VARCHAR(20),

    work_arrangement VARCHAR(50),
    seniority_level VARCHAR(50),

    required_experience_years INT,

    visa_sponsorship BOOLEAN,

    posted_at TIMESTAMP,

    is_active BOOLEAN DEFAULT TRUE,
    expired_at TIMESTAMP,

    metadata JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(source, external_job_id)
);

CREATE TABLE skills (
    skill_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE job_skills (
    job_id BIGINT REFERENCES jobs(job_id)
        ON DELETE CASCADE,

    skill_id BIGINT REFERENCES skills(skill_id)
        ON DELETE CASCADE,

    skill_type VARCHAR(50),

    PRIMARY KEY(job_id, skill_id)
);

CREATE TABLE benefits (
    benefit_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    name VARCHAR(100) UNIQUE
);

CREATE TABLE job_benefits (
    job_id BIGINT REFERENCES jobs(job_id)
        ON DELETE CASCADE,

    benefit_id BIGINT REFERENCES benefits(benefit_id)
        ON DELETE CASCADE,

    PRIMARY KEY(job_id, benefit_id)
);

--GOLD LAYER
CREATE TABLE job_statistics (
    statistic_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    state VARCHAR(100),

    total_jobs INT,

    average_salary NUMERIC,

    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE skill_trends (
    trend_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    skill_id BIGINT REFERENCES skills(skill_id),

    month DATE,

    demand_count INT
);