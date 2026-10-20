import csv

class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand_associato = None

    def __str__(self):
        base = f"{self.codice} - {self.nome} {self.cognome}"
        if self.stand_associato:
            return f"{base} (Stand assegnato: {self.stand_associato.codice})"
        return f"{base} (Nessuno stand assegnato)"

class Stand:
    def __init__(self, codice, mq, padiglione, prezzo_base):
        self.codice = codice
        self.mq = int(mq)
        self.padiglione = int(padiglione)
        self.prezzo_base = float(prezzo_base)
        self.disponibile = True
        self.espositore = None

    def calcola_prezzo_finale(self):
        return self.prezzo_base

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Assegnato a {self.espositore.codice}"
        return f"{self.codice}: Standard | {self.mq} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo_finale():.2f}€ - {stato}"

    def __eq__(self, other):
        if isinstance(other, Stand):
            return self.codice == other.codice
        return False

    def __lt__(self, other):
        if isinstance(other, Stand):
            return self.calcola_prezzo_finale() < other.calcola_prezzo_finale()
        return False

class StandPreseExtra(Stand):
    def __init__(self, codice, mq, padiglione, prezzo_base, prese_extra):
        super().__init__(codice, mq, padiglione, prezzo_base)
        self.prese_extra = int(prese_extra)

    def calcola_prezzo_finale(self):
        sovrapprezzo = self.prezzo_base * (0.07 * self.prese_extra)
        return self.prezzo_base + sovrapprezzo

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Assegnato a {self.espositore.codice}"
        return f"{self.codice}: Prese Extra | {self.mq} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo_finale():.2f}€ - Prese aggiuntive: {self.prese_extra} - {stato}"

class StandPremium(Stand):
    def __init__(self, codice, mq, padiglione, prezzo_base, posizione):
        super().__init__(codice, mq, padiglione, prezzo_base)
        self.posizione = posizione

    def calcola_prezzo_finale(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Assegnato a {self.espositore.codice}"
        return f"{self.codice}: Premium | {self.mq} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo_finale():.2f}€ - Posizione: {self.posizione} - {stato}"


class LingottoFiere:
    def __init__(self, nome):
        self._nome = nome
        self.stand = []
        self.espositori = []

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nuovo_nome):
        self._nome = nuovo_nome

    def carica_file_dati(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lettore = csv.reader(f)
                for riga in lettore:
                    if not riga:
                        continue
                        
                    codice = riga[0].strip()
                    
                    if codice.startswith('ES'):
                        espositore = Espositore(codice, riga[1].strip(), riga[2].strip())
                        self.espositori.append(espositore)
                        
                    elif codice.startswith('ST'):
                        mq = riga[1].strip()
                        padiglione = riga[2].strip()
                        prezzo = riga[3].strip()
                        
                        if len(riga) == 4:
                            nuovo_stand = Stand(codice, mq, padiglione, prezzo)
                        elif len(riga) == 5:
                            extra = riga[4].strip()
                            if extra.isdigit():
                                nuovo_stand = StandPreseExtra(codice, mq, padiglione, prezzo, extra)
                            else:
                                nuovo_stand = StandPremium(codice, mq, padiglione, prezzo, extra)
                                
                        self.stand.append(nuovo_stand)
        except FileNotFoundError:
            raise FileNotFoundError(f"Il file {file_path} non è stato trovato.")

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        stand_trovato = None
        for s in self.stand:
            if s.codice == codice_stand:
                stand_trovato = s
                break
                
        espositore_trovato = None
        for e in self.espositori:
            if e.codice == codice_espositore:
                espositore_trovato = e
                break

        if not stand_trovato:
            raise Exception("Lo stand richiesto non esiste.")
        if not espositore_trovato:
            raise Exception("L'espositore richiesto non esiste.")
        if not stand_trovato.disponibile:
            raise Exception("Lo stand richiesto è già stato assegnato.")
        if espositore_trovato.stand_associato is not None:
            raise Exception("L'espositore ha già uno stand assegnato.")

        stand_trovato.disponibile = False
        stand_trovato.espositore = espositore_trovato
        espositore_trovato.stand_associato = stand_trovato

    def elenca_espositori(self):
        for e in self.espositori:
            print(e)

    def stand_ordinati_per_prezzo(self):
        lista_ordinata = sorted(self.stand)
        return lista_ordinata