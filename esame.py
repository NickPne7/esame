
class CSVFile:

    def __init__(self, name):
        
        # Setto il nome del file
        self.name = name
        
        
        # Provo ad aprirlo e leggere una riga
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            self.can_read = False 
            
            
    def get_data(self):
        
        if not self.can_read:
            
            # Se nell'init ho settato can_read a False vuol dire che
            # il file non poteva essere aperto o era illeggibile
            raise ExamException            
            # Esco dalla funzione tornando "niente".
            return None

        else:
            # Inizializzo una lista vuota per salvare tutti i dati
            data = []
    
            # Apro il file
            my_file = open(self.name, 'r')

            # Leggo il file linea per linea
            for line in my_file:
                
                # Faccio lo split di ogni linea sulla virgola
                elements = line.split(',')
                
                # Posso anche pulire il carattere di newline 
                # dall'ultimo elemento con la funzione strip():
                elements[-1] = elements[-1].strip()
                
                # p.s. in realta' strip() toglie anche gli spazi
                # bianchi all'inizio e alla fine di una stringa.
    
                # Se NON sto processando l'intestazione...
                if elements[0] != 'Date':
                    # Aggiungo alla lista gli elementi di questa linea
                    data.append(elements)
            
            # Chiudo il file
            my_file.close()
            
            # Quando ho processato tutte le righe, ritorno i dati
            return data 




class CSVTimeSeriesFile(CSVFile):
    def __init__(self, name):
        # Setto il nome del file
        self.name = name
        
    def get_data(self):
        # Provo ad aprirlo e leggere una riga
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            self.can_read = False 
            
        #controlla se il file è ordinato
        
        dataset = super().get_data()
        lista_date = []
        #abbiamo bisogno solo della parte della data di ogni riga del dataset ottenuto dalla get_data
        for row in dataset:
            lista_date.append(row[0])
        
        #controllo se è ordinata
        if lista_date != sorted(lista_date):
            raise ExamException("Il file non contiene dati ordinati o i dati nella colonna data non sono corretti")
              
        return super().get_data()
       
    

class ExamException(Exception):
    pass

    
#funzione che calcola la media per anno
def mediaAnno(times_series, annoInput):
    annoInput = int(annoInput)
    passeggeri = 0
    numero_mesi_validi = 0        
        
    #itero su time series 
    for row in times_series:
        try:
            #in questo codice consideriamo solo la 
            #parte dell'anno nel primo elemento di row con una split 
            split_row = row[0].split('-')
            year = split_row[0]
            year = int(year)
            
            #se l'anno è uguale all'anno di imput, 
            #conto i mesi una misurazione e 
            #considero la media su quelli
            if year == annoInput:
                
                #se il contenuto del mese è diverso da 0 
                #allora considero il mese valido per il calcolo della media
                if int(row[1]) != 0:
                    numero_mesi_validi = numero_mesi_validi + 1
                
                passeggeri = passeggeri + int(row[1])
        except Exception:
            #se c'è un'eccezione passa all'iterazione successiva
            pass
    #può essere che i mesi validi siano 0,
    #se l'anno è compreso ha passato il test della funzione isinside
    #allora torno media = 0
    try:
        media = passeggeri / numero_mesi_validi
    except:
        media = 0
    return media

#funzione che cerca se gli estremi sono nel dataset
def isInside(dati, first_year, last_year):
    check = True
    listaAnni = []
    for row in dati:
        splitted_row = row[0].split('-')
        anno = splitted_row[0]
        anno = int(anno)
        if anno not in listaAnni:
            listaAnni.append(anno)
         
    if first_year not in listaAnni or last_year not in listaAnni:
        check = False
    
    return check


#funzione che calcola la variazione media dei passeggieri negli anni
def compute_increments(time_series, first_year, last_year):
    
    #-----------------
    #CONTROLLI INPUT
    #-----------------
    #controllo se sono stringhe gli input degli estremi
    if not isinstance(first_year, str) or not isinstance(last_year, str):
        raise ExamException("Gli input non sono delle stringhe")
    
    #converto in intero i due estremi dell'intervallo
    try:    
        first_year = int(first_year)
        last_year = int(last_year)
    except Exception:
        raise ExamException("I valori non sono delle stringhe di numeri")
    
    
    #gestione eccezzione
    if first_year > last_year:
        raise ExamException("il primo estremo è più grande dell'ultimo")
    
    if not isInside(time_series, first_year, last_year):
        raise ExamException("Uno degli intervalli non è contenuto nel data set")
    
    #-----------------
    #FINE CONTROLLO
    #-----------------
    
    #se l'input considera due anni come intervallo
    #valuto se uno dei due intervalli non ha misurazioni
    #in tal caso ritorno una lista vuota
    
    if last_year-first_year == 1:
        if mediaAnno(time_series,last_year) == 0 or mediaAnno(time_series, first_year) == 0:
            return []
    
    #altrimenti->
    #inizializzo la variabile di incremento e il dizionario
    incremento = 0
    dizionario = {}
    
    #setto annoCorrente, variabile che tiene conto dell'anno in cui sono
    #lo faccio partire dal primo elemento della time_series
    annoCorrente = time_series[0][0].split('-')
    annoCorrente = int(annoCorrente[0])
    
    
    #incremento l'anno finchè non raggiungo il primo dell'intervallo
    while annoCorrente != first_year:
        annoCorrente = annoCorrente+1
        
        
    #ciclo principale, formo il dizionario e uso mediaAnno per calcolare
    #la media fra i due anni di riferimento
    #il ciclo continua finchè annoCorrente non raggiunge l'ultimo anno più uno,
    #e se il nostro anno+1 è presente nel file
    while annoCorrente != last_year+1 and isInside(time_series, first_year, annoCorrente+1):
        
        #caso in cui l'anno compreso fra 2 anni abbia media nulla
        #prendo la media del successivo e la tolgo all'attuale
        try:
            if mediaAnno(time_series, annoCorrente+1) == 0:
                incremento = mediaAnno(time_series, annoCorrente+2) - mediaAnno(time_series, annoCorrente)
                dizionario.update({str(annoCorrente) + '-' + str(annoCorrente+2):round(incremento,2)})
                annoCorrente = annoCorrente+2
            #altrimenti proseguo normalmente
            else:
                incremento = mediaAnno(time_series, annoCorrente+1) - mediaAnno(time_series, annoCorrente)
                dizionario.update({str(annoCorrente) + '-' + str(annoCorrente+1):round(incremento,2)})
                annoCorrente = annoCorrente+1
        except:
            raise ExamException("")
            
    return dizionario
            
