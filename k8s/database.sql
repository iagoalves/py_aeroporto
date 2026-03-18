
-- Criação da tabela 'aeroporto'
CREATE TABLE IF NOT EXISTS aeroporto (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    estado VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    codigo_iata VARCHAR(10),
    codigo_icao VARCHAR(10)
);

-- Criação da tabela 'companhia_aerea'
CREATE TABLE IF NOT EXISTS companhia_aerea (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    codigo VARCHAR(10) NOT NULL,
    pais VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS aeronave (
    id SERIAL PRIMARY KEY,
    modelo VARCHAR(100) NOT NULL,
    capacidade INTEGER NOT NULL,
    companhia_id INTEGER NOT NULL,
    FOREIGN KEY (companhia_id) REFERENCES companhia_aerea(id) ON DELETE CASCADE
);

CREATE TABLE companhia_aerea_aeronave (
    id SERIAL PRIMARY KEY,
    companhia_id INTEGER REFERENCES companhia_aerea(id),
    aeronave_id INTEGER REFERENCES aeronave(id)
);

-- Criação da tabela 'voo'
CREATE TABLE IF NOT EXISTS voo (
    id SERIAL PRIMARY KEY,
    numero_voo VARCHAR(20) NOT NULL,
    companhia_id INT NOT NULL,
    origem_id INT NOT NULL,
    destino_id INT NOT NULL,
    aeronave_id INT NOT NULL,
    partida_prevista TIMESTAMP NOT NULL,
    chegada_prevista TIMESTAMP NOT NULL,
    custo DECIMAL(10, 2) NOT NULL,  -- Adicionando a coluna de custo
    FOREIGN KEY (companhia_id) REFERENCES companhia_aerea(id),
    FOREIGN KEY (origem_id) REFERENCES aeroporto(id),
    FOREIGN KEY (destino_id) REFERENCES aeroporto(id),
    FOREIGN KEY (aeronave_id) REFERENCES aeronave(id)  -- Chave estrangeira para aeronave
);

-- Criação da tabela de clientes com CPF
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    cpf VARCHAR(14) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL
);

CREATE TABLE reservas (
    id SERIAL PRIMARY KEY,
    voo_id INTEGER,
    cliente_id INTEGER,
    localizador VARCHAR(100),
    numero_eticket VARCHAR(100),
    status_pagamento VARCHAR(20) DEFAULT 'pendente',
    FOREIGN KEY (voo_id) REFERENCES voo(id),  -- Chave estrangeira para voos
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)  -- Chave estrangeira para clientes
);

