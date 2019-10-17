from datetime import date
from PW.pewee_test import Person, Pet

uncle_bob = Person.create(name='Bob', birthday=date(1960, 1, 15))
herb = Person.create(name='Herb', birthday=date(1950, 5, 5))
grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
grandma.name = 'Grandma L.'
grandma.save()

bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

herb_mittens.delete_instance()

herb_fido.owner = uncle_bob
herb_fido.save()
