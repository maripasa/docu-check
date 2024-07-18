-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-07-17 17:06:31.132

-- tables
-- Table: companies
CREATE TABLE companies (
    id serial  NOT NULL,
    name varchar(255)  NOT NULL,
    cnpj char(11)  NOT NULL,
    email varchar(255)  NOT NULL,
    CONSTRAINT companies_pk PRIMARY KEY (id)
);

-- Table: company_document
CREATE TABLE company_document (
    id serial  NOT NULL,
    start_date timestamp  NOT NULL,
    expiry_date timestamp  NOT NULL,
    id_company int  NOT NULL,
    id_document int  NOT NULL,
    CONSTRAINT company_document_pk PRIMARY KEY (id)
);

-- Table: consultations
CREATE TABLE consultations (
    id serial  NOT NULL,
    consultation_date timestamp  NOT NULL,
    id_company int  NOT NULL,
    CONSTRAINT consultations_pk PRIMARY KEY (id)
);

-- Table: documents
CREATE TABLE documents (
    id serial  NOT NULL,
    type varchar(255)  NOT NULL,
    CONSTRAINT documents_pk PRIMARY KEY (id)
);

-- foreign keys
-- Reference: consulta_empresa (table: consultations)
ALTER TABLE consultations ADD CONSTRAINT consulta_empresa
    FOREIGN KEY (id_company)
    REFERENCES companies (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: empresa_documento_documento (table: company_document)
ALTER TABLE company_document ADD CONSTRAINT empresa_documento_documento
    FOREIGN KEY (id_document)
    REFERENCES documents (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: empresa_documento_empresa (table: company_document)
ALTER TABLE company_document ADD CONSTRAINT empresa_documento_empresa
    FOREIGN KEY (id_company)
    REFERENCES companies (id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.