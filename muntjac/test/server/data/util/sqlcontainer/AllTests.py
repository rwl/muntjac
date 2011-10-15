# Copyright (C) 2010 IT Mill Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# from com.vaadin.data.util.sqlcontainer.query.generator.DefaultSQLGenerator import (DefaultSQLGenerator,)
# from org.junit.runner.RunWith import (RunWith,)
# from org.junit.runners.Suite import (Suite,)
# from org.junit.runners.Suite.SuiteClasses import (SuiteClasses,)


class AllTests(object):
    # Set the DB used for testing here!

    class DB(object):
        # 0 = HSQLDB, 1 = MYSQL, 2 = POSTGRESQL, 3 = MSSQL, 4 = ORACLE
        HSQLDB = 'HSQLDB'
        MYSQL = 'MYSQL'
        POSTGRESQL = 'POSTGRESQL'
        MSSQL = 'MSSQL'
        ORACLE = 'ORACLE'
        _values = [HSQLDB, MYSQL, POSTGRESQL, MSSQL, ORACLE]

        @classmethod
        def values(cls):
            return cls._enum_values[:]

    db = DB.HSQLDB
    # Auto-increment column offset (HSQLDB = 0, MYSQL = 1, POSTGRES = 1)
    offset = None
    # Garbage table creation query (=three queries for oracle)
    createGarbage = None
    createGarbageSecond = None
    createGarbageThird = None
    # DB Drivers, urls, usernames and passwords
    dbDriver = None
    dbURL = None
    dbUser = None
    dbPwd = None
    # People -test table creation statement(s)
    peopleFirst = None
    peopleSecond = None
    peopleThird = None
    # Versioned -test table createion statement(s)
    versionStatements = None
    # SQL Generator used during the testing
    sqlGen = None
    # Set DB-specific settings based on selected DB
    sqlGen = DefaultSQLGenerator()
    _0 = db
    _1 = False
    while True:
        if _0 == object.HSQLDB:
            _1 = True
            offset = 0
            createGarbage = 'create table garbage (id integer generated always as identity, type varchar(32), PRIMARY KEY(id))'
            dbDriver = 'org.hsqldb.jdbc.JDBCDriver'
            dbURL = 'jdbc:hsqldb:mem:sqlcontainer'
            dbUser = 'SA'
            dbPwd = ''
            peopleFirst = 'create table people (id integer generated always as identity, name varchar(32), AGE INTEGER)'
            peopleSecond = 'alter table people add primary key (id)'
            versionStatements = ['create table versioned (id integer generated always as identity, text varchar(255), version tinyint default 0)', 'alter table versioned add primary key (id)']
            break
        if (_1 is True) or (_0 == object.MYSQL):
            _1 = True
            offset = 1
            createGarbage = 'create table GARBAGE (ID integer auto_increment, type varchar(32), PRIMARY KEY(ID))'
            dbDriver = 'com.mysql.jdbc.Driver'
            dbURL = 'jdbc:mysql:///sqlcontainer'
            dbUser = 'sqlcontainer'
            dbPwd = 'sqlcontainer'
            peopleFirst = 'create table PEOPLE (ID integer auto_increment not null, NAME varchar(32), AGE INTEGER, primary key(ID))'
            peopleSecond = None
            versionStatements = ['create table VERSIONED (ID integer auto_increment not null, TEXT varchar(255), VERSION tinyint default 0, primary key(ID))', 'CREATE TRIGGER upd_version BEFORE UPDATE ON VERSIONED' + ' FOR EACH ROW SET NEW.VERSION = OLD.VERSION+1']
            break
        if (_1 is True) or (_0 == object.POSTGRESQL):
            _1 = True
            offset = 1
            createGarbage = 'create table GARBAGE (\"ID\" serial PRIMARY KEY, \"TYPE\" varchar(32))'
            dbDriver = 'org.postgresql.Driver'
            dbURL = 'jdbc:postgresql://localhost:5432/test'
            dbUser = 'postgres'
            dbPwd = 'postgres'
            peopleFirst = 'create table PEOPLE (\"ID\" serial primary key, \"NAME\" VARCHAR(32), \"AGE\" INTEGER)'
            peopleSecond = None
            versionStatements = ['create table VERSIONED (\"ID\" serial primary key, \"TEXT\" VARCHAR(255), \"VERSION\" INTEGER DEFAULT 0)', 'CREATE OR REPLACE FUNCTION zz_row_version() RETURNS TRIGGER AS $$' + 'BEGIN' + '   IF TG_OP = \'UPDATE\'' + '       AND NEW.\"VERSION\" = old.\"VERSION\"' + '       AND ROW(NEW.*) IS DISTINCT FROM ROW (old.*)' + '   THEN' + '       NEW.\"VERSION\" := NEW.\"VERSION\" + 1;' + '   END IF;' + '   RETURN NEW;' + 'END;' + '$$ LANGUAGE plpgsql;', 'CREATE TRIGGER \"mytable_modify_dt_tr\" BEFORE UPDATE' + '   ON VERSIONED FOR EACH ROW' + '   EXECUTE PROCEDURE \"public\".\"zz_row_version\"();']
            break
        if (_1 is True) or (_0 == object.MSSQL):
            _1 = True
            offset = 1
            createGarbage = 'create table GARBAGE (\"ID\" int identity(1,1) primary key, \"TYPE\" varchar(32))'
            dbDriver = 'com.microsoft.sqlserver.jdbc.SQLServerDriver'
            dbURL = 'jdbc:sqlserver://localhost:1433;databaseName=tempdb;'
            dbUser = 'sa'
            dbPwd = 'sa'
            peopleFirst = 'create table PEOPLE (\"ID\" int identity(1,1) primary key, \"NAME\" VARCHAR(32), \"AGE\" INTEGER)'
            peopleSecond = None
            versionStatements = ['create table VERSIONED (\"ID\" int identity(1,1) primary key, \"TEXT\" VARCHAR(255), \"VERSION\" rowversion not null)']
            sqlGen = MSSQLGenerator()
            break
        if (_1 is True) or (_0 == object.ORACLE):
            _1 = True
            offset = 1
            createGarbage = 'create table GARBAGE (\"ID\" integer primary key, \"TYPE\" varchar2(32))'
            createGarbageSecond = 'create sequence garbage_seq start with 1 increment by 1 nomaxvalue'
            createGarbageThird = 'create trigger garbage_trigger before insert on GARBAGE for each row begin select garbage_seq.nextval into :new.ID from dual; end;'
            dbDriver = 'oracle.jdbc.OracleDriver'
            dbURL = 'jdbc:oracle:thin:test/test@localhost:1521:XE'
            dbUser = 'test'
            dbPwd = 'test'
            peopleFirst = 'create table PEOPLE (\"ID\" integer primary key, \"NAME\" VARCHAR2(32), \"AGE\" INTEGER)'
            peopleSecond = 'create sequence people_seq start with 1 increment by 1 nomaxvalue'
            peopleThird = 'create trigger people_trigger before insert on PEOPLE for each row begin select people_seq.nextval into :new.ID from dual; end;'
            versionStatements = ['create table VERSIONED (\"ID\" integer primary key, \"TEXT\" VARCHAR(255), \"VERSION\" INTEGER DEFAULT 0)', 'create sequence versioned_seq start with 1 increment by 1 nomaxvalue', 'create trigger versioned_trigger before insert on VERSIONED for each row begin select versioned_seq.nextval into :new.ID from dual; end;', 'create sequence versioned_version start with 1 increment by 1 nomaxvalue', 'create trigger versioned_version_trigger before insert or update on VERSIONED for each row begin select versioned_version.nextval into :new.VERSION from dual; end;']
            sqlGen = OracleGenerator()
            break
        break
