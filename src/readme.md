### Passenger Dataset: TIPOLOGIA_VIAGGIATORE

NAZIONALITA, TIPO_DOCUMENTO, FASCIA_ETA, COMPAGNIA_AEREA and NUMERO_VOLO contain inconsistent data.<br>
note_operatore and codice_rischio are almost empty. <br>
GENERE, ENTRATI, INVESTIGATI, DATA_PARTENZA, ANNO_PARTENZA, MESE_PARTENZA and CODICE_PAESE_ARR are not in correct formats.<br>
'DATA_PARTENZA' contains unstandard rows. (ex: instead of having dd/mm/yyyy format all in numbers, January was recorded as GEN) <br>
In 'CODICE_PAESE_ARR' Italy was represented by both ITA and IT. All country entries were converted into standard 3 alpha codes.<br>
N.D.'s from 'Tipo Documento' and 'FASCIA ETA' were replaced with null.<br>
There are 61 rows that are exact duplicates of other rows. Duplicate rows were removed since it will create bias afterwards in our model.<br>
There are some logical issues with the given data as well. 259 rows have more 'INVESTIGATI' than 'ENTRATI' and 218 rows have more 'ALLARMATI' than 'INVESTIGATI'. In order to fix this issue we drop them. There are 3 rows that have an extremely large amount of 'ENTRATI' while the largest commercial aircraft can take maximum of 853 passengers. These columns were exluded. The columns type was set as integer.'<br>
In 'AREOPORTO_ARRIVO' and 'AREOPORTO_PARTENZA', some of codes were lower cased which was causing duplication. All uppercased.<br>


### Cases Dataest: Allarmi
'TOT', 'PAESE_PART', *'CODICE_PAESE_ARR', 'ZONA' and 'PAESE_ARR' includes noisy and inconsistent data (Negative values). It is a duplicate of 'tot voli' so it is dropped. The values in 'tot voli' were standardized.<br>
*CODICE PAESE ARR' (inconsistent) and 'paese%arr' (redundant) can't be considered since all of the arrival airports are in Italy.<br>
'note_operatore' and 'flag_rischio' are dropped since they are almost empty.<br>
'ANNO_PARTENZA' and 'MESE_PARTENZA' are also dropped because of redunduncy.<br>
'tot voli' values is standardized. (was including integers and characters)<br>
'DATA_PARTENZA' follows the same pattern as Passenger dataset.<br>
The dataset contains 50 duplicated rows. All are dropped.<br>
'OCCORRENZE' contains placeholders like ???, N/C, and Altro. They are replaced with UNKNOWN.<br>
Conditional Filling was used for 'DESCR_AEROPORTO_PART'. If the description is missing or inconsistent, it ise filled it with the Airport Code.<br>
'CITTA_PARTENZA' includes missing rows. Missing rows were replaced with their country.<br>
'CODICE_PAESE_PART' includes unstandard and inconsistent rows. All rows are uppercased and missing values are saved as 'UNKNOWN' and later on will be filled by looking at 'PAESE PARTENZA'<br>
All columns are translated to English<br>
'region_zone' has some logical issues (a country can't be in multiple zones like Regno Unito). Zones were redefined by the most frequent values.<br>

