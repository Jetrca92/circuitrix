import secrets
import random

from datetime import datetime, timedelta

from manager.models import Country, Driver, Car, LeadDesigner, RaceMechanic



RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def random_password(length, allowed_chars=RANDOM_STRING_CHARS):
    return "".join(secrets.choice(allowed_chars) for i in range(length))


def generate_driver_name():
    gb_names = [
        'William', 'James', 'John', 'Robert', 'Henry', 'Edward', 'Thomas', 'Charles', 'Richard', 'George',
        'Alexander', 'David', 'Andrew', 'Peter', 'Stephen', 'Simon', 'Oliver', 'Adam', 'Christopher', 'Matthew',
        'Benjamin', 'Daniel', 'Anthony', 'Brian', 'Colin', 'Donald', 'Eric', 'Francis', 'Gareth', 'Hugh',
        'Ian', 'Jack', 'Keith', 'Lewis', 'Mark', 'Nigel', 'Owen', 'Patrick', 'Quentin', 'Raymond',
        'Timothy', 'Victor', 'Walter', 'Alan', 'Bernard', 'Cyril', 'Duncan', 'Gavin', 'Harrison', 'Isaac',
        'Jacob', 'Kevin', 'Liam', 'Mason', 'Nathan', 'Oscar', 'Parker', 'Quinn', 'Ryan', 'Samuel',
        'Theodore', 'Vincent', 'Wyatt', 'Abraham', 'Benedict', 'Calvin', 'Dominic', 'Elijah', 'Franklin', 'Gabriel',
        'Hugo', 'Isaiah', 'Jonathan', 'Kenneth', 'Landon', 'Maxwell', 'Nolan', 'Orion', 'Sebastian', 'Tristan',
        'Ulric', 'Wesley', 'Alistair', 'Beckett', 'Caspian', 'Dexter', 'Emmett', 'Finnegan', 'Gideon', 'Hendrik',
        'Ignatius', 'Jasper', 'Kieran', 'Lysander', 'Malachi', 'Nathaniel', 'Orlando', 'Percival', 'Quincy', 'Raphael',
        'Silas', 'Tobias', 'Ulysses', 'Valentine', 'Winston', 'Xanthus', 'Yorick', 'Zacharias', 'Atticus', 'Barnaby',
        'Cedric', 'Desmond', 'Fergus'
    ]


    gb_surnames = [
        'Smith', 'Johnson', 'Brown', 'Taylor', 'Wilson', 'Clark', 'Wright', 'Robinson', 'Walker', 'Wood',
        'Thompson', 'White', 'Watson', 'Turner', 'Edwards', 'Green', 'Hall', 'Lewis', 'Cook', 'Cooper',
        'Carter', 'Lee', 'Morris', 'Phillips', 'King', 'Hill', 'Parker', 'Collins', 'Hayes', 'Hughes',
        'Dixon', 'Grant', 'Rogers', 'Reed', 'Palmer', 'Stevens', 'Butler', 'Knight', 'Lane', 'Freeman',
        'Owen', 'Mason', 'Holland', 'Black', 'Elliott', 'Marshall', 'Berry', 'May', 'Harvey', 'West',
        'Bennett', 'Coleman', 'Cox', 'Fox', 'Graham', 'Harrison', 'Hudson', 'Jordan', 'Murray', 'Nelson',
        'Perry', 'Reynolds', 'Scott', 'Simpson', 'Stewart', 'Ward', 'Webb', 'Wells', 'Willis', 'Young',
        'Adams', 'Bailey', 'Baker', 'Bell', 'Brooks', 'Bryant', 'Burton', 'Clarkson', 'Cunningham', 'Daniels',
        'Douglas', 'Foster', 'Gibson', 'Gordon', 'Hamilton', 'Howard', 'Hunter', 'Jacobs', 'Kennedy', 'Lawrence',
        'Lynch', 'McCarthy', 'Murray', 'Owens', 'Porter', 'Richards', 'Russell', 'Shaw', 'Simmons', 'Spencer',
        'Tucker', 'Wallace', 'Watkins', 'Webster', 'Wheeler', 'Wilkins', 'Woods', 'Wrightson', 'Young'
    ]

    name = random.choice(gb_names)
    surname = random.choice(gb_surnames)
    return name, surname


def generate_driver_skills(overall):
    num_skills = 5
    skill_weights = [0.01, 0.05, 0.4, 0.6, 0.6, 0.3, 0.2, 0.1, 0.05, 0.01]

    while True:
        try:
            # Generate a list of random integers based on the weighted distribution
            skills = random.choices(range(1, 11), weights=skill_weights, k=num_skills)

            # Calculate the remaining sum and add it to the highest-value skill
            remaining = overall - sum(skills)
            max_index = skills.index(max(skills))
            skills[max_index] += remaining

            # Check if any skill is negative
            if any(skill < 0 for skill in skills):
                raise ValueError("Negative skill generated")

            # Shuffle the list and assign the skills to named variables
            random.shuffle(skills)
            racecraft, pace, focus, car_management, feedback = skills

            break  # Break out of the loop if skills are generated successfully

        except ValueError:
            continue  # Retry the random generation if a negative skill is encountered

    return racecraft, pace, focus, car_management, feedback


def generate_drivers(team):
    # Generate names and birthdate
    driver1_name, driver1_surname = generate_driver_name()
    driver2_name, driver2_surname = generate_driver_name()
    team_country_object = Country.objects.get(name=team.location.name)
    now = datetime.now()
    delta1 = timedelta(days=random.randint(1512, 1900))
    driver1_birth_date = now - delta1
    delta2 = timedelta(days=random.randint(1512, 1900))
    driver2_birth_date = now - delta2

    # Generate driver skills
    racecraft, pace, focus, car_management, feedback = generate_driver_skills(25)
    racecraft1, pace1, focus1, car_management1, feedback1 = generate_driver_skills(25)
    driver1 = Driver(name=driver1_name, surname=driver1_surname, country=team_country_object, 
                     date_of_birth=driver1_birth_date, team=team, skill_overall=25, skill_racecraft=racecraft, 
                     skill_pace=pace, skill_focus=focus, skill_car_management=car_management, skill_feedback=feedback)
    driver2 = Driver(name=driver2_name, surname=driver2_surname, country=team_country_object, 
                     date_of_birth=driver2_birth_date, team=team, skill_overall=25, skill_racecraft=racecraft1, 
                     skill_pace=pace1, skill_focus=focus1, skill_car_management=car_management1, skill_feedback=feedback1)
    driver1.save()
    driver2.save()
    team.drivers.add(driver1, driver2)


def generate_staff(team):
    # Generate staff names and birthdate
    lead_designer_name, _lead_designer_surname = generate_driver_name()
    team_country_object = Country.objects.get(name=team.location.name)
    delta3 = timedelta(days=random.randint(2100, 2900))
    now = datetime.now()
    lead_designer_birth_date = now - delta3
    lead_designer = LeadDesigner(name=lead_designer_name, surname=_lead_designer_surname, country=team_country_object,
                                 date_of_birth=lead_designer_birth_date, team=team)
    lead_designer.save()
    team.lead_designer = lead_designer

    race_mechanic1_name, race_mechanic1_surname = generate_driver_name()
    race_mechanic2_name, race_mechanic2_surname = generate_driver_name()
    delta4 = timedelta(days=random.randint(2100,2900))
    delta5 = timedelta(days=random.randint(2100,2900))
    race_mechanic1_birth_date = now - delta4
    race_mechanic2_birth_date = now - delta5
    race_mechanic1 = RaceMechanic(name=race_mechanic1_name, surname=race_mechanic1_surname, country=team_country_object,
                                  date_of_birth=race_mechanic1_birth_date, team=team)
    race_mechanic2 = RaceMechanic(name=race_mechanic2_name, surname=race_mechanic2_surname, country=team_country_object,
                                  date_of_birth=race_mechanic2_birth_date, team=team)
    race_mechanic1.save()
    race_mechanic2.save()
    team.race_mechanics.add(race_mechanic1, race_mechanic2)


def generate_car(team):
    car = Car(owner=team)
    car.save()
    team.car = car