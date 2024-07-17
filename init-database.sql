-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-06-07 01:27:37.867

-- tables
-- Table: consulta
CREATE TABLE consulta (
    id serial  NOT NULL,
    data_consulta date  NOT NULL,
    id_empresa int  NOT NULL,
    CONSTRAINT consulta_pk PRIMARY KEY (id)
);

-- Table: documento
CREATE TABLE documento (
    id serial  NOT NULL,
    tipo varchar(255)  NOT NULL,
    CONSTRAINT documento_pk PRIMARY KEY (id)
);

-- Table: empresa
CREATE TABLE empresa (
    id serial  NOT NULL,
    nome varchar(255)  NOT NULL,
    cnpj char(11)  NOT NULL,
    email varchar(255)  NOT NULL,
    CONSTRAINT empresa_pk PRIMARY KEY (id)
);

-- Table: empresa_documento
CREATE TABLE empresa_documento (
    id serial  NOT NULL,
    data_inicio date  NOT NULL,
    data_vencimento date  NOT NULL,
    id_empresa int  NOT NULL,
    id_documento int  NOT NULL,
    CONSTRAINT empresa_documento_pk PRIMARY KEY (id)
);

-- foreign keys
-- Reference: consulta_empresa (table: consulta)
ALTER TABLE consulta ADD CONSTRAINT consulta_empresa
    FOREIGN KEY (id_empresa)
    REFERENCES empresa (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: empresa_documento_documento (table: empresa_documento)
ALTER TABLE empresa_documento ADD CONSTRAINT empresa_documento_documento
    FOREIGN KEY (id_documento)
    REFERENCES documento (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: empresa_documento_empresa (table: empresa_documento)
ALTER TABLE empresa_documento ADD CONSTRAINT empresa_documento_empresa
    FOREIGN KEY (id_empresa)
    REFERENCES empresa (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

