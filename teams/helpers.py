import random
from datetime import timedelta

from django.utils import timezone

from teams.constants import (
    uk_names, uk_surnames, 
    us_names, us_surnames, 
    fr_names, fr_surnames, 
    es_names, es_surnames, 
    mc_names, mc_surnames, 
    it_names, it_surnames, 
    at_names, at_surnames, 
    be_names, be_surnames, 
    de_names, de_surnames, 
    jp_names, jp_surnames
)
from manager.models import Country, Driver, Car, LeadDesigner, RaceMechanic


country_name_surname_lists = {
    'UK': (uk_names, uk_surnames),
    'US': (us_names, us_surnames),
    'FR': (fr_names, fr_surnames),
    'ES': (es_names, es_surnames),
    'MC': (mc_names, mc_surnames),
    'IT': (it_names, it_surnames),
    'AT': (at_names, at_surnames),
    'BE': (be_names, be_surnames),
    'DE': (de_names, de_surnames),
    'JP': (jp_names, jp_surnames),
}


def generate_driver_name(country):
    country_code = country.short_name
    name_list, surname_list = country_name_surname_lists[country_code]
    name = random.choice(name_list)
    surname = random.choice(surname_list)
    return name, surname


def generate_driver_skills(overall):
    num_skills = 5
    skill_weights = [0.01, 0.05, 0.4, 0.6, 0.6, 0.3, 0.2, 0.1, 0.05, 0.01]

    while True:
        try:
            # Generate a list of random integers based on weights
            skills = random.choices(range(1, 11), weights=skill_weights, k=num_skills)

            # Calculate the remaining sum and add it to the highest-value skill
            remaining = overall - sum(skills)
            max_index = skills.index(max(skills))
            skills[max_index] += remaining

            # Check if skill value valid
            if any(skill < 0 for skill in skills) or any(skill > 7 for skill in skills):
                raise ValueError("Invalid skill value!")
            
            # Shuffle the list and assign the skills to named variables
            random.shuffle(skills)
            racecraft, pace, focus, car_management, feedback = skills

            break  # Break out of the loop if skills are generated successfully

        except ValueError:
            continue  # Retry the random generation if a negative skill is encountered

    return racecraft, pace, focus, car_management, feedback


def generate_drivers(team):
    # Generate names and birthdate
    driver1_name, driver1_surname = generate_driver_name(team.location)
    driver2_name, driver2_surname = generate_driver_name(team.location)
    team_country_object = Country.objects.get(id=team.location.id)

    # Generate driver skills
    racecraft, pace, focus, car_management, feedback = generate_driver_skills(25)
    racecraft1, pace1, focus1, car_management1, feedback1 = generate_driver_skills(25)

    driver1 = Driver(
        name=driver1_name, 
        surname=driver1_surname, 
        country=team_country_object,                    
        date_of_birth=driver_random_birth_date(), 
        team=team, 
        skill_overall=25, 
        skill_racecraft=racecraft, 
        skill_pace=pace, 
        skill_focus=focus, 
        skill_car_management=car_management, 
        skill_feedback=feedback
    )
    
    driver2 = Driver(
        name=driver2_name, 
        surname=driver2_surname, 
        country=team_country_object, 
        date_of_birth=driver_random_birth_date(), 
        team=team, 
        skill_overall=25, 
        skill_racecraft=racecraft1, 
        skill_pace=pace1, 
        skill_focus=focus1, 
        skill_car_management=car_management1, 
        skill_feedback=feedback1
    )

    driver1.save()
    driver2.save()
    team.drivers.add(driver1, driver2)


def driver_random_birth_date():
    now = timezone.now()
    delta = timedelta(days=random.randint(1512, 1900))
    driver_birth_date = now - delta
    return driver_birth_date


def staff_random_birth_date():
    now = timezone.now()
    delta = timedelta(days=random.randint(2100, 2900))
    staff_birth_date = now - delta
    return staff_birth_date


def generate_lead_designer(team):
    # Generate lead designers name and birthdate
    lead_designer_name, lead_designer_surname = generate_driver_name(team.location)
    team_country_object = Country.objects.get(id=team.location.id)

    lead_designer = LeadDesigner(
        name=lead_designer_name, 
        surname=lead_designer_surname, 
        country=team_country_object,
        date_of_birth=staff_random_birth_date(), 
        team=team
    )

    lead_designer.save()
    team.lead_designer = lead_designer


def generate_race_mechanics(team):
    # Generate mechanics names and birthdays
    race_mechanic1_name, race_mechanic1_surname = generate_driver_name(team.location)
    race_mechanic2_name, race_mechanic2_surname = generate_driver_name(team.location)
    team_country_object = Country.objects.get(id=team.location.id)

    race_mechanic1 = RaceMechanic(
        name=race_mechanic1_name, 
        surname=race_mechanic1_surname, 
        country=team_country_object,
        date_of_birth=staff_random_birth_date(), 
        team=team
    )

    race_mechanic2 = RaceMechanic(
        name=race_mechanic2_name, 
        surname=race_mechanic2_surname, 
        country=team_country_object,
        date_of_birth=staff_random_birth_date(), 
        team=team
    )
    
    race_mechanic1.save()
    race_mechanic2.save()
    team.race_mechanics.add(race_mechanic1, race_mechanic2)


def generate_car(team):
    car = Car(owner=team)
    car.save()
    team.car = car
    team.save()