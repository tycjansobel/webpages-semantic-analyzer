## Istotne informacje

#### Model

W projekcie do liczenia embeddingów zastosowałem model encoder-only stella-pl (https://huggingface.co/sdadas/stella-pl). Jest to model typu encoder-only oparty na architekturze qwen2, destylowany z większych modeli.
Model był trenowany na polsko-angielskich zbiorach, więc nadaje się do generowania embeddingów dla stron w języku polskim oraz angielskim.
Model jest w stanie przetworzyć 32768 tokenów (w jednym kontekście), co czyni go idealnym do uchwycenia kontekstu całej strony. Sprawdzałem podstrony Senuto - mają średnio 10k-12k tokenów, więc limit 30k jest w stanie uchwycić kontekst nawet trzykrotnie większych stron bez konieczności stosowania technik semantic chunking.


```
https://huggingface.co/sdadas/stella-pl/blob/main/tokenizer_config.json -> model_max_length 32768
```

#### Porównywanie semantyczne wektorów
Użyłem podobieństwa cosinusowego, które jest symetryczne - oznacza to, że dla inputu wektor A i wektor B zwróci tę samą wartość co dla inputu wektor B i wektor A.
W rezultacie wykluczyłem z wyników porównania te same strony w odwrotnej kolejności.
Sama operacja liczenia podobieństwa cosinusowego nie jest wymagająca obliczeniowo.

#### Zwracanie rzeczowników w podstawowej formie
Użyłem biblioteki spaCy do NLP i pobrałem zasób dla języka polskiego, zwracanie rzeczowników w formie podstawowej działa dla poslko-języcznych stron. Można dopisać oczywiście funkcjonalność wielu języków

#### Co możnaby doiplementować gdyby poświęcić więcej czasu
Projekt był tworzony przeze mnie w jeden wieczór, więc nie jest perfekcyjny. Moim zdaniem warto skupić się na kilku rzeczach, które można by dopracować przy większym nakładzie czasu:

1. Użyć asyncio i aiohttp, żeby pobierać asynchronicznie wszystkie strony jednocześnie zamiast w pętli. Na ten moment proces działał na tyle szybko dla kilku stron ze tego nie implementowałem.

2. Dla kilku linków czasy odpowiedzi u mnie lokalnie to jest 10-12s (drugi strzał, pierwszy trwa dłuzej poniewaz jest razem z pobraniem modelu) nie mam gpu, mój sprzęt to macbook z m3 pro. 
Uwazam ze nie powinno się takich obliczen generować w locie więc warto sie zastanowic na kolejkowaniem tasków i zwracaniem wyników asynchronicznie

3. Zapisywanie wygenerowanych wektorów do bazy aby nie generować w kołko wektorów dla stron dla stron których juz wygenerowaliśmy wektor
Podszedłbym do tego w taki sposób
Dla każdego contentu strony generowana jest suma kontrolna (hash) na podstawie jego zawartości:
    
    1.Hash służy jako unikalny identyfikator dokumentu w bazie danych
    
    2. Wektor embedding jest przechowywany w powiązaniu z tym identyfikatorem
    
    3. Przy kolejnych operacjach na dokumencie:
    
    4. Najpierw obliczany jest hash aktualnej zawartości
    
    5. System sprawdza czy hash już istnieje w bazie
    
    6. Jeśli hash istnieje, wykorzystywany jest zapisany wcześniej wektor
    
    7. Tylko w przypadku nowego hasha generowany jest nowy embedding

Mozna równiez uzyć bazy wektorowej (qdrant, elasticsearch, weaviate) i zrobić indeks na polu wektorowym i przeszukiwać zbiory wektorem w poszukiwaniu najbardziej podobnej semantycznie strony, lub kolekcji za pomoca KNN, w istniejącym zbiorze.

4. Wdrozenie modelu encoder-only na chmurę (sagemaker, vertex ai) lub inne środowisko z gpu, aby efektywnie korzystać z endpointu inferencji i oddzielić kod który nie jest tak wymagący obliczeniowo jak same generowanie embeddingu wtedy mozna by skalować ten kod i kolejkować inferencje

### Przykładowy request

```
POST localhost:3000/api/v1/analyze
{
    "urls": [
        "https://www.senuto.com/pl/blog/jak-humanizowac-teksty-ai-wskazowki-i-narzedzia/",
        "https://www.senuto.com/pl/blog/jezyk-korzysci",
        "https://www.senuto.com/pl/blog/lokalne-seo-pozycjonowanie",
        "https://www.senuto.com/pl/blog/jak-zwiekszyc-widocznosc-strony/"
    ]
}
```

przykładowa odpowiedź

```
{"nouns":{"https://www.senuto.com/pl/blog/jak-humanizowac-teksty-ai-wskazowki-i-narzedzia/":{"tekst":76,"treść":28,"zdanie":14,"narzędzie":13,"inteligencja":13,"humanizacja":12,"informacja":9,"struktura":9,"prompt":8,"strona":8,"długość":8,"dane":7,"temat":7,"treści":6,"jakość":6,"analiza":6,"akapit":6,"styl":6,"przykład":6,"artykuł":6,"sposób":6,"fakt":5,"cel":5,"czytelnik":5,"wyszukiwarka":5,"efekt":5,"podstawa":5,"odbiorca":5,"słowo":5,"doświadczenie":5,"pytanie":5,"czynnik":4,"rytm":4,"tworzyć":4,"detektor":4,"proces":4,"oko":4,"zakres":4,"konstrukcja":4,"list":4,"czas":4,"osoba":4,"autor":4,"użytkownik":4,"wartość":4,"fragment":4,"rower":4,"prompta":4,"przypadek":4,"wynik":4,"rok":4,"content":3,"pozycja":3,"pomoc":3,"chata":3,"zwrot":3,"grupa":3,"perspektywa":3,"model":3,"łańcuch":3,"wiedza":3,"użyć":3,"wersja":3,"źródło":3,"większość":3,"pisać":3,"-":3,"myśl":3,"wskazówki":2,"ton":2,"humanizować":2,"zwięzłość":2,"podsumowanie":2,"ogólnik":2,"rzut":2,"wytyczna":2,"powtarzalność":2,"aspekt":2,"język":2,"marka":2,"spójność":2,"szczyt":2,"odbior":2,"brzmienie":2,"detektór":2,"element":2,"algorytm":2,"wskazówka":2,"praca":2,"wybór":2,"rodzaj":2,"stosować":2,"umieszczać":2,"tabela":2,"kwestia":2,"read":2,"potrzeba":2,"krok":2,"halucynacja":2,"opis":2,"linka":2,"szyk":2,"sekcja":2,"modele":2,"błąd":2,"detekcja":2,"ozdobnik":2,"odpowiedź":2,"wprowadzić":2,"sposob":2,"oczekiwanie":2,"rynek":2,"nawigacja":2,"potencjał":2,"konkurencja":2,"baza":2,"dzień":2,"spis":1,"minuta":1,"poziom":1,"generyczność":1,"fraza":1,"brak":1,"przejście":1,"nadużywanie":1,"świat":1,"sztampowość":1,"tożsamość":1,"emocja":1,"płynność":1,"narracja":1,"copywriter":1,"redaktor":1,"wykorzystać":1,"podejście":1,"wzgląd":1,"media":1,"dostarczać":1,"mowa":1,"obręb":1,"wykrycie":1,"wymaganie":1,"wygenerować":1,"poinformować":1,"zmiana":1,"skłonieć":1,"zapis":1,"newsletter":1,"ułatwiyć":1,"produkt":1,"wypunktować":1,"sformułowanie":1,"sektor":1,"premium":1,"wyrażenie":1,"intelligence":1,"personalizacja":1,"materiał":1,"wariant":1,"obróbka":1,"punkt":1,"wyjście":1,"podawać":1,"przekonanie":1,"technologia":1,"generować":1,"pobierać":1,"system":1,"dokument":1,"👉":1,"rozwiązanie":1,"ramy":1,"czytać":1,"podać":1,"ok":1,"oryginalność":1,"wrażenie":1,"zlepek":1,"typ":1,"anegdota":1,"życie":1,"metafora":1,"porównanie":1,"ukłon":1,"konsekwencja":1,"podpis":1,"powielać":1,"miara":1,"link":1,"tona":1,"dawka":1,"humor":1,"podnieść":1,"wydajność":1,"dostęp":1,"miejsce":1,"wysiłek":1,"schematyczność":1,"synonim":1,"idiomy":1,"kolokwializmy":1,"humanizatory":1,"pogrubienie":1,"sygnatura":1,"powtórzenie":1,"narzędzia":1,"przepływ":1,"przykładem":1,"zastosowanie":1,"praktyka":1,"tendencja":1,"przestrzeń":1,"konkret":1,"zapychacz":1,"przeredaguj":1,"kombo":1,"część":1,"zmienność":1,"formatować":1,"długośc":1,"przyswajać":1,"obraz":1,"cytat":1,"monotonia":1,"linki":1,"definicja":1,"korzyść":1,"wymóg":1,"spełnić":1,"chat":1,"writer":1,"prompto":1,"rezultat":1,"test":1,"kolejność":1,"starcie":1,"writara":1,"możliwość":1,"pojawieć":1,"branża":1,"udział":1,"okolica":1,"wniosek":1,"detektory":1,"wyrocznia":1,"sugestia":1,"waga":1,"wytyczny":1,"znaczenie":1,"wsparcie":1,"generowania":1,"sukces":1,"cecha":1,"standard":1,"badanie":1,"przepisywać":1,"dziedzina":1,"rankingach":1,"uwzględniać":1,"resarch":1,"kreatywność":1,"sprawdzenie":1,"prompty":1,"szlif":1,"powodzenie":1,"post":1,"marketingie":1,"zagadnienie":1,"marketingiem":1,"trial":1,"szkoleniu":1,"termin":1},"https://www.senuto.com/pl/blog/jezyk-korzysci":{"korzyść":48,"język":45,"treść":18,"produkt":18,"klient":17,"tekst":14,"sprzedaż":11,"odbiorca":11,"model":8,"tworzyć":8,"przykład":8,"potrzeba":7,"człowiek":7,"cecha":7,"zaleta":6,"oferta":6,"sposób":6,"copywriting":6,"copywriter":5,"technika":5,"grupa":4,"pisać":4,"usługa":4,"marka":4,"reklama":4,"post":4,"wyobraźnia":4,"dane":4,"komunikacja":3,"marketing":3,"perswazja":3,"techniki":3,"błąd":3,"wykorzystać":3,"opis":3,"zakup":3,"dzień":3,"działanie":3,"media":3,"firma":3,"użyć":3,"read":3,"czas":3,"koniec":3,"raz":3,"osoba":3,"uwaga":3,"zdanie":3,"pytanie":3,"możliwość":3,"fakt":3,"hotel":3,"informacja":3,"klucz":2,"content":2,"aida":2,"minuta":2,"hasło":2,"praca":2,"wymaganie":2,"rynek":2,"e":2,"artykuł":2,"poziom":2,"znajomość":2,"wiedza":2,"praktyka":2,"księgowość":2,"program":2,"przypadek":2,"wyliczenie":2,"odwołać":2,"internet":2,"plaża":2,"tłum":2,"zdjęcie":2,"zainteresowanie":2,"rzeczywistość":2,"spis":1,"dany":1,"ucho":1,"szansa":1,"handlowiec":1,"kupować":1,"specjalista":1,"sprawa":1,"namawian":1,"palec":1,"must":1,"have":1,"zrozumienie":1,"kwestia":1,"definicja":1,"opisywać":1,"zysek":1,"cel":1,"zwiększyć":1,"zaufanie":1,"employer":1,"pobranie":1,"booka":1,"polubienie":1,"fanpage":1,"czytelnik":1,"wynik":1,"landing":1,"page":1,"y":1,"social":1,"odpowiedź":1,"decyzja":1,"konwersja":1,"sformułowanie":1,"przemyślenie":1,"komunikat":1,"facebook":1,"efekt":1,"potencjał":1,"zmniejszać":1,"budżet":1,"koszt":1,"pozyskać":1,"zapis":1,"newsletter":1,"przejście":1,"strona":1,"dodania":1,"koszyk":1,"nauka":1,"poradnik":1,"początkujący":1,"potwór":1,"góra":1,"las":1,"trudność":1,"teoria":1,"emocja":1,"lęk":1,"oczekiwać":1,"szkoła":1,"zajęcia":1,"wartość":1,"element":1,"znaczenie":1,"dystans":1,"konkret":1,"zwrot":1,"głowa":1,"rozwój":1,"biznes":1,"płyn":1,"podział":1,"akapit":1,"wstawiyć":1,"śródtytueł":1,"cytat":1,"materiał":1,"odbiorc":1,"skalować":1,"sklep":1,"case":1,"study":1,"wezwanie":1,"tablica":1,"nazwać":1,"zwrócć":1,"rozwiązanie":1,"potakiwanie":1,"zadanie":1,"biegać":1,"odkurzacz":1,"fan":1,"powiązanie":1,"fana":1,"piekarnik":1,"dostęp":1,"dodatek":1,"podkreślać":1,"konkurencja":1,"miesiąc":1,"prezent":1,"kontekst":1,"zastosowanie":1,"przedstawić":1,"plaż":1,"wstęp":1,"gość":1,"odpoczynek":1,"wyjść":1,"apartament":1,"leżak":1,"widok":1,"ocean":1,"napój":1,"bar":1,"molo":1,"relaks":1,"telefon":1,"aparat":1,"robić":1,"lustrzanka":1,"kliknięec":1,"znajomy":1,"wakacje":1,"powódź":1,"motywacja":1,"badacz":1,"funkcja":1,"równiez":1,"skrót":1,"pożądanie":1,"działać":1,"schemat":1,"przyciągnięć":1,"zwiększeć":1,"wzbudzyć":1,"posiadać":1,"przedmiot":1,"porada":1,"ogólnik":1,"jedno":1,"frazes":1,"kosz":1,"zlecenie":1,"punkt":1,"widzenie":1,"pozór":1,"wzgląd":1,"meta":1,"oszustwo":1,"ortografia":1,"interpunkcja":1,"komentarz":1,"przecinek":1,"ćwiczenie":1,"miejsce":1,"oczekiwanie":1,"kliknięcie":1,"opise":1,"wyliczeni":1,"kłamstwo":1,"wiara":1,"życie":1,"nacisk":1,"treści":1,"myśleć":1,"kolej":1,"modelu":1,"metoda":1,"projektantka":1,"managerka":1,"trial":1,"szkoleniu":1,"termin":1},"https://www.senuto.com/pl/blog/lokalne-seo-pozycjonowanie":{"strona":51,"wynik":40,"firma":34,"słowo":26,"użytkownik":19,"informacja":19,"fraza":18,"obszar":17,"lokalizacja":15,"konkurencja":15,"miasto":15,"wyszukiwarka":14,"usługa":14,"wizytówka":14,"wyszukiwanie":13,"struktura":12,"przypadek":12,"serwis":11,"pozycja":10,"fraz":10,"dane":10,"page":9,"pozycjonowanie":9,"biznes":9,"klient":9,"branża":9,"element":9,"narzędzie":9,"wyszukiwać":8,"pozycjonować":8,"działanie":8,"zapytanie":8,"mapa":8,"nazwa":8,"adres":8,"opinia":8,"algorytm":7,"landing":7,"dzielnica":7,"znaczenie":7,"działalność":7,"optymalizacja":7,"analiza":7,"typ":7,"treść":6,"zależność":6,"znacznik":6,"widoczność":6,"fryzjer":6,"sposób":6,"miejsce":6,"uwaga":6,"czynnik":6,"sygnał":6,"profil":6,"link":6,"sklep":5,"katalog":5,"pack":5,"odnośnik":5,"title":5,"domena":5,"podstrona":5,"placówka":5,"sens":4,"rodzaj":4,"dzień":4,"sieć":4,"kawiarnia":4,"media":4,"zdjęcie":4,"źródło":4,"witryna":4,"możliwość":4,"produkt":4,"oddział":4,"podział":4,"restauracja":4,"kuchnia":4,"podstawa":3,"zmiana":3,"okolica":3,"punkt":3,"godzina":3,"otwarcie":3,"ustalać":3,"portal":3,"wpis":3,"krok":3,"piekarnia":3,"przykład":3,"opis":3,"kampania":3,"teren":3,"post":3,"zakres":3,"doprecyzować":3,"utworzyć":3,"doprecyzowanie":3,"zabieg":3,"parametr":3,"dodać":3,"oznaczenie":3,"content":2,"szukać":2,"pogłębiać":2,"schema":2,"podsumowanie":2,"cel":2,"pomoc":2,"artykuł":2,"region":2,"statystyka":2,"ciąg":2,"ustawienie":2,"rynku":2,"decyzja":2,"numer":2,"raz":2,"site":2,"waga":2,"linka":2,"zamian":2,"linek":2,"ilość":2,"description":2,"nagłówk":2,"sytuacja":2,"problem":2,"liczba":2,"pomysł":2,"ruch":2,"moduł":2,"miara":2,"interakcja":2,"kod":2,"czas":2,"trial":2,"potencjał":2,"kraj":2,"rozbudowa":2,"oparcie":2,"istnieć":2,"oferta":2,"kwestia":2,"poprawa":2,"gabinet":2,"zasada":2,"reguła":2,"atrybut":2,"tekst":2,"pozyskiwać":2,"linkbuilding":2,"skala":2,"sukces":2,"spis":1,"śledź":1,"minuta":1,"szereg":1,"zwiększyć":1,"zakład":1,"gastronomia":1,"beauty":1,"rok":1,"mnie”/":1,"rozwój":1,"trend":1,"przedsiębiorca":1,"grono":1,"słuszność":1,"osoba":1,"przedsiębiorstwo":1,"zadbanie":1,"szansa":1,"moment":1,"rynek":1,"hydraulik":1,"huta":1,"branż":1,"siłownia":1,"hotel":1,"biblioteka":1,"promień":1,"ulica":1,"zintensyfikować":1,"poziom":1,"telefon":1,"ocena":1,"ułatwienie":1,"urządzenie":1,"przycisk":1,"trasa":1,"-":1,"wyniek":1,"ustalić":1,"pytanie":1,"zostawiać":1,"linkowanie":1,"popularność":1,"instytucja":1,"klub":1,"grupa":1,"zainteresowanie":1,"umieszczć":1,"recenzje":1,"jakość":1,"praktyka":1,"odpowiadać":1,"umieszczeć":1,"wzmianka":1,"umieszczenie":1,"address":1,"oko":1,"zachować":1,"zaangażowanie":1,"meldować":1,"pogo":1,"personalizacja":1,"wpływ":1,"kontekst":1,"obsługa":1,"read":1,"definicja":1,"korzyść":1,"robota":1,"zaindeksować":1,"frazy":1,"dentysta":1,"prać":1,"dywan":1,"poszukiwanie":1,"rozpocząć":1,"sprawdzeć":1,"ranking":1,"wgląd":1,"planer":1,"słów":1,"baz":1,"propozycje":1,"baza":1,"podpowiedzie":1,"lista":1,"meta":1,"przejrzeć":1,"stan":1,"konkurent":1,"real":1,"sfera":1,"wpisać":1,"analizy":1,"wykaz":1,"marka":1,"wizytówki":1,"ekspert":1,"kontakt":1,"uwierzytelnienie":1,"wpisanie":1,"poczta":1,"podać":1,"copywriting":1,"strategie":1,"porada":1,"początkujący":1,"kopalnia":1,"wydarzeni":1,"rabat":1,"tydzień":1,"publikacja":1,"zdjęcia":1,"właściciel":1,"sesja":1,"siedziba":1,"wystawić":1,"recenzja":1,"mnogość":1,"ile":1,"placówk":1,"budowa":1,"stworzyć":1,"utworzenie":1,"dziesiątka":1,"setka":1,"konsekwencja":1,"wygenerowania":1,"thin":1,"duplikacja":1,"obręb":1,"całość":1,"rzeczywistość":1,"ośrodek":1,"zastosowanie":1,"infrastruktura":1,"posiadać":1,"sprzedażą":1,"brand":1,"zagłębienie":1,"wzór":1,"indeksować":1,"wolumen":1,"sprzedaż":1,"pierwowzór":1,"dany":1,"uczelnia":1,"kształcenie":1,"tworzyć":1,"sekcja":1,"program":1,"nauczanie":1,"przyciągać":1,"komunikacja":1,"student":1,"uwzględniać":1,"miasta":1,"sektor":1,"aglomeracja":1,"uproszczenie":1,"agregator":1,"autorytet":1,"komfort":1,"przeszukiwać":1,"zasób":1,"wzgląd":1,"rating":1,"wstawienie":1,"położyć":1,"lokal":1,"styl":1,"oznaczyć":1,"zdefiniować":1,"wyszukiwarek":1,"localbusiness":1,"podgrupa":1,"name":1,"postaladdress":1,"geocoordinates":1,"openinghoursspecification":1,"department":1,"dokumentacja":1,"biuro":1,"podróż":1,"agent":1,"pośrednictwo":1,"nieruchomość":1,"doszczegółowienie":1,"metody":1,"implementacja":1,"developer":1,"podejście":1,"pozór":1,"zdobywać":1,"pozyskać":1,"dopasować":1,"portala":1,"charakter":1,"wartość":1,"fakt":1,"użyteczność":1,"skuteczność":1,"powiązanie":1,"odnośniek":1,"teoria":1,"nofollow":1,"wyszukiwarke":1,"społeczność":1,"inicjatywa":1,"parametre":1,"zbieżność":1,"kontrolować":1,"monitoring":1,"część":1,"wybór":1,"monitoringu":1,"zawężenie":1,"pizzeria":1,"oznaczać":1,"aktualizacja":1,"szkoleniu":1,"termin":1},"https://www.senuto.com/pl/blog/jak-zwiekszyc-widocznosc-strony/":{"strona":149,"widoczność":78,"witryna":45,"link":43,"słowo":40,"treść":32,"podstrona":31,"użytkownik":27,"produkt":26,"adres":23,"optymalizacja":22,"element":21,"fraza":20,"opis":20,"miejsce":19,"kategoria":19,"czas":17,"pozycja":17,"wynik":17,"kod":16,"sposób":16,"analiza":15,"struktura":15,"narzędzie":15,"uwaga":15,"aspekt":15,"ładować":14,"domena":14,"tekst":14,"serwis":13,"duplikacja":13,"informacja":12,"fraz":12,"specjalista":12,"przypadek":12,"wyszukiwanie":12,"stan":11,"błąd":11,"robota":11,"nazwa":11,"działanie":11,"możliwość":11,"czynnik":10,"budować":10,"content":9,"meta":9,"dane":9,"usługa":9,"zawartość":9,"szansa":9,"artykuł":9,"przykład":9,"wpis":9,"blog":8,"konkurencja":8,"audyt":8,"oznaczenie":8,"wpływ":8,"problem":8,"poprawa":8,"tworzyć":8,"moc":8,"praca":8,"jakość":8,"linek":8,"publikacja":8,"przekierowanie":7,"szybkość":7,"proces":7,"pomoc":7,"klient":7,"wyszukiwarka":7,"firma":7,"oferta":7,"efekt":7,"wzrost":7,"certyfikat":7,"sklep":7,"robot":7,"urządzenie":6,"linkowanie":6,"intencja":6,"parametr":6,"linkować":6,"nofollow":6,"rozwiązanie":6,"rodzaj":6,"wersja":6,"wykorzystać":6,"wzgląd":6,"sieć":6,"rozmiar":6,"obręb":6,"portal":6,"typ":6,"wiedza":6,"pytanie":5,"ruch":5,"liczba":5,"sytuacja":5,"raz":5,"duplikat":5,"zadanie":5,"obrazek":5,"znak":5,"tytuł":5,"zasada":5,"kanibalizacja":5,"marka":5,"nagłówek":5,"odnośnik":5,"wydawca":5,"metoda":5,"bezpieczeństwo":4,"hierarchia":4,"pozycjonowanie":4,"odpowiedź":4,"lista":4,"zabezpieczenie":4,"doświadczenie":4,"zwiększyć":4,"dzień":4,"potrzeba":4,"walka":4,"konwersja":4,"cel":4,"wskazówka":4,"spadek":4,"wartość":4,"punkt":4,"menu":4,"kwestia":4,"znaczenie":4,"zakup":4,"serwer":4,"postać":4,"rola":4,"strategia":4,"grafika":4,"plik":4,"znacznik":4,"podstrone":4,"ocena":4,"temat":4,"porada":3,"podstawa":3,"zaplecze":3,"grafik":3,"odbiorca":3,"właściciel":3,"dobór":3,"zagrożenie":3,"mobile":3,"koniec":3,"trial":3,"profil":3,"budżet":3,"zagadnienie":3,"moment":3,"osoba":3,"przeglądarka":3,"uzyskać":3,"test":3,"etap":3,"wątpliwość":3,"indeksować":3,"wskaźnik":3,"styl":3,"miara":3,"rozdział":3,"poprawka":3,"wordpress":3,"wtyczka":3,"zastosować":3,"but":3,"anchor":3,"kopia":3,"raport":3,"zmiana":3,"opinia":3,"część":3,"nagłówk":3,"platforma":3,"czołówka":3,"internet":3,"wyszukiwać":3,"sukienka":3,"linka":3,"sprawdzić":2,"nasyć":2,"podsumowanie":2,"identyfikacja":2,"indeksacja":2,"ranking":2,"krok":2,"biznes":2,"otoczenie":2,"rywal":2,"kraj":2,"źródło":2,"kształt":2,"brak":2,"zaplecz":2,"budowa":2,"ingerencja":2,"posiadać":2,"odczytać":2,"programista":2,"https":2,"protokół":2,"zdobywać":2,"przestrzeń":2,"rozplanować":2,"rozpocząć":2,"list":2,"podział":2,"większość":2,"stworzyć":2,"powód":2,"prędkość":2,"rok":2,"arkusz":2,"interakcja":2,"skuteczność":2,"linijka":2,"spacja":2,"skrypt":2,"początek":2,"zalecenie":2,"odczyt":2,"nawigacja":2,"sekcja":2,"zależność":2,"canonical":2,"zwiększać":2,"ulepszenie":2,"ostrzeżenie":2,"dostęp":2,"pewność":2,"mowa":2,"fakt":2,"nasyceć":2,"tematyka":2,"title":2,"tag":2,"przejść":2,"zamieszczeć":2,"wykorzystywać":2,"case":2,"baza":2,"kąt":2,"osłabić":2,"ilość":2,"kolejność":2,"nagłówki":2,"utworzyć":2,"akapit":2,"wyszukiwarke":2,"grafiki":2,"kontekst":2,"nasycić":2,"poszukiwać":2,"grupa":2,"szukać":2,"stosunek":2,"wybór":2,"pozyskać":2,"for":2,"sugestia":2,"dofollow":2,"wybrać":2,"promocja":2,"opłata":2,"fora":2,"relikt":2,"przeszłość":2,"post":2,"wizytówka":2,"autorytet":2,"katalog":2,"pozyskiwać":2,"użyć":2,"linki":2,"branża":2,"klucz":1,"sukces":1,"tutoriale":1,"spis":1,"minuta":1,"podejście":1,"analityka":1,"pozycjonować":1,"analizy":1,"wypadek":1,"treścia":1,"zasięg":1,"sąsiedztwo":1,"przedsiębiorstwo":1,"mieszkaniec":1,"okolica":1,"inspiracja":1,"zweryfikowanie":1,"skorzystanie":1,"dokument":1,"konsultacja":1,"konkret":1,"dostosować":1,"wymóg":1,"zarządzać":1,"wnętrze":1,"skład":1,"trzeci":1,"celownik":1,"niebezpieczeństwo":1,"przestroga":1,"pojawieć":1,"komunikat":1,"karta":1,"próba":1,"wejście":1,"minus":1,"gwarancja":1,"wymoga":1,"wdrożyć":1,"wykonać":1,"screen":1,"poprawność":1,"podpięcie":1,"załadować":1,"weryfikować":1,"kombinacja":1,"wpisywać":1,"pasek":1,"tworzenie":1,"ujednoliceć":1,"zwiększeć":1,"kierunek":1,"rozpisanie":1,"zadać":1,"porażka":1,"potrzeb":1,"odrzucyć":1,"szczęście":1,"sprawa":1,"wygląd":1,"programisty":1,"rozdzielczość":1,"ekran":1,"telefon":1,"tablet":1,"odbior":1,"nota":1,"ostateczność":1,"weryfikacja":1,"sprawdzć":1,"zakładka":1,"obsługa":1,"przeglądać":1,"roboty":1,"chwila":1,"źródłowy":1,"wyświetlenie":1,"blok":1,"tło":1,"kliknięć":1,"przycisk":1,"zareagować":1,"czynność":1,"cumulative":1,"przesunięcie":1,"interaction":1,"metryka":1,"rejestracja":1,"opóźnienie":1,"read":1,"norma":1,"kolej":1,"aktualizacja":1,"algorytm":1,"miesiąc":1,"dopasowania":1,"pamięć":1,"opóźniyć":1,"plan":1,"czcionka":1,"fragment":1,"nadmiar":1,"wydłużyć":1,"pobierać":1,"przetwarzać":1,"linia":1,"cmsów":1,"minifikację":1,"walidator":1,"konstrukcja":1,"ryzyko":1,"wystąpić":1,"przepływ":1,"umiar":1,"stworzeć":1,"bloki":1,"odpowiednik":1,"blóg":1,"tago":1,"odnośnike":1,"canonicala":1,"head":1,"uniknięć":1,"powielać":1,"sortowanie":1,"filtrować":1,"sortować":1,"generować":1,"szczegół":1,"kolor":1,"rozmiaro":1,"uporządkowanie":1,"dostępność":1,"widzenie":1,"wyjaśnieć":1,"deweloper":1,"komfort":1,"użytkować":1,"naprawa":1,"sprawdzać":1,"okazja":1,"wizyta":1,"nasycenie":1,"występowaniu":1,"kondycja":1,"czasy":1,"przekaz":1,"unikalność":1,"włożeć":1,"worek":1,"treście":1,"dopełnieć":1,"przygotować":1,"ważny":1,"związek":1,"przyciągnąć":1,"zachęceć":1,"opisanie":1,"wyświetlać":1,"emocja":1,"kopiować":1,"platform":1,"miano":1,"staż":1,"setka":1,"tysiąc":1,"tysiąca":1,"podołać":1,"przyszłość":1,"szereg":1,"producent":1,"upadek":1,"study":1,"inwestycja":1,"marketing":1,"dbać":1,"spójność":1,"zbudować":1,"zjawisko":1,"wrzucać":1,"procent":1,"margines":1,"stopień":1,"wyeliminować":1,"napisać":1,"zachowanie":1,"treściy":1,"nawiązać":1,"nakreśleć":1,"wniesiyć":1,"powtarzać":1,"znaczniki":1,"rząd":1,"paragraf":1,"dbałość":1,"zrozumienie":1,"odbiór":1,"całość":1,"powtórzeć":1,"siła":1,"odmiana":1,"rozdzielać":1,"sformułowanie":1,"ogół":1,"przesycenie":1,"pozór":1,"zmniejszyć":1,"wgrać":1,"stosować":1,"litera":1,"myślnik":1,"atrybut":1,"grafki":1,"potencjał":1,"pełnia":1,"wczytywać":1,"redukcja":1,"format":1,"porównać":1,"odnalezić":1,"wyniek":1,"wpisaniu":1,"oko":1,"porównanie":1,"system":1,"komputer":1,"laptop":1,"wiązać":1,"talia":1,"ryż":1,"wesele":1,"preferencja":1,"teoria":1,"wymaganie":1,"lupa":1,"parameter":1,"whitepress":1,"przewaga":1,"podawać":1,"estymacje":1,"panel":1,"linkbuilding":1,"przejąć":1,"przeniesieć":1,"stwierdzić":1,"usta":1,"miejscówka":1,"poszukiwanie":1,"kryterium":1,"oznaczyć":1,"reklama":1,"user":1,"komentarz":1,"skanowanie":1,"=":1,"zeskanowanie":1,"przekazać":1,"dylemat":1,"decyzja":1,"wariant":1,"exact":1,"match":1,"forma":1,"połączyć":1,"brand":1,"zamieszczać":1,"artykuły":1,"blogi":1,"influencer":1,"zamówienie":1,"poradnik":1,"recenzja":1,"obszar":1,"foro":1,"społeczność":1,"wypowiedź":1,"angielski":1,"address":1,"katalogi":1,"wyjątka":1,"wskazać":1,"powiązanie":1,"znaleźć":1,"tanie":1,"pakiet":1,"pozyskaniem":1,"wydatkie":1,"udostępnienie":1,"relacja":1,"perspektywa":1,"barter":1,"komentować":1,"publikować":1,"konsekwencja":1,"budowanie":1,"orientacja":1,"wytypować":1,"specjalist":1,"rynek":1,"kampania":1,"udział":1,"agencja":1,"partner":1,"realizacja":1,"przyspieszenie":1,"wprowadzić":1,"znajomość":1,"wsparcie":1,"obserwacja":1,"html":1,"pozycjonowania":1,"instrukcja":1,"dyrektywa":1,"intencje":1,"przyspieszyć":1,"zakres":1,"specjalistka":1,"szkoleniu":1,"termin":1}},"similarities":{"https://www.senuto.com/pl/blog/jak-zwiekszyc-widocznosc-strony/ vs https://www.senuto.com/pl/blog/lokalne-seo-pozycjonowanie":0.72,"https://www.senuto.com/pl/blog/jak-humanizowac-teksty-ai-wskazowki-i-narzedzia/ vs https://www.senuto.com/pl/blog/jak-zwiekszyc-widocznosc-strony/":0.55,"https://www.senuto.com/pl/blog/jak-humanizowac-teksty-ai-wskazowki-i-narzedzia/ vs https://www.senuto.com/pl/blog/jezyk-korzysci":0.54,"https://www.senuto.com/pl/blog/jak-humanizowac-teksty-ai-wskazowki-i-narzedzia/ vs https://www.senuto.com/pl/blog/lokalne-seo-pozycjonowanie":0.49,"https://www.senuto.com/pl/blog/jezyk-korzysci vs https://www.senuto.com/pl/blog/lokalne-seo-pozycjonowanie":0.44,"https://www.senuto.com/pl/blog/jak-zwiekszyc-widocznosc-strony/ vs https://www.senuto.com/pl/blog/jezyk-korzysci":0.43}}
```


Zbudowanie obrazu i uruchomienie

Niestety trzeba poczekać na spacy az zalezność z cpython sie zbuduje więc chwile to trwa
```
docker build -t api:latest .
```

Startowanie

```
docker run -p 3000:3000 api:latest
```