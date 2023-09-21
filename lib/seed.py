#!/usr/bin/env python3

# Script goes here!
from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from random import randint

from models import Company, Freebie, Dev

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()


fake=Faker()

def delete_records():
    session.query(Company).delete()
    session.query(Freebie).delete()
    session.query(Dev).delete()
    session.commit()

def create_records():
    random_freebies = ["watch", "ipad", "pen", "hand sanitizer", "charger"]
    companies = [Company(name=f'{fake.company()} {fake.company_suffix()}', founding_year=randint(1900,2023)) for i in range(100)]
    freebies = [Freebie(item_name=random.choice(random_freebies), value=randint(5,50)) for i in range(200)]
    devs = [Dev(name=fake.name()) for i in range(50)]
    session.add_all(companies + freebies + devs)
    session.commit()
    return companies, freebies, devs

def relate_records(companies, freebies, devs):
    for freebie in freebies:
        freebie.dev = random.choice(devs)
        freebie.company = random.choice(companies)

    session.add_all(freebies)
    session.commit()

if __name__ == '__main__':
    delete_records()
    companies, devs, freebies = create_records()
    relate_records(companies, devs, freebies)




