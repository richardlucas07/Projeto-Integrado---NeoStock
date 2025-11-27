-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS NeoStock;

-- Uso do banco de dados
USE NeoStock;

-- Criação da tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    telefone VARCHAR(15),
    senha VARCHAR(50) NOT NULL
);

-- Criação da tabela de produtos
CREATE TABLE IF NOT EXISTS produtos (
    cod INT AUTO_INCREMENT PRIMARY KEY,
    produto VARCHAR(50) NOT NULL,
    quantidade INT,
    preco_unitario DECIMAL(10,2),
    preco_total DECIMAL(10,2)
);

-- Criação da tabela de fornecedores
CREATE TABLE IF NOT EXISTS fornecedores (
    cod INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cnpj VARCHAR(20) NOT NULL UNIQUE,
    telefone VARCHAR(15),
    produto VARCHAR(50)
);
SELECT * FROM usuarios;
SELECT * FROM produtos;
SELECT * FROM fornecedores;