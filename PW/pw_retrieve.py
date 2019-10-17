from PW.pewee_test import Person, Pet

grandma = Person.select().where(Person.name == 'Grandma L.').get()
# grandma = Person.get(Person.name == 'Grandma L.')

for person in Person.select():
    print(person.name)

query = Pet.select().where(Pet.animal_type == 'cat')

for pet in query:
    print(pet.name, pet.owner.name)

query = (Pet
         .select(Pet, Person)
         .join(Person)
         .where(Pet.animal_type == 'cat'))

bob = Person.select().where(Person.name == 'Bob').get()

for pet in Pet.select().where(Pet.owner == bob):
    print(pet.name)

for pet in Pet.select().join(Person).where(Person.name == 'Bob'):
    print(pet.name)

# select Pet, Person from Pet join Person where pet.animal_type == 'cat'