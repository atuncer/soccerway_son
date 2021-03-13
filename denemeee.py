arr = [
    "fikstur_bundesliga",
"fikstur_ligue1",
"fikstur_premier",
"fikstur_seriea",
"fikstur_superlig",
"fikstur_tmp",
"lig_bundesliga",
"lig_laliga",
"lig_ligue1",
"lig_premier",
"lig_seriea",
"lig_superlig"
]

for item in arr:
    print(f'create table {item} as (select * from {item}_backup)')