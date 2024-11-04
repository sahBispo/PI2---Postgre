#pip install flask 
#pip install mysql-connector-python

from flask import Flask, request, render_template, redirect, jsonify, session
#import mysql.connector
import psycopg2
from psycopg2 import sql

# A chave secreta é usada para assinar os cookies de sessão, garantindo que não possam ser falsificados ou manipulados por terceiros
PI2 = Flask(__name__)

#
PI2.secret_key = 'teste'


def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-cskctudds78s7399k91g-a",
        database="adestra",
        user="adestra_user",
        password="DxZMLInXvHMdyQTvq50h6Wf55zdxuzBY"
    )
    return conn

# Função para criar as tabelas no banco de dados, se ainda não existirem
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL para criar a tabela Tutor
    create_tutor_table = """
    CREATE TABLE IF NOT EXISTS Tutor (
        id_resp SERIAL PRIMARY KEY,
        Nome VARCHAR(80), 
        Email VARCHAR(50) UNIQUE,
        Senha VARCHAR(15), 
        Endereco VARCHAR(200),
        Telefone BIGINT,
        Autoriza_imagem VARCHAR(3),
        CONSTRAINT autoriza_imagem_check CHECK (Autoriza_imagem IN ('Sim', 'Não'))
    );
    """

    # SQL para criar a tabela Animal
    create_animal_table = """
    CREATE TABLE IF NOT EXISTS Animal (
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
    """

    # Executa os comandos SQL para criar as tabelas
    try:
        cursor.execute(create_tutor_table)
        cursor.execute(create_animal_table)
        conn.commit()
        print("Tabelas Tutor e Animal criadas com sucesso.")
    except Exception as e:
        print("Erro ao criar tabelas:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Chama a função de criação de tabelas
create_tables()

# Definição das rotas
# Rota para a página de inical
@PI2.route('/')
def pagina_inicial():
    return render_template('index.html')

# Rota para a página de Login
@PI2.route('/login')
def pagina_login():
    return render_template('login.html')

# Rota para a página de Cadastro
@PI2.route('/cadastro')
def pagina_cadastro():
    return render_template('cadastro.html')

# Rota para a página de Agenda
@PI2.route('/agenda')
def pagina_agenda():
    return render_template('agenda.html')

# Rota para a página de Adestramento
@PI2.route('/adestramento')
def pagina_adestramento():
    return render_template('adestramento.html')

# Rota para a página de Quem
@PI2.route('/quem')
def pagina_quem():
    return render_template('quem.html')



@PI2.route('/salvar-dados', methods=['POST'])
def salvar_dados():
    data = request.json
    Nome = data.get('Nome')
    Email = data.get('Email')
    Senha = data.get('Senha')
    Endereco = data.get('Endereco')
    Telefone = data.get('Telefone')
    Autoriza_imagem = data.get('Autoriza_imagem')

    dados = (Nome, Email, Senha, Endereco, Telefone, Autoriza_imagem)
    print(dados)

    conn = get_db_connection()
    cursor = conn.cursor()
            
    cursor.execute("INSERT INTO Tutor (Nome, Email, Senha, Endereco, Telefone, Autoriza_imagem) VALUES (%s, %s, %s, %s, %s, %s)", 
        (Nome, Email, Senha, Endereco, Telefone, Autoriza_imagem))

    # Obtém o último ID inserido e armazena na sessão
    cursor.execute("SELECT LASTVAL()")
    tutor_id = cursor.fetchone()[0]
    session['tutor_id'] = tutor_id
    print("ID do tutor na sessão:", session.get('tutor_id'))

    conn.commit()

    

    # Fecha o cursor e a conexão
    cursor.close()
    conn.close()

# Obtém o último ID inserido (id do Tutor) e armazena na sessão
    '''tutor_id = cursor.lastrowid
    session['tutor_id'] = tutor_id
    print("ID do tutor na sessão:", session.get('tutor_id'))'''

    return render_template('cadastro.html')

@PI2.route('/salvar-animal', methods=['POST'])
def salvar_animal():
    print("Requisição para salvar animal recebida")  # Verifique se esta linha aparece
    data = request.json
    
    Nome = data.get('Nome')
    Raca = data.get('Raca')
    idade = data.get('idade')
    Sexo = data.get('Sexo')
    Castrado = data.get('Castrado')
    id_resp = session.get('tutor_id')
    print("ID do tutor:", id_resp)  # Debugging
   

    dados1 = (Nome, Raca, idade, Sexo, Castrado)
    print(dados1)

    # Obtém o último ID inserido (id do Tutor) e armazena na sessão
    print("ID do tutor na sessão:", session.get('tutor_id'))

    conn = get_db_connection()
    cursor = conn.cursor()

    if id_resp:
        cursor.execute("INSERT INTO animal (Nome, Raca, idade, Sexo, Castrado, id_resp_animal) VALUES (%s, %s, %s, %s, %s, %s)", 
                        (Nome, Raca, idade, Sexo, Castrado, id_resp))
    
        conn.commit()    
        cursor.close()
        conn.close()

        return jsonify({'mensagem': 'Animal cadastrado com sucesso!'}), 200

    else:
        return jsonify({'mensagem': 'Erro: Tutor não identificado'}), 400



# Rota para verificar as credenciais de login e redirecionar para home de acesso
@PI2.route('/verificar-login', methods=['POST'])
def verificar_login():
    data = request.json
    Email = data['Email']
    Senha = data['Senha']
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Consulta SQL para verificar o login no banco de dados
    cursor.execute("SELECT * FROM Tutor WHERE Email = %s AND Senha = %s", (Email, Senha))
    responsavel = cursor.fetchone()
    print(responsavel)
    
    conn.commit()    
    cursor.close()
    conn.close()

    if responsavel:
        return jsonify({'redirect_url': '/agenda'}), 200 
    else:
        return jsonify({'mensagem': 'Login inválido'}), 401
    


if __name__ == '__main__':
    PI2.run(debug=True)  