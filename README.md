# Hungarian-method

## Podatki
- Poln dvodelen graf *G*, kjer je <img src="https://render.githubusercontent.com/render/math?math=$V(G) = X \cup Y$">dvodelna razdelitev, <img src="https://render.githubusercontent.com/render/math?math=$X = \{x_1,\ldots,x_n\}$"> in <img src="https://render.githubusercontent.com/render/math?math=$Y = \{y_1,\ldots,y_m\}$">.
- 
- Matrika cen povezav $C \in \mathbb{R}^{n\times m}$.

## Rezultat
Najcenejše popolno prirejanje v $G$, pri čemer je cena prirejanja $M \subseteq E(G)$ enaka
$$ c(M) = \sum_{x_iy_j \in M}c_{ij}. $$

## Postopek
1. Zarotiramo matriko cen povezav tako, da bo stolpcev vsaj toliko kot vrstic in 
   definiramo $k = \min{(n,m)}$. Pojdi na točko 2.
2. Od elementov vsake vrstice matrike $C$ odštejemo najmanjši element vrstice. Pojdi
   na točko 3.
3. V tej novi matriki najdi ničlo $N$. Označi jo z zvezdico, če v vrstici in stolpcu ničle
   $N$ ni nobene druge ničle z zvezdico. To nadaljuj za vsak element matrike. Pojdi na točko 4.
4. Pokrij vsak stolpec, ki vsebuje ničlo z zvezdico. Če je pokritih $k$ stolpcev, pojdi na 
   zadnjo točko. Drugače pojdi na točko 5.
5. Najdi nepokrito ničlo in jo označi z črtico. Če ni nobene ničle z zvezdico v vrstici te
   ničle s črtico pojdi na točko 6. Drugače, pokrij vrstico z ničlno s črtico in razkrij
   stolpec, ki vsebuje ničlo z zvezdico. Nadaljuj ta postopek, dokler ni več nobene nepokrite
   ničle. Shrani najmanjšo nepokrito vrednost v matriki in pojdi na točko 7.
6. Skonstruiraj zaporedje ničel s črtico in ničel z zvezdico na naslednji način. Naj bo $N_0$ ničla
   ničla s črtico iz točke 5. Z $N_1$ označimo ničlo z zvezdico, ki je v istem stolpcu kot $N_0$ (če obstaja).
   Z $N_2$ označi ničlo s črtico v isti vrstici kot $N_1$. Nadaljuj dokler se zaporedje ne ustavi
   na ničli s črtico, ki nima nobene ničle z zvedico v njenem stolpcu. V tem zaporedju vse ničle s
   črtico spremeni v ničle z zvedico in vse ničle z zvezdico odznači. Vsa pokritja odpokrij in pojdi
   na točko 4.
7. Dodaj vrednost iz točke 5 vsakem elementu pokritih vrstic in odštej vrednost iz točke 5 vsakemu
   elementu nepokritih stolpcev. Pojdi nazaj na točko 5.
8. Najcenejše popolno prirejanje predstavljajo indeski ničel z zvezdico.
