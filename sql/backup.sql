-- =========================================
-- CRIAR BANCO
-- =========================================
CREATE DATABASE IF NOT EXISTS weia;
USE weia;

-- =========================================
-- EMPRESAS
-- =========================================
CREATE TABLE companies (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- USUÁRIOS
-- =========================================
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    company_id BIGINT NOT NULL,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- =========================================
-- PASTAS
-- =========================================
CREATE TABLE folders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    company_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    name VARCHAR(200) NOT NULL,
    parent_id BIGINT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES folders(id) ON DELETE CASCADE
);

-- =========================================
-- INDEXES
-- =========================================
CREATE INDEX idx_company_name ON companies(name);
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_user_company ON users(company_id);
CREATE INDEX idx_folder_user ON folders(user_id);
CREATE INDEX idx_folder_parent ON folders(parent_id);

-- =========================================
-- DADOS INICIAIS
-- =========================================

-- EMPRESA
INSERT INTO companies (name)
VALUES ('WeIA Tecnologia');

-- USUÁRIOS
INSERT INTO users (company_id, name, email, password_hash)
VALUES
(1, 'Wellington', 'wellington@weia.com', '$2b$12$hashbcrypt1'),
(1, 'Admin', 'admin@weia.com', '$2b$12$hashbcrypt2');

-- PASTAS PRINCIPAIS
INSERT INTO folders (company_id, user_id, name, parent_id)
VALUES
(1, 1, 'Documentos', NULL),
(1, 1, 'Projetos', NULL),
(1, 2, 'Administrativo', NULL);

-- SUBPASTAS
INSERT INTO folders (company_id, user_id, name, parent_id)
VALUES
(1, 1, 'IA', 2),
(1, 1, 'Backend', 2),
(1, 1, 'Contratos', 1),
(1, 2, 'Financeiro', 3);