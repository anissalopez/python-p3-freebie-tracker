from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)






class Company(Base):
    __tablename__ = 'companies'

   

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    freebies= relationship('Freebie', back_populates='company')
    devs = association_proxy('freebies', 'dev',
        creator=lambda de: Freebie(dev=de))
    
    def give_freebie(self, dev, name, cost):
        new_freebie = Freebie(item_name=name, value=cost)
        new_freebie.company = self
        new_freebie.dev = dev
        print(f'Name: {new_freebie.item_name}')
        return new_freebie
    

  


    def __repr__(self):
        return f'{self.name}'


class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies= relationship('Freebie', back_populates='dev')
    companies = association_proxy('freebies', 'company',
        creator=lambda co: Freebie(company=co))
    
    def received_one(self, item):
        for freebie in self.freebies:
            if freebie.item_name == item:
                return True
        return False
    
    def give_away(self, newdev, freebie):
        for freeitems in self.freebies:
            if freeitems.item_name == freebie.item_name:
                print("you successfully gifted this freebie")
                return freebie.dev == newdev
        else:
            return print("you can't give this away")

    def __repr__(self):
        return f'{self.name}'
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
  
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))

    company = relationship('Company', back_populates='freebies')
    dev = relationship('Dev', back_populates='freebies')

    def print_details(self):
        return f'{self.dev.name} owns a {self.item_name} from {self.company}'

    def __repr__(self):
        return f'{self.dev} recieved Freebie: {self.item_name} from Company: {self.company}'