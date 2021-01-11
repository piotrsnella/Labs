from sqlalchemy.orm import sessionmaker
from database_config import create_connection, create_tables, Base, IN_MEMORY_DB_URL, MYSQL_DATABASE_URL, SQLITE_DATABASE_URL, WIN_SQLITE_DATABASE_URL
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from user import User


def crud_operations(session):
    # usuń wszystkch użytkowników z tabeli users - mogli istnieć, ale ich nie potrzebujemy
    session.query(User).delete()

    first_user = User(first_name='Jan', last_name='Kowalski')
    session.add(first_user)
    # w tym miejscu first_user jest oczekujący jeżeli chodzi o stan bazy danych,
    # oznacza to, iż nie jest jeszcze zapisany w bazie
    # obiekt session zapisze first_user tak szybko jak to potrzebne w procesie nazwanym `flush`


    # przed pobraniem użytkownika z bazy, obiekt sesji zapisuje poprzedni rekord
    our_first_user = session.query(User).filter_by(first_name='Jan').first()
    # można używać również funkcji filter, która pozwala chociażby na użycie wyrażeń regularnych
    # więcej informacji https://docs.sqlalchemy.org/en/13/orm/query.html#sqlalchemy.orm.query.Query.filter
    print('Stworzony użytkownik', our_first_user)
    print('typ danych pobranego użytkownika', type(our_first_user))

    # dodanie wielu użytkowników
    users = [
        ('Andrzej', 'Nowak'),
        ('Janina', 'Nowak'),
        ('Anna', 'Kowalska'),
        ('Jan', 'Nowak')
    ]
    session.add_all([User(first_name=f_name, last_name=l_name) for f_name, l_name in users])

    # filtrowanie wyników - pobranie tylko nazwisk użytkowników
    last_names = session.query(User.last_name).all()
    print('wszystkie nazwiska', last_names)

    last_names = session.query(User.last_name).distinct().all()
    print('wszystkie unikatowe nazwiska', last_names)

    # typ zwracanych rezultatów to result
    print('zwrócony typ danych', type(last_names))
    print('iterowanie po rezultatach')
    for last_name in last_names:
        print(type(last_name), '\t', last_name)

    for last_name, in last_names:
        print(type(last_name), '\t', last_name)

    # sortowanie danych
    users_sorted_by_last_first_name = session.query(User).order_by(User.first_name)
    for user in users_sorted_by_last_first_name:
        print(f'{user.id}:\t{user.first_name}')

    # bardziej zaawansowane filtrowanie
    women_in_last_names = session.query(User).filter(User.first_name.like('%a'))
    for user in women_in_last_names:
        print(f'{user.id}:\t{user.first_name}')

    filtered_query = session.query(User).filter(User.first_name.in_(['Andrzej', 'Janina']))
    for user in filtered_query:
        print(f'{user.id}:\t{user.first_name}')

    and_conditions = session.query(User).filter(User.first_name == 'Jan', User.last_name == 'Kowalski')
    for user in and_conditions:
        print(f'{user.id}:\t{user.first_name} {user.last_name}')

    # usuwanie użytkowników
    user_to_be_deleted = session.query(User).filter(User.first_name == 'Jan').first()
    print('przed usunięciem', user_to_be_deleted)
    session.delete(user_to_be_deleted)
    user_to_be_deleted = session.query(User).filter(User.first_name == 'Jan').first()
    print('po usunięciu', user_to_be_deleted)

    print('Aktualizacja użytkowników')
    # chcemy znaleźć pierwszego jana w tabeli i go zaktualizować
    user_to_be_updated = session.query(User).filter(User.first_name=='Jan').first()
    print('przed aktualizacją', user_to_be_updated)
    user_to_be_updated.first_name = 'Janeczek'
    session.add(user_to_be_updated)

    # po aktualizacji nie możemy go znaleźć po imieniu, bo je zmieniliśmy na janeczek
    # więc używamy jego id
    id = user_to_be_updated.id
    user_to_be_updated = session.query(User).filter(User.id == id).first()
    print('po aktualizacji', user_to_be_updated)


def relations(session):
    # relationships
    class Person(Base):
        __tablename__ = 'people'
        id = Column(Integer, primary_key=True)
        first_name = Column(String(30), nullable=False)
        last_name = Column(String(30), nullable=False)
        address_id = Column(Integer, ForeignKey('addresses.id'))
        # połączenie między tabelami
        # najpierw podajemy nazwę klasy z którą ma się łączyć ta relacja
        # następnie nazwę kolumny
        address = relationship('Address', back_populates='people')

        def __repr__(self):
                return f"<Person(first_name={self.first_name}, last_name={self.last_name}, address={self.address})>"

    class Address(Base):
        __tablename__ = 'addresses'
        id = Column(Integer, primary_key=True)
        street = Column(String(30), nullable=False)
        street_number = Column(Integer, nullable=False)
        city = Column(String(30), nullable=False)
        postal_code = Column(String(30), nullable=False)
        # relacja z użytkownikami, pierwszym argumentem jest nazwa klasy,
        # później określamy jak sortować listę osób, które odnoszą się do tego adresu
        # następnie dodajemy nazwę tabeli w argumencie back_populates
        # tak by SQLAlchemy wiedział do której kolumny w Person się odnosi ta relacja
        people = relationship('Person', order_by=Person.id, back_populates='address')

        def __repr__(self):
            return f"<Address(street={self.street} {self.street_number}, city={self.city}, postal_code={self.postal_code})>"

    create_tables(engine, tables=[Person.__table__, Address.__table__])
    # wyczyść tabele people oraz addresses
    session.query(Person).delete()
    session.query(Address).delete()

    some_address = Address(street='Gruszkowa', street_number=12, city='Poznań', postal_code='62-000')
    jan = Person(first_name='Jan', last_name='Kowalski')
    jan.address = some_address
    session.add(jan)

    jan_from_db = session.query(Person).filter(Person.first_name=='Jan').first()
    print(jan_from_db)

    janina = Person(first_name='Janina', last_name='Ostatnia', address=some_address)
    session.add(janina)

    janina_from_db = session.query(Person).filter(Person.first_name=='Janina').first()
    print(janina_from_db)

    addresses_from_db = session.query(Address).all()

    for address in addresses_from_db:
        print('*'*30)
        print('Ludzie mieszkający pod adresem', address)
        for person in address.people:
            print('\t', person)
        print('*'*30)


if __name__=="__main__":
    # tworzy połączenie z bazą
    engine = create_connection(connection_url=WIN_SQLITE_DATABASE_URL, debug_sql=False)

    # tworzy wszystkie table, które zostały wcześniej zdefiniowane jeżeli nie została jeszcze stworzona
    create_tables(engine, tables=[User.__table__])


    # fabryka sesji
    Session = sessionmaker()
    # konfigurujemy ją
    Session.configure(bind=engine)

    # i tworzymy obiekt sesji
    # autocommit oznacza, że nie musimy wywoływać
    session = Session(autocommit=True, autoflush=True)

    crud_operations(session)
    relations(session)