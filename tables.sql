/*
    Este e o arquivo de configuração do DB.
    Aqui é onde a tabela é criada e configurada
    (talvez um perfil padrão ¯\_(ツ)_/¯)
*/

/*
    Lista de códigos de sala:
    1°A = tbmb1b
    1°B = tbmb1c
    1°C = tbmb1d
    2°A = ucnc2c
    2°B = ucnc2d
    2°C = ucnc2e
    3°A = vdod3d
    3°B = vdod3e
    3°C = vdod3f
*/

-- Cria a tabela
create database Tabela;

-- Cria o acesso
grant all on Tabela.* to 'webDB' identified by 'DBpasswd';

-- Cria a tabela de usuários
create table users(
    id int auto_increment primary key,
    user varchar(128) not null,
    nome varchar(1024) not null,
    email varchar(512) not null,
    senha varchar(64) not null,
    sala varchar(32) not null,
    tipo varchar(64) not null
);

-- Cria a tabela de aula
create table aulas(
    id int auto_increment primary key,
    sala varchar(64) not null,
    dia varchar(64) not null,
    materia varchar(512) not null,
    prof varchar(256) not null,
    horario varchar(32) not null
);

-- User default aluno
insert into users (
    user, nome, senha, email, sala, tipo
) values (
    'aluno', 'teste', 'a21d6f3803f0491c32444ef91a0836be243cc4da5186357e805b7009a5b0669b', 'example@aluno', '1c', 'aluno'
);

/*
    User default aluno
    user: aluno
    nome: teste
    senha: aluno
    email: example@aluno
    sala: 1c
    tip: aluno
*/


-- User default prof
insert into users(
    user, nome, senha, email, sala, tipo
) values (
    'prof', 'teste', '51d1e6a398acbda7e15b687de747e7dfe95fa13154dcb40aa8ab37f1e2b393a0', 'example@prof', 'todas', 'prof'
);

/*
    User default professor
    user: prof
    nome: teste
    senha: prof
    email: example@prof
    sala: todas
    tipo: prof
*/