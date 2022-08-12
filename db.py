import sqlite3
from datetime import datetime

class BaseStatement(object):
    def __init__(self, statement, parameters=()):
        self.statement = statement
        self.parameters = parameters

class BaseModel(object):

    def get_create_statement(self) -> BaseStatement: pass
    def get_insert_statement(self) -> BaseStatement: pass
    def get_select_statement(self) -> BaseStatement: pass

    def create(self):
        s = self.get_create_statement()
        return self.__execute__(s.statement, s.parameters)

    def insert(self):
        s = self.get_insert_statement()
        return self.__execute__(s.statement, s.parameters)
    
    def select(self):
        s = self.get_select_statement()
        return self.__execute__(s.statement, s.parameters)

    def __execute__(self, statement, parameters):
        con = sqlite3.connect('data.db')
        c = con.cursor()
        results = c.execute(statement).fetchall()
        c.close()
        return results

class WiFiModel(BaseModel):

    def __init__(self):
        self.timestamp = None
        self.ssid = None
        self.passphrase = None

    def get_create_statement(self):
        return BaseStatement("CREATE TABLE wifi (timestamp real, ssid text, passphrase text)")

    def get_insert_statement(self):
        return BaseStatement("INSERT INTO wifi VALUES(?, ?, ?)", (datetime.now(), self.ssid, self.passphrase))

    def get_select_statement(self):
        return BaseStatement("SELECT TOP(1) FROM wifi ORDER BY timestamp DESC")

class ScheduleModel(BaseModel):
    
    def __init__(self):
        self.liquid1_time = None
        self.liquid2_time = None
        self.pill1_time = None
        self.pill2_time = None

    def get_create_statement(self):
        return BaseStatement("CREATE TABLE schedule (timestamp real, liquid1_time real, liquid2_time real, pill1_time real, pill2_time real)")

    def get_insert_statement(self):
        return BaseStatement("INSERT INTO schedule VALUES(?, ?, ?, ?, ?)", (datetime.now(), self.liquid1_time, \
            self.liquid2_time, self.pill1_time, self.pill2_time))

    def get_select_statement(self):
        return BaseStatement("SELECT TOP(1) FROM schedule ORDER BY timestamp DESC")

class CompletedMedsModel(BaseModel):
    def __init__(self):
        self.pill1 = None
        self.pill2 = None
        self.liquid1 = None
        self.liquid2 = None

    def get_create_statement(self):
        return BaseStatement("CREATE TABLE completed_meds (date real, pill1 real, pill2 real, liquid1 real, liquid2 real)")

    def get_insert_statement(self):
        return BaseStatement("INSERT INTO completed_meds VALUES(?, ?, ?, ?, ?)", (datetime.today(), \
            self.pill1, self.pill2, self.liquid1, self.liquid2))

    def med_completed(self, medication):
        # get the current dates record, create it
        # if it does not exist
        todays = self.get_todays()
        if todays is None:
            todays = self.create_todays()

        # mark the medication complete and save
        # the record
        if medication == 'pill1':
            self.pill1 = datetime.now()
        if medication == 'pill2':
            self.pill2 = datetime.now()
        if medication == 'liquid1':
            self.liquid1 = datetime.now()
        if medication == 'liquid2':
            self.liquid2 = datetime.now()
