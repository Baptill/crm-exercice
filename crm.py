import re
import string
from tinydb import TinyDB
from pathlib import Path

class User:
    DB = TinyDB(Path(__file__).resolve().parent / 'db.json', indent=4)

    def __init__(self, first_name:str, last_name: str, phone_number: int = "", address: str = ""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    def __repr__(self) -> str:
        return f"User({self.first_name}, {self.last_name})"

    def __str__(self):
        return(f"{self.full_name}\n{self.phone_number}\n{self.address}")

    def _checks(self):
        self._check_names

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def _check_phone_number(self):
        phone_digits = re.sub(r"[+()\s]*", "", self.phone_number)
        if len(phone_digits) > 10 or not phone_digits.isdigit():
            raise ValueError(f"Numéro de téléphone {self.phone_number} invalide")

    def _check_names(self):
        if not (self.first_name and self.last_name):
            raise ValueError("Le prénom et le nom de famille ne peuvent pas être vides.")

        special_characters = string.punctuation + string.digits

        for character in self.first_name + self.last_name:
            if character in special_characters:
                raise ValueError(f"Pas de charactère special dans le prenom {self.full_name}")

    def save(self, validate_data=False):
        if validate_data:
            self._checks()
        return User.DB.insert(self.__dict__)

def get_all_user():
    for user in User.DB.all():
        User(**user)

if __name__ == "__main__":
    from faker import Faker
    fake = Faker(locale="fr_FR")

    for _ in range(10):
        user = User(first_name = fake.first_name(),
                    last_name = fake.last_name(),
                    phone_number = fake.phone_number(),
                    address  =  fake.address())
        user._checks()
        user.save()
