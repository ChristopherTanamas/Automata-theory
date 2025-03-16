'''
Nama Kelompok:
1. Christopher Nathaniel Tanamas // 222200153
2. Gilbert Gregorius Kirana // 222102119
3. Grace Calista Lim // 222102176
4. Jemima Alithia Sigar // 222101393
5. Samuel Revaldo Tjahyadi // 222102304
'''

import re
import csv

class IndonesianWordClassifier:
    def __init__(self):
        self.patterns = {
            'angka_bulat': r'^[-+]?\d+$', # ? = opsional, 1x
            'angka_pecahan': r'^[-+]?([.]\d+|\d+[.]\d*)$',
            'email': r'^[a-zA-Z0-9]+(([!]|[#]|[$]|[%]|[&]|[*]|[+]|[-]|[=]|[?]|[_]|[`]|[{]|[|]|}|[~]|[.])[a-zA-Z0-9]+)*@[a-zA-Z0-9]+([-][a-zA-Z0-9]+)*([.][a-zA-Z0-9]+)+$', 
            'bulan': r'^(januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember)$',
            'hari': r'^(senin|selasa|rabu|kamis|jumat|sabtu|minggu)$',  
            'nama' : r'^(christopher|grace|gilbert|jemima|samuel)$',  
            'ibu_kota': r'^()$', 
            'partikel': r'^()$',
            'benda': r'^()$',
            'sifat': r'^()$',
            'kerja': r'^()$',
            'alphanumeric':  r'^[a-zA-Z]+[a-zA-Z0-9]*$'
        }
        self.verb_re()
        self.noun_re()
        self.adjective_re()
        self.partikel()
        self.ibu_kota()


    def verb_re(self):
        with open('word-verb.txt', 'r') as verbs:   # diambil dari github (https://github.com/kirralabs/Indonesian-Word-Tagged/blob/master/resources/word-verb.txt)
            verb_list = []
            for verb in verbs:
                verb = verb.strip() # ilangin line breaks \n
                if ' ' in verb: # kalau ada spasi, ganti s+
                    verb = verb.replace(' ', r'\s+')
                verb_list.append(verb)

            verb_pattern = r'^(' + '|'.join(verb_list) + r')$' # Gabung jadi 1 pattern
            self.patterns['kerja'] = verb_pattern # Masukkan ke dictionary

    
    def noun_re(self):
        with open('word-noun.txt', 'r') as nouns:   # diambil dari github (https://github.com/kirralabs/Indonesian-Word-Tagged/blob/master/resources/word-noun.txt)
            noun_list = []
            for noun in nouns:
                noun = noun.strip()
                if ' ' in noun: # kalau ada spasi, ganti s+
                    noun = noun.replace(' ', r'\s+')
                noun_list.append(noun)

            noun_pattern = r'^(' + '|'.join(noun_list) + r')$' # Gabung jadi 1 pattern
            self.patterns['benda'] = noun_pattern # Masukkan ke dictionary

    
    def adjective_re(self):
        with open('word-adj.csv', 'r') as csvfile:  # diambil dari kaggle (https://www.kaggle.com/datasets/linkgish/indonesian-adjective-sentiment-kata-sifat?resource=download&select=indonesian-adjective-sentiment-raw.csv)
            csvreader = csv.reader(csvfile)
            next(csvreader)   # Lewati header
            
            # Kata-Kata Sifat berada di kolom kedua
            adj_list = [] 
            for row in csvreader:
                adj = row[1]
                if ' ' in adj: # kalau ada spasi, ganti s+
                    adj = adj.replace(' ', r'\s+')
                adj_list.append(adj)
            
            adj_pattern = r'^(' + '|'.join(adj_list) + r')$' # Gabung jadi 1 pattern
            self.patterns['sifat'] = adj_pattern # Masukkan ke dictionary


    def partikel(self):
        with open('partikel.txt', 'r') as particles:   # diambil dari kbbi (pendataan manual seluruh kategori partikel)
            particle_list = []
            for particle in particles:
                particle = particle.strip()
                if ' ' in particle: # kalau ada spasi, ganti s+
                    particle = particle.replace(' ', r'\s+')
                particle_list.append(particle)

            particle_pattern = r'^(' + '|'.join(particle_list) + r')$' # Gabung jadi 1 pattern
            self.patterns['partikel'] = particle_pattern # Masukkan ke dictionary


    def ibu_kota(self):
        with open('ibu-kota.txt', 'r') as cities:   # penulisan seluruh ibukota provinsi di Indonesia
            capital_city_list = []
            for city in cities:
                city = city.strip()
                if ' ' in city: # kalau ada spasi, ganti s+
                    city = city.replace(' ', r'\s+')
                capital_city_list.append(city)

            capital_city_pattern = r'^(' + '|'.join(capital_city_list) + r')$' # Gabung jadi 1 pattern
            self.patterns['ibu_kota'] = capital_city_pattern # Masukkan ke dictionary


    def classify_word(self, word: str):
        word = word.lower().strip(',!?') # Validasi kalau ada simbol-simbol
        for category, pattern in self.patterns.items(): # Cari kategorinya
            if re.match(pattern, word): # Validasi kata dengan regex
                return category
            
        return 'tidak_dikenal'

    def classify_sentence(self, sentence):
        result = []
        words = sentence.split() # Memisahkan kata dalam kalimat
        counter = 0
        while counter < len(words): # Looping semua kata
            word = words[counter].lower()
            second_word = ''
            if (counter + 1) != len(words):
                second_word = words[counter + 1].lower()
            double_word = word + ' ' + second_word
            double_word = double_word
            # Antisipasi untuk ibukota dengan 2 kata
            if double_word == "banda aceh" or double_word == "tanjung pinang" or double_word == "tanjung selor" or double_word == 'bandar lampung' or double_word == "pangkal pinang":
                word = double_word
                result.append(self.classify_word(word))
                counter += 1
                
            result.append(self.classify_word(word)) # Masukan kata yang udah dilakuin classifier
            counter += 1
        return result

def main():
    classifier = IndonesianWordClassifier()
    
    while True:
        sentence = input("Masukkan kalimat (atau ketik 'exit' untuk mengakhiri): ") # Input
        if sentence.lower() == 'exit': # Keluar Program
            break
        
        classifications = classifier.classify_sentence(sentence)
        print("Klasifikasi:", classifications)

if __name__ == "__main__":
    main()

# Contoh: Samuel pergi ke Yogyakarta tanggal 10 Juni sambil membawa buku yang keren