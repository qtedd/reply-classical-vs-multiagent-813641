from pathlib import Path

#Base Path
BASE_DIR = Path(__file__).resolve().parent
IO_DIR = BASE_DIR / "io"
IO_DIR.mkdir(parents=True, exist_ok=True)

#Datasets
CASES_DATA = IO_DIR / 'ALLARMI.csv'
PASSENGERS_DATA= IO_DIR / 'TIPOLOGIA_VIAGGIATORE.csv'

#Output


#Translation of columns
COLUMN_MAPPING_PASSENGERS = {
    'AREOPORTO_ARRIVO': 'arrival_airport_code',
    'AREOPORTO_PARTENZA': 'departure_airport_code',
    'DATA_PARTENZA': 'departure_date',
    'DESCR_AEREOPORTO_ARR': 'arrival_airport_name',
    'DESCR_AEREOPORTO_PART': 'departure_airport_name',
    'CITTA_ARR': 'arrival_city',
    'CITTA_PARTENZA': 'departure_city',
    'CODICE_PAESE_ARR': 'arrival_country_code',
    'CODICE_PAESE_PART': 'departure_country_code',
    'PAESE_ARR': 'arrival_country',
    'PAESE_PART': 'departure_country',
    'ZONA': 'zone',
    'ENTRATI': 'passengers_entries_count',
    'INVESTIGATI': 'passengers_investigated_count',
    'ALLARMATI': 'passengers_flagged_count',
    'GENERE': 'gender',
    'FLAG_TRANSITO': 'transit_flag',
    'ESITO_CONTROLLO': 'control_result',
    'Tipo Documento': 'document_type',
    'FASCIA ETA': 'age_range',
    '3nazionalita': 'nationality',
    'compagnia%aerea': 'airline',
    'num volo': 'flight_number'
}

GENDER_MAPPING = {
    'F': 'F', 'f': 'F', 'Femmina': 'F', 'Female': 'F', 'FEMALE': 'F', '2': 'F',
    'M': 'M', 'm': 'M', 'Maschio': 'M', 'Male': 'M', 'MALE': 'M', '1': 'M',
    'X': 'Other/NB', 'N/B': 'Other/NB'
}

COLUMN_MAPPING_CASES = {
    'OCCORRENZE': 'event_type',
    'AREOPORTO_ARRIVO': 'arrival_airport',
    'AREOPORTO_PARTENZA': 'departure_airport',
    'DATA_PARTENZA': 'departure_date',
    'DESCR_AEREOPORTO_ARR': 'arrival_airport_name',
    'DESCR_AEREOPORTO_PART': 'departure_airport_name',
    'CITTA_ARR': 'arrival_city',
    'CITTA_PARTENZA': 'departure_city',
    'CODICE PAESE ARR': 'arrival_country_code',
    'CODICE_PAESE_PART': 'departure_country_code',
    'MOTIVO_ALLARME': 'alarm_reason',
    'paese%arr' : 'arrival_country',
    'Paese Partenza': 'departure_country_name',
    'tot voli': 'total_flights',
    '3zona': 'region_zone'
}

COUNTRY_CODES = {
    'GB': 'GBR', 
    'EG': 'EGY', 
    'TR': 'TUR', 
    'AL': 'ALB', 
    'MA': 'MAR', 
    'AE': 'ARE'
}