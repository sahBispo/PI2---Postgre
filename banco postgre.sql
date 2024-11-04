-- Criando a tabela do tutor:
create table Tutor(
id_resp serial primary key,
Nome varchar (80), 
Email varchar (50) unique,
Senha varchar (15), 
Endereco varchar (200),
Telefone Bigint,
Autoriza_imagem VARCHAR(3),
    CONSTRAINT autoriza_imagem_check CHECK (
        Autoriza_imagem IN ('Sim', 'Não')
    )
);


-- criando a tabela do animal
CREATE TABLE Animal (
    id_animal SERIAL PRIMARY KEY,
    Nome VARCHAR(100),
    Raca VARCHAR(50),
    idade INT,
    Sexo VARCHAR(6),
    Castrado VARCHAR(3),
    id_resp_animal INT NOT NULL,
    CONSTRAINT sexo_check CHECK (Sexo IN ('Macho', 'Femea')),
    CONSTRAINT castrado_check CHECK (Castrado IN ('Sim', 'Não')),
    FOREIGN KEY (id_resp_animal) REFERENCES Tutor (id_resp)
);

INSERT INTO Tutor (Nome, Email, Senha, Endereco, Telefone, Autoriza_imagem)
VALUES ('João', 'oaomanuel@gmail.com', '12345', 'Rua teste tes testes', 1192354698, 'Sim');

INSERT INTO animal (Nome, Raca, Idade, Sexo, Castrado, id_resp_animal)
VALUES ('Sasha', 'vira lata', 4, 'Femea', 'Sim', 01); 


Select * from Tutor;
Select *from animal;

