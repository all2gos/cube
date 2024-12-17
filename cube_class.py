#stworzyc obiekt cube, ktory bedzie przyjmowac informacje o scramble'u i bedzie mozna przy jego pomocy poprzez wbudowane w niego metody uzyskiwac rozne informacje o stanie kostki po wymieszaniu
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Cube:
    def __init__(self):
        # Tworzenie ułożonej kostki
        self.colors = ['W', 'G', 'R', 'B', 'O', 'Y']  # Biały, Zielony, Czerwony, Niebieski, Pomarańczowy, Żółty
        self.cube = self.solved_cube()


    def solved_cube(self):
        #"ułozona" kostka, inicjacja głównego, trójwymiarowego obiektu
        #każda ściana 3x3 wypełniona literami: W, G, R, B, O, Y
        colors = ['W', 'G', 'R', 'B', 'O', 'Y']  # Kolejność ścian
        cube = np.array([np.array([f"{color}{i}" for i in range(1, 10)]).reshape(3, 3) for color in colors])
        return cube
    
    def __str__(self):
        return '\n'.join([f"{self.cube[i]}" for i in range(6)])


    def visualize(self, layout='classic'):
        """
        Wizualizuje kostkę w jednym z dwóch układów:
        - 'classic': siatka kostki (góra, boki, dół)
        - 'flat': rozłożona siatka 18x3
        """
        # Mapowanie liter na kolory
        color_map = {
            'W': 'white',
            'G': 'green',
            'R': 'red',
            'B': 'blue',
            'O': 'orange',
            'Y': 'yellow'
        }

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.axis('off')

        if layout == 'classic':
            # Klasyczny układ siatki
            ax.set_xlim(0, 12)
            ax.set_ylim(0, 9)

            # Kolejność rozmieszczenia ścian na siatce
            positions = {
                0: (3, 6),  # Góra (biała)
                4: (0, 3),  # Lewa (zielona)
                1: (3, 3),  # Przód (czerwona)
                2: (6, 3),  # Prawa (niebieska)
                3: (9, 3),  # Tył (pomarańczowa)
                5: (3, 0)   # Dół (żółta)
            }

            # Rysowanie każdej ściany
            for face_idx, (x_offset, y_offset) in positions.items():
                face = self.cube[face_idx]
                for i in range(3):
                    for j in range(3):
                        # Pobierz kolor i tekst z komórki
                        cell_value = face[i, j]
                        color = color_map[cell_value[0]]

                        # Rysowanie naklejki
                        rect = patches.Rectangle(
                            (x_offset + j, y_offset + 2 - i), 
                            1, 1, 
                            facecolor=color,
                            edgecolor='black'
                        )
                        ax.add_patch(rect)

                        # Dodanie tekstu na środku naklejki
                        ax.text(
                            x_offset + j + 0.5,         # Środek naklejki w osi X
                            y_offset + 2 - i + 0.5,     # Środek naklejki w osi Y
                            cell_value,                 # Tekst do wyświetlenia
                            color='black' if color != 'black' else 'white',  # Kontrastujący kolor tekstu
                            ha='center',                # Wyrównanie poziome
                            va='center',                # Wyrównanie pionowe
                            fontsize=10                 # Rozmiar czcionki
                        )


        elif layout == 'flat':
            # Rozłożona siatka 18x3
            ax.set_xlim(0, 18)
            ax.set_ylim(0, 3)

            # Pozycje ścian w rozłożonym układzie
            flat_order = [0, 1, 2, 3, 4, 5]  # Kolejność: W, G, R, B, O, Y
            x_offset = 0

            # Rysowanie rozłożonej siatki
            for face_idx in flat_order:
                face = self.cube[face_idx]
                for i in range(3):
                    for j in range(3):
                        color = color_map[face[i, j][0]]
                        rect = patches.Rectangle(
                            (x_offset + j, 2 - i), 
                            1, 1, 
                            facecolor=color,
                            edgecolor='black'
                        )
                        ax.add_patch(rect)
                x_offset += 3  # Przesunięcie na następną sekcję

        plt.show()


    def rotate(self, front_site):
        #obrot kostki w taki sposob, ze podana sciana jest na froncie

        #ciekawe to jest bardzo ze potrzebne sa dwa typy rotacji i jeden typ ruchu zeby zdefiniowac wszystkie ruchy na kostce, doslownie wszystkie,bo mozna tez z powodzeniem
        #definiowac tak ruchy sciana srodkowa np ale na nasze potrzeby nie jest to konieczne
        temp = self.cube.copy()
        if front_site == 'W':
            self.cube[0] = np.rot90(temp[3],2)
            self.cube[1] = temp[0]
            self.cube[2] = np.rot90(temp[2],1)
            self.cube[3] = np.rot90(temp[5],2 )
            self.cube[4] = np.rot90(temp[4],-1)
            self.cube[5] = temp[1]
        
        elif front_site =='R':
            self.cube[0] = np.rot90(temp[0],-1)
            self.cube[1] = temp[2]
            self.cube[2] = temp[3]
            self.cube[3] = temp[4]
            self.cube[4] = temp[1]
            self.cube[5] = np.rot90(temp[5],1)

    def process_sequence(self, seq):
        seq = seq.split()  # Rozdziela sekwencję na listę ruchów
        print(f"Input sequence: {seq}")
        s = ""

        for m in seq:
            if len(m) == 2 and m[1] == '2':  # Sprawdza, czy ruch to np. "L2"
                s += m[0] * 2  # Dodaje literę dwukrotnie
            elif len(m) == 2 and m[1] == "'":  # Sprawdza, czy ruch to np. "F'"
                s += m[0] * 3  # Dodaje literę trzykrotnie
            else:  # Pojedynczy ruch (np. "L")
                s += m

        print(f"Output sequence: {s}")
        return s
    
    def do(self, seq):
        #program wykonuje podana sekwencje na kostce, ale najpierw trzeba ja obrobic

        for m in seq:
            self.move(m)


    def front_move(self):
        #ruch sciana frontowa zgodnie z ruchem wskazowek zegara
        temp = self.cube.copy()  
        # cube[sciana, wiersz, kolumna]
        self.cube[0][2, :] = temp[4][:, 2][::-1]  
        self.cube[1] = np.rot90(temp[1],-1)  
        self.cube[2][:, 0] = temp[0,2,0], temp[0,2,1],temp[0,2,2]
        self.cube[4][:, 2] = temp[5][0, :]  
        self.cube[5][0, :] = temp[2,2,0],temp[2,1,0],temp[2,0,0]  

    def move(self, move_type):
        #definiowanie procedury wykonania każdego ruchu

        if move_type == 'R':
            self.rotate('R') #obrocenie kostki zeby czerwona sciana byla z przodu
            self.front_move() #wykonanie ruchu
            self.rotate('R') #powrót rotacją kostki
            self.rotate('R') #powrót rotacją kostki
            self.rotate('R') #powrót rotacją kostki
    
        elif move_type == 'B':
            self.rotate('R')
            self.rotate('R')
            self.front_move() #wykonanie ruchu
            self.rotate('R')
            self.rotate('R')

        elif move_type =='L':
            self.rotate('R')
            self.rotate('R')
            self.rotate('R')
            self.front_move() #wykonanie ruchu
            self.rotate('R')

        elif move_type == 'F':
            #ruch podstawowy, na podstawie rotacji i tego ruchu mozna zdefiniowac kazdy inny ruch
            self.front_move() #po prostu wykonanie ruchu

        elif move_type == 'U':
            self.rotate('W') #obrocenie kostki zeby biala sciana byla z przodu
            self.front_move() #wykonanie ruchu
            self.rotate('W') #powrót rotacją kostki
            self.rotate('W') #powrót rotacją kostki
            self.rotate('W') #powrót rotacją kostki


        elif move_type == 'D':
            self.rotate('W') #obrocenie kostki zeby biala sciana byla z przodu
            self.rotate('W') #powrót rotacją kostki
            self.rotate('W') #powrót rotacją kostki
            self.front_move() #wykonanie ruchu
            self.rotate('W') #powrót rotacją kostki


cube = Cube()

#perm U
#cube.do('RFFFRFRFRFFFRRRFFFRR')
#cube.do('RUUURURURUUURRRUUURR')
#cube.do('LBBBLBLBLBBBLLLBBBLL')


#perm T
cube.do(cube.process_sequence("U' B' U2 B2 R2 F2 R U2 R F2 L' F2 L2 U2 B D' F2 L2 F L' U"))
#cube.process_sequence("RURRRUUURRRFRRUUURRRUUURURRRFFF")
#cube.do('UU')
cube.visualize(layout='classic')





