# import math
# from db import DatabaseUti
# from datetime import datetime, date, timedelta

# def compute_age(birthday):
#     # Convert the birthday string to a datetime object
#     birthdate = datetime.strptime(birthday, '%Y-%m-%d').date()

#     # Compute the age based on the current date and the birthdate
#     today = date.today()
#     age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
#     return age

# def organize_bunkhouses(campers):
#     # Calculate the number of campers per bunkhouse
#     num_bunkhouses = 3
#     num_campers = len(campers)
#     campers_per_bunkhouse = int(math.ceil(num_campers / num_bunkhouses))

#     # Sort the campers by age
#     sorted_campers = sorted(campers, key=lambda camper: compute_age(camper[2]))

#     # Divide the campers into bunkhouses
#     bunkhouses = []
#     for i in range(num_bunkhouses):
#         start_index = i * campers_per_bunkhouse
#         end_index = min(start_index + campers_per_bunkhouse, num_campers)
#         bunkhouse_campers = sorted_campers[start_index:end_index]
#         bunkhouse = []
#         for camper in bunkhouse_campers:
#             camper_id = camper[0]
#             bunkhouse.append((camper_id, compute_age(camper[2])))
#         bunkhouses.append(bunkhouse)

#     return bunkhouses


# # Create an instance of the DatabaseUti class
# db = DatabaseUti()

# # Query the camper table for CamperID, Gender, and Birthday
# camper_info = db.query_camper_info()

# # Divide the campers into female and male lists
# female_campers = [(camper[0], camper[1], camper[2]) for camper in camper_info if camper[1] == "Female"]
# male_campers = [(camper[0], camper[1], camper[2]) for camper in camper_info if camper[1] == "Male"]

# # Organize the female and male campers into bunkhouses
# female_bunkhouses = organize_bunkhouses(female_campers)
# male_bunkhouses = organize_bunkhouses(male_campers)

# # Print the results for female bunkhouses
# print("Female bunkhouses:")
# for i, bunkhouse in enumerate(female_bunkhouses):
#     num_campers = len(bunkhouse)
#     avg_age = sum(camper[1] for camper in bunkhouse) / num_campers
#     print(f"Bunkhouse {i+1}: {num_campers} camper(s), average age {avg_age:.1f}")
#     for camper in bunkhouse:
#         print(f"Camper {camper[0]}")

# # Print the results for male bunkhouses
# print("Male bunkhouses:")
# for i, bunkhouse in enumerate(male_bunkhouses):
#     num_campers = len(bunkhouse)
#     avg_age = sum(camper[1] for camper in bunkhouse) / num_campers
#     print(f"Bunkhouse {i+1}: {num_campers} camper(s), average age {avg_age:.1f}")
#     for camper in bunkhouse:
#         print(f"Camper {camper[0]}")


# # db.insert_camper_bunkhouse()

