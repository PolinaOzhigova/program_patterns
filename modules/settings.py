class Settings:
    __organization_name = ""
    __inn = ""
    __bank_account = ""
    __correspondent_account = ""
    __bik = ""
    __type_property = ""

    @property
    def organization_name(self):
        return self.__organization_name
    
    @organization_name.setter
    def organization_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр!")
        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn
    
    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str) or len(value) != 12:
            raise TypeError("Длина ИНН должна быть 12 символов!")
        self.__inn = value

    @property
    def bank_account(self):
        return self.__bank_account
    
    @bank_account.setter
    def bank_account(self, value: str):
        if not isinstance(value, str) or len(value) != 11:
            raise TypeError("Длина счета должна быть 11 символов!")
        self.__bank_account = value

    @property
    def correspondent_account(self):
        return self.__correspondent_account
    
    @correspondent_account.setter
    def correspondent_account(self, value: str):
        if not isinstance(value, str) or len(value) != 11:
            raise TypeError("Длина корреспондентского счета должна быть 11 символов!")
        self.__correspondent_account = value

    @property
    def bik(self):
        return self.__bik
    
    @bik.setter
    def bik(self, value: str):
        if not isinstance(value, str) or len(value) != 9:
            raise TypeError("Длина БИК должна быть 9 символов!")
        self.__bik = value

    @property
    def type_property(self):
        return self.__type_property
    
    @type_property.setter
    def type_property(self, value: str):
        if not isinstance(value, str) or len(value) != 5:
            raise TypeError("Длина типа собственности должна быть 5 символов!")
        self.__type_property = value