-- Inserção de aeroportos brasileiros com dados reais de cidade e estado
INSERT INTO aeroporto (nome, estado, cidade, pais, latitude, longitude, codigo_iata, codigo_icao) VALUES
('Aeroporto Internacional de São Paulo - Guarulhos', 'São Paulo', 'Guarulhos', 'Brasil', -23.4356, -46.4731, 'GRU', 'SBGR'),
('Aeroporto Santos Dumont', 'Rio de Janeiro', 'Rio de Janeiro', 'Brasil', -22.9100, -43.1636, 'SDU', 'SBRJ'),
('Aeroporto Internacional de Porto Alegre', 'Rio Grande do Sul', 'Porto Alegre', 'Brasil', -29.9933, -51.1719, 'POA', 'SBPA'),
('Aeroporto Internacional Tancredo Neves', 'Minas Gerais', 'Belo Horizonte', 'Brasil', -19.6306, -43.9678, 'CNF', 'SBCF'),
('Aeroporto Internacional de Brasília', 'Distrito Federal', 'Brasília', 'Brasil', -15.7800, -47.9292, 'BSB', 'SBBR'),
('Aeroporto Internacional dos Guararapes', 'Pernambuco', 'Recife', 'Brasil', -8.1281, -34.9186, 'REC', 'SBRF'),
('Aeroporto de Vitória', 'Espírito Santo', 'Vitória', 'Brasil', -20.2583, -40.2925, 'VIX', 'SBVT'),
('Aeroporto Internacional Salgado Filho', 'Rio Grande do Sul', 'Porto Alegre', 'Brasil', -29.9933, -51.1719, 'POA', 'SBPA'),
('Aeroporto Internacional de Belém', 'Pará', 'Belém', 'Brasil', -1.3792, -48.4769, 'BEL', 'SBBE'),
('Aeroporto Internacional Hercílio Luz', 'Santa Catarina', 'Florianópolis', 'Brasil', -27.6686, -48.5478, 'FLN', 'SBFL'),
('Aeroporto Internacional Pinto Martins', 'Ceará', 'Fortaleza', 'Brasil', -3.7764, -38.5328, 'FOR', 'SBFZ'),
('Aeroporto Internacional de Campinas', 'São Paulo', 'Campinas', 'Brasil', -23.0070, -47.1342, 'VCP', 'SBKP'),
('Aeroporto Internacional de Salvador', 'Bahia', 'Salvador', 'Brasil', -12.9086, -38.3231, 'SSA', 'SBSV'),
('Aeroporto Internacional de Recife', 'Pernambuco', 'Recife', 'Brasil', -8.1281, -34.9186, 'REC', 'SBRF'),
('Aeroporto Internacional de Manaus', 'Amazonas', 'Manaus', 'Brasil', -3.0432, -60.0474, 'MAO', 'SBEG'),
('Aeroporto Internacional de Foz do Iguaçu', 'Paraná', 'Foz do Iguaçu', 'Brasil', -25.5320, -54.4853, 'IGU', 'SBFI'),
('Aeroporto de Congonhas', 'São Paulo', 'São Paulo', 'Brasil', -23.6261, -46.6561, 'CGH', 'SBSP'),
('Aeroporto Internacional de Curitiba', 'Paraná', 'Curitiba', 'Brasil', -25.5206, -49.1751, 'CWB', 'SBCT'),
('Aeroporto Internacional de Cuiabá', 'Mato Grosso', 'Cuiabá', 'Brasil', -15.5981, -56.0981, 'CGB', 'SBCY');

-- Inserção de companhias aéreas
INSERT INTO companhia_aerea (nome, codigo, pais) VALUES
('LATAM Airlines', 'LATAM', 'Brasil'),
('Gol Linhas Aéreas', 'GOL', 'Brasil'),
('Azul Linhas Aéreas', 'Azul', 'Brasil'),
('Avianca Brasil', 'Avianca', 'Brasil'),
('Passaredo Linhas Aéreas', 'Passaredo', 'Brasil');


-- Inserção de aeronaves 
INSERT INTO aeronave (modelo, capacidade, companhia_id) VALUES
('A321neo', 244, 1),  -- LATAM → A321neo
('B737 MAX 8', 186, 2),  -- Gol → B737 MAX 8
('E195-E2', 136, 3),  -- Azul → E195-E2
('A320-200', 180, 4),  -- Avianca → A320-200
('ATR 72-600', 70, 5);  -- Passaredo → ATR 72-600

