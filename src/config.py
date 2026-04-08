from pathlib import Path

#Base Path
BASE_DIR = Path(__file__).resolve().parent
IO_DIR = BASE_DIR / "io"
IO_DIR.mkdir(parents=True, exist_ok=True)

PREPROCESS_DIR = IO_DIR / 'preprocessing'
PREPROCESS_DIR.mkdir(parents=True, exist_ok=True)

FEAT_ENGEERING_DIR = IO_DIR / 'feat_engineering'
FEAT_ENGEERING_DIR.mkdir(parents=True, exist_ok=True)

#Datasets
CASES_DATA = IO_DIR / 'ALLARMI.csv'
PASSENGERS_DATA = IO_DIR / 'TIPOLOGIA_VIAGGIATORE.csv'

#Output
CASES_CLEAN_OUT = PREPROCESS_DIR / 'cases_clean.csv'
PASSENGERS_CLEAN_OUT = PREPROCESS_DIR / 'passenger_clean.csv'
FEAT_ENGEERING_OUT = FEAT_ENGEERING_DIR / 'feat_engineered.csv'

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

COLUMN_MAPPING_CASES = {
    'OCCORRENZE': 'event_type',
    'AREOPORTO_ARRIVO': 'arrival_airport_code',
    'AREOPORTO_PARTENZA': 'departure_airport_code',
    'DATA_PARTENZA': 'departure_date',
    'DESCR_AEREOPORTO_ARR': 'arrival_airport_name',
    'DESCR_AEREOPORTO_PART': 'departure_airport_name',
    'CITTA_ARR': 'arrival_city_name',
    'CITTA_PARTENZA': 'departure_city_name',
    'CODICE PAESE ARR': 'arrival_country_code',
    'CODICE_PAESE_PART': 'departure_country_code',
    'MOTIVO_ALLARME': 'alarm_reason',
    'paese%arr' : 'arrival_country_name',
    'Paese Partenza': 'departure_country_name',
    'tot voli': 'total_flights',
    '3zona': 'region_zone'
}

#Standardization of gender values
GENDER_MAPPING = {
    'F': 'F', 'f': 'F', 'Femmina': 'F', 'Female': 'F', 'FEMALE': 'F', '2': 'F',
    'M': 'M', 'm': 'M', 'Maschio': 'M', 'Male': 'M', 'MALE': 'M', '1': 'M',
    'X': 'Other/NB', 'N/B': 'Other/NB'
}

#3 Alpha Iso codes of countries for cases dataset.
COUNTRY_CODES = {
    'GB': 'GBR', 
    'EG': 'EGY', 
    'TR': 'TUR', 
    'AL': 'ALB', 
    'MA': 'MAR', 
    'AE': 'ARE'
}

#Feature Engineering Columns
ID_COLS = ["date", "route_city", "route_country", "route_airport"]
CALENDAR_COLS = ["year", "month", "day", "weekday", "is_weekend"]
BASE_COLS = ["entries", "investigated", "flagged","investigation_rate", "flag_rate", "flag_given_investigated"]

SEGMENT_COLS = ["nationality_count", "avg_nat_entries", "max_nat_entries", "avg_nat_flag_rate", "max_nat_flag_rate",
    "document_type_count", "avg_doc_entries", "max_doc_entries", "avg_doc_flag_rate", "max_doc_flag_rate",
    "airline_count", "avg_airline_entries", "max_airline_entries", "avg_airline_flag_rate", "max_airline_flag_rate",
    "control_result_count", "avg_control_entries", "max_control_entries", "avg_control_flag_rate", "max_control_flag_rate"]

CASE_COLS = [
    "has_case_match", "case_records", "total_flights",
    "unique_alarm_reasons", "unique_event_types","alarm_density_per_entry"]

CHANGE_COLS = ['entries_lag1','entries_diff1','entries_pct_change1',
    'investigated_lag1','investigated_diff1','investigated_pct_change1',
    'flagged_lag1','flagged_diff1','investigation_rate_lag1',
    'investigation_rate_diff1','investigation_rate_pct_change1','flag_rate_lag1','flag_rate_diff1']

VOLUME_FLAG_COLS = ["is_low_volume", "is_low_volume_50"]

ROLLING_COLS = ["entries_roll7", "entries_roll30", "entries_dev_ratio7", "flag_rate_roll7",
     "flag_rate_roll30", "flag_rate_dev_ratio7", "investigation_rate_roll7", "investigation_rate_roll30",
     "investigation_rate_dev_ratio7"]

SEASONAL_COLS = ["entries_trend", "entries_residual", "entries_residual_z"]