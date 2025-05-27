
# Optimizacija dostavnih ruta pomoću Tabu Search algoritma

## Opis projekta

Ovaj projekt simulira i rješava problem optimizacije dostavnih ruta u urbanim područjima pomoću **Tabu Search algoritma**, jedne od najpoznatijih metaheurističkih metoda za kombinatornu optimizaciju.

Zamislimo dostavnu službu koja svaki dan mora obići veći broj adresa unutar grada — s izazovima poput prometnih gužvi, pogrešnih skretanja i vremenskih ograničenja. Ključni cilj takvog sustava je pronaći **najkraću moguću rutu** koja pokriva sve točke, uzimajući u obzir stvarne uvjete poput **rush-hour** intervala, gdje dolazi do zastoja i kašnjenja. Upravo to simuliramo i optimiziramo ovim programom.

### Glavne funkcionalnosti

1. **Generiranje lokacija**  
   Program prvo nasumično generira određeni broj točaka (lokacija) na koordinatnoj mreži, koje predstavljaju destinacije za dostavu. Svaka točka ima X i Y koordinatu, a sve se spremaju u `coordinates.csv`.

2. **Računanje udaljenosti**  
   Između svake dvije lokacije računa se euklidska udaljenost pomoću matematičke formule. Te udaljenosti se koriste kao osnova za izračun troška rute.

3. **Simulacija gužvi – penalizacija**  
   Kako bismo simulirali uvjete stvarnog prometa, između pojedinih lokacija se nasumično dodaju penalizacije koje predstavljaju kašnjenja u prometu tijekom gužvi (rush-hour). Te vrijednosti se spremaju u `penalty_matrix.csv`.

4. **Izračun troška rute**  
   Svaka ruta ima svoj ukupni trošak, koji se sastoji od zbroja udaljenosti između točaka i dodanih penala. Ruta se zatvara tako da se zadnja točka vraća na početnu lokaciju.

5. **Optimizacija pomoću Tabu Search algoritma**  
   Algoritam traži optimalan redoslijed obilaska točaka izbjegavajući lokalne minimume pomoću tabu liste — memorije prethodnih loših rješenja. Na taj način sustav pronalazi efikasniju rutu s manjim ukupnim vremenom.

6. **Vizualizacija**  
   Na kraju, optimalna ruta se prikazuje na grafu: 
   - Crvena točka označava početak,
   - Zelena točka označava kraj rute,
   - Uz svaku lokaciju ispisano je i vrijeme dolaska do nje (uključujući penalizaciju).

## Zaključak

Korištenjem Tabu Search algoritma pokazali smo kako heuristički pristup može značajno poboljšati rješenja problema optimizacije ruta, čak i u uvjetima s penalima i prometnim gužvama.

