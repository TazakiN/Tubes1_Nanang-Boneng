# Tugas Besar I Strategi Algoritma (IF2211)
## Kelompok Nanang-Boneng:
* Tazkia Nizami 			(13522032)
* Dhidit Abdhii Aziz 		(13522040)
* Muhammad Naufal Aulia 	(13522074)


## Table of Contents
* [Permainan Diamonds dan Algoritma Greedy](#cyberpunk)
* [Screenshots](#screenshots)
* [Dependencies](#dependencies)
* [How to Use](#how-to-use)


## Permainan Diamonds: Implementasi Algoritma Greedy  <a href="cyberpunk"></a>
> Diamonds merupakan suatu programming challenge yang mempertandingkan bot yang dibuat dengan bot dari para pemain lainnya. Setiap pemain akan memiliki sebuah bot dimana tujuan dari bot ini adalah mengumpulkan diamond sebanyak-banyaknya. Akan terdapat berbagai rintangan yang akan membuat permainan ini menjadi lebih seru dan kompleks. 

Dalam rangka memenangkan pertandingan, dibuatlah pendekatan algoritma greedy dari kelompok kami dengan memanfaatkan objek-objek yang tersedia pada permainan. Algoritma greedy yang diterapkan dalam bot kami adalah _greedy by distance, by red diamond, by defense, by avoid teleport, button_, dan _timing to base_. Dengan begitu, bot akan mengumpulkan diamond terdekat dan berpoin tinggi terlebih dahulu, melindungi dirinya, menghindari teleport, menekan _diamond button_, dan kembali ke base dengan efektif.


## Screenshots <a href="screenshots"></a>
![Example screenshot](.diamonds.gif)

## Dependencies <a href="dependencies"></a>
- Python 3.x
- Node.js
- Docker desktop
- yarn

## How to Use <a href="how-to-use"></a>
0. Siapkan requirement jika belum di-install:
    - Node.js (https://nodejs.org/en) 
    - Docker desktop (https://www.docker.com/products/docker-desktop/) 
    - Yarn

1. Download source code (.zip) pada link berikut:
    ```
    https://github.com/haziqam/tubes1-IF2211-game-engine/releases/tag/v1.1.0
    ```
2. Extract zip tersebut, lalu masuk ke folder hasil extractnya dan buka terminal
3. Masuk ke root directory dari project (sesuaikan dengan nama rilis terbaru)
    ```
    cd tubes1-IF2211-game-engine-1.1.0
    ```
4. Install dependencies menggunakan Yarn
    ```
    yarn
    ```
5. Setup default environment variable dengan menjalankan script berikut
Untuk Windows
    ```
    ./scripts/copy-env.bat
    ```
    Untuk Linux / (possibly) macOS
    ```
    chmod +x ./scripts/copy-env.sh
    ./scripts/copy-env.sh
    ```
6. Setup local database (buka aplikasi docker desktop terlebih dahulu, lalu jalankan command berikut di terminal)
    ```
    docker compose up -d database
    ```
    Lalu jalankan script berikut. Untuk Windows
    ```
    ./scripts/setup-db-prisma.bat
    ```
    Untuk Linux / (possibly) macOS
    ```
    chmod +x ./scripts/setup-db-prisma.sh
    ./scripts/setup-db-prisma.sh
    ```
7. Jika sudah, lakukan build kemudian run untuk menjalankan website
    ```
    npm run build
    ```
    ```
    npm run start
    ```
    Kunjungi frontend melalui `http://localhost:8082/`.
8. Untuk menjalankan bot, clone repository ini dengan
    ```
    git clone https://github.com/TazakiN/Tubes1_Nanang-Boneng.git
    ```
9. Masuk ke src directory dari project 
    ```
    cd Tubes1_Nanang-Boneng/src
    ```
10. Install dependencies menggunakan pip
    ```
    pip install -r requirjements.txt
    ```
11. Run bot di dalam direktori src dengan:
    - hanya 1 bot:
    ```
    python main.py --logic NB --email=nanang135_email@example.com --name=nanangbon --password=nanang135_password --team etimo
    ```
    - lebih dari 1 bot bersamaan (windows):
    ```
    ./run-bots.bat
    ```
    - lebih dari 1 bot bersamaan (linux/macOS):
    ```
    ./run-bots.sh
    ```
    sesuaikan script pada  `run-bots` tersebut