-- Inserção de voos comerciais reais
INSERT INTO voo (numero_voo, companhia_id, origem_id, destino_id, aeronave_id, partida_prevista, chegada_prevista, custo) VALUES
('LA3721', 1, 1, 2, 1, '2025-05-07 08:00:00', '2025-05-07 09:10:00', 343.31),
('G31645', 2, 1, 3, 2, '2025-05-07 09:30:00', '2025-05-07 11:00:00', 865.5),
('AD4562', 3, 4, 1, 3, '2025-05-07 07:45:00', '2025-05-07 09:15:00', 496.11),
('LA3745', 1, 5, 1, 4, '2025-05-07 10:00:00', '2025-05-07 11:30:00', 864.79),
('G31789', 2, 6, 7, 5, '2025-05-07 06:00:00', '2025-05-07 07:30:00', 1467.45),
('AD2345', 3, 8, 9, 1, '2025-05-07 12:00:00', '2025-05-07 14:30:00', 3194.46),
('LA3987', 1, 10, 1, 2, '2025-05-07 15:00:00', '2025-05-07 17:00:00', 514.62),
('G31234', 2, 11, 12, 3, '2025-05-07 13:00:00', '2025-05-07 14:30:00', 2329.93),
('AD5678', 3, 13, 14, 4, '2025-05-07 09:00:00', '2025-05-07 10:30:00', 648.85),
('LA4001', 1, 15, 1, 5, '2025-05-07 16:00:00', '2025-05-07 17:30:00', 2696.9),
('G31235', 2, 1, 3, 1, '2025-05-07 17:00:00', '2025-05-07 18:30:00', 865.5),
('AD5679', 3, 4, 5, 2, '2025-05-07 18:00:00', '2025-05-07 19:30:00', 599.43),
('LA4002', 1, 6, 7, 3, '2025-05-07 19:00:00', '2025-05-07 20:30:00', 1467.45),
('G31236', 2, 8, 9, 4, '2025-05-07 20:00:00', '2025-05-07 21:30:00', 3194.46),
('AD5680', 3, 10, 11, 5, '2025-05-07 21:00:00', '2025-05-07 22:30:00', 2861.14),
('LA4003', 1, 12, 13, 1, '2025-05-07 22:00:00', '2025-05-07 23:30:00', 1458.23),
('G31237', 2, 14, 15, 2, '2025-05-07 23:00:00', '2025-05-07 00:30:00', 2836.69),
('AD5681', 3, 1, 2, 3, '2025-05-08 00:00:00', '2025-05-08 01:30:00', 343.31),
('LA4004', 1, 3, 4, 4, '2025-05-08 01:00:00', '2025-05-08 02:30:00', 1361.6),
('G31238', 2, 5, 6, 5, '2025-05-08 02:00:00', '2025-05-08 03:30:00', 1650.27);


-- Inserção dos 20 clientes com CPF
INSERT INTO clientes (nome, email, telefone, cpf, senha_hash) VALUES
('Cliente 1', 'cliente1@exemplo.com', '123456789', '000.000.000-01', '$2b$12$Em6RoNOhi0LKJUEnYEiU1ujQkcVcziQ8.v9ZpDttNsi9slrnH0.U6'),
('Cliente 2', 'cliente2@exemplo.com', '987654321', '000.000.000-02', '$2b$12$98tbI4GxunfugED3Q1aTNeUbUjiuJeEOcdKxreQfMgGo/JLm6RVvi'),
('Cliente 3', 'cliente3@exemplo.com', '123123123', '000.000.000-03', '$2b$12$TsLfsxuc1REANLwFRD.VnO34TEdaCLpeMkAlozVpF1W9FbWA5KZbC'),
('Cliente 4', 'cliente4@exemplo.com', '456456456', '000.000.000-04', '$2b$12$kK4j7zs9LuGWThrUSkDyXuiLGb5AP0VU0PPgdVK.Oql5Ru8dqkH.O'),
('Cliente 5', 'cliente5@exemplo.com', '789789789', '000.000.000-05', '$2b$12$I6XVNXqnkIbsnHQ/irB5wO2DCDcf5Wx.a7Fairg68kroipNiR/LMK'),
('Cliente 6', 'cliente6@exemplo.com', '321321321', '000.000.000-06', '$2b$12$Ar3pfXZCqCtOOXFC0Bi1LOmRbr.4EdTAv3KH8obMxKDQQikd/CtMy'),
('Cliente 7', 'cliente7@exemplo.com', '654654654', '000.000.000-07', '$2b$12$vKAmX.WxH9RUdn6wfv/l/ukzjc9B1EzuT3qEGDOzhgLyiL/EAdcaq'),
('Cliente 8', 'cliente8@exemplo.com', '987987987', '000.000.000-08', '$2b$12$9SYwpDzclxl94VpA93VSWuIqDtzwp0grw5dPijhrIh21D95gCYxyK'),
('Cliente 9', 'cliente9@exemplo.com', '159159159', '000.000.000-09', '$2b$12$/z467u52K41PDtwIoqn1TeSYfoNkxvwkcNnXlK3YvKmUgS6u2rkhS'),
('Cliente 10', 'cliente10@exemplo.com', '753753753', '000.000.000-10', '$2b$12$Pbiq/4MCHgmHMoJ7qES2..TtSZTmJcWg/hjuU76qHkMW2yge.gxke'),
('Cliente 11', 'cliente11@exemplo.com', '852852852', '000.000.000-11', '$2b$12$5zgErEXpAlG3ObmJ/trWAuMTm.0k9XRIlS9QNMPNOt1hweW8UFkJS'),
('Cliente 12', 'cliente12@exemplo.com', '369369369', '000.000.000-12', '$2b$12$Ft4YYkFuHGLNR/fySeyIie1b/GhjTXBgfbgUC41NTIFmb5/s65Ou.'),
('Cliente 13', 'cliente13@exemplo.com', '468468468', '000.000.000-13', '$2b$12$w65SBA7cfefAEIAJJhC7Ce6u3NtCUzRcFj3jjMlIcXNaKrFEdd3qu'),
('Cliente 14', 'cliente14@exemplo.com', '159753159', '000.000.000-14', '$2b$12$hTnDLeH8c83Nf15ZWOo/4OMiW.KYik4TUHfoGGDo9PKN58bz44kp6'),
('Cliente 15', 'cliente15@exemplo.com', '753159753', '000.000.000-15', '$2b$12$v6FIRTAoQHXFZtD2gTkRyeoEzbiyrUliDVupvgVbOzMQOfpNrcO9G'),
('Cliente 16', 'cliente16@exemplo.com', '258258258', '000.000.000-16', '$2b$12$amjPm.J9D1tMtZJwvdHVk.vY1TcFkaILB5EUPdeLEUf5IlxQ0h5p.'),
('Cliente 17', 'cliente17@exemplo.com', '654123654', '000.000.000-17', '$2b$12$NzkWLidP9JH3eBO4ZojMheHBinnSrLKNLyewQt4mSoetacQJqi9T.'),
('Cliente 18', 'cliente18@exemplo.com', '987654123', '000.000.000-18', '$2b$12$m82lVy0mIHclqWc7Gm9OSes7fZeI8zyRGbFNl9zPK1jJtX33Kobum'),
('Cliente 19', 'cliente19@exemplo.com', '321654987', '000.000.000-19', '$2b$12$Q3QS5xC5c9Lss8jcs9bl.ub7tYpeGkR5YD1Y..edh.R4yAQXeJGwq'),
('Cliente 20', 'cliente20@exemplo.com', '987321654', '000.000.000-20', '$2b$12$9asNRQ7xB1F.FCcmqUA7auKMo9M7IySt8koewffRQ4YZcELu9vHba');

