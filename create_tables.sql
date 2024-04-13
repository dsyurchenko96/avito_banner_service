-- Create tables for banners, features, tags, and users
CREATE TABLE banners IF NOT EXISTS (
    banner_id SERIAL PRIMARY KEY,
    feature_id INTEGER REFERENCES features(feature_id),
    content JSONB NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE features IF NOT EXISTS (
    feature_id SERIAL PRIMARY KEY
);

CREATE TABLE tags IF NOT EXISTS (
    tag_id SERIAL PRIMARY KEY
);

CREATE TABLE users IF NOT EXISTS (
    id SERIAL PRIMARY KEY,
    tag_id INTEGER REFERENCES tags(tag_id)
    token VARCHAR(255) NOT NULL
);

CREATE TABLE admins IF NOT EXISTS (
    id SERIAL PRIMARY KEY,
    token VARCHAR(255) NOT NULL
);

CREATE TABLE banner_tags IF NOT EXISTS (
    banner_id INTEGER REFERENCES banners(banner_id),
    tag_id INTEGER REFERENCES tags(tag_id),
    PRIMARY KEY (banner_id, tag_id)
);

-- Create a table to manage the relationships between banners and tags/features
--CREATE TABLE banner_tag IF NOT EXISTS (
--    banner_id INT,
--    tag_id INT,
--    FOREIGN KEY (banner_id) REFERENCES banners(banner_id),
--    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
--);

--CREATE TABLE banner_feature IF NOT EXISTS (
--    banner_id INT,
--    feature_id INT,
--    FOREIGN KEY (banner_id) REFERENCES banners(banner_id),
--    FOREIGN KEY (feature_id) REFERENCES features(tag_id)
--);

-- Insert sample data if needed
INSERT INTO features DEFAULT VALUES
SELECT generate_series(1, 10);
INSERT INTO tags DEFAULT VALUES
SELECT generate_series(1, 10);



-- Add indexes or constraints as needed