INSERT INTO reservas (voo_id, cliente_id, localizador, numero_eticket, status_pagamento)
VALUES
    (1, 1, 'LOC1234', 'ETICKET001', 'pago'),
    (2, 2, 'LOC1235', 'ETICKET002', 'pendente'),
    (3, 3, 'LOC1236', 'ETICKET003', 'pago'),
    (4, 4, 'LOC1237', 'ETICKET004', 'pendente'),
    (5, 5, 'LOC1238', 'ETICKET005', 'pago'),
    (6, 6, 'LOC1239', 'ETICKET006', 'pago'),
    (7, 7, 'LOC1240', 'ETICKET007', 'pendente'),
    (8, 8, 'LOC1241', 'ETICKET008', 'pago'),
    (9, 9, 'LOC1242', 'ETICKET009', 'pendente'),
    (10, 10, 'LOC1243', 'ETICKET010', 'pago'),
    (11, 11, 'LOC1244', 'ETICKET011', 'pendente'),
    (12, 12, 'LOC1245', 'ETICKET012', 'pago'),
    (13, 13, 'LOC1246', 'ETICKET013', 'pago'),
    (14, 14, 'LOC1247', 'ETICKET014', 'pendente'),
    (15, 15, 'LOC1248', 'ETICKET015', 'pago'),
    (16, 16, 'LOC1249', 'ETICKET016', 'pendente'),
    (17, 17, 'LOC1250', 'ETICKET017', 'pago'),
    (18, 18, 'LOC1251', 'ETICKET018', 'pendente'),
    (19, 19, 'LOC1252', 'ETICKET019', 'pago'),
    (20, 20, 'LOC1253', 'ETICKET020', 'pendente');
