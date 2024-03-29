# Visualisasi Data Sensor di Wireless Sensor Network



### Nama&emsp; &emsp;&emsp;: Dimas Kurniawan - 6181901019
### Pembimbing : Elisati Hulu, S.T., M.T.

Library, Framework, dan Teknologi :
<ul style='list-style-type: "✅ "'>
  <li>Laravel (8.8.2)</li>
  <li>BootStrap </li>
  <li>Plotly (2.32.2)</li>
  <li>Docker</li>
  <li>MySQL & phpMyAdmin</li>
</ul>


## 📌 Konten

  - [Hasil](#hasil)
  - [Arsitektur Sistem](#arsitektur-sistem)
    - [Wireless Sensor Networks]()
    - API
    - Database
    - Website
  - Format Pertukaran Data
  - Peletakan Node Sensor 
  - Perintah yang dibutuhkan
    - Instalasi driver Preon32
    - Setting Serial port  di Linux khususnya Raspberry Pi OS
    - Shell Script dan Batch File
    - Perintah Docker
    - Perintah laravel *developement mode*




## 📌 Hasil
<p align="center">
  <img  src="Images\realtime2.png">
  <p align="center"> Tangkapan Layar Realtime</p>
</p>

<p align="center">
  <img  src="Images\MultipleRealtime.png">
  <p align="center"> Tangkapan Layar Multiple Realtime</p>
</p>



## 📌 Arsitektur Sistem
<img src="Images\Skripsi - Arhitectural desain.png" alt="drawing" style="width:100%;"/>


  
### 🔗 Wireless sensor Networks

*Wireless sensor networks* atau yang selanjutnya disebut WSN. WSN merupakan sekumpulan node sensor yang terhubung dalam satu jaringan komputer nirkabel. Setiap node sensor saling berkomunikasi antara satu dengan lainnya untuk memantau atau mengukur kondisi suatu lingkungan (*sensing*) sesuai dengan jenis sensornya.

Pada proyek (skripsi) ini perangkat yang digunakan pada yaitu Preon32. Pada Preon32 terdapat 4 buah sensor antara lain thermometer, barometer, higrometer, dan akselerometer. Untuk kode dan lebih detail mengenai WSN dapat dilihat pada [berikut ini](https://github.com/dimas519/Skripsi/tree/main/Program/WSN). 
<p align="center">
  <img style="width:200px;" src="Images\preon32.jpg">
  <p align="center"> Perangkat Preon32</p>
</p>

### 🔗 API

API pada sistem ini digunakan untuk menyimpan dan memberikan data pada website. Pada sistem ini WSN tidak langsung melakukan *query* ke basis data agar server dapat dioptimasi. seperti pada contohnya server API dioptimasi untuk komputasi seperti perhitungan statistik yang akan ditampilkan pada website,  sedangkan untuk server basis data dioptimasi untuk sisi pengambilan dan penyimpanan data. Untuk kode dan lebih detail mengenai API dapat dilihat pada [berikut ini](https://github.com/dimas519/Skripsi/tree/main/Program/API).

### 🔗 Basis Data

<p align="center">
  <img style="width:80vw;" src="Images\Skripsi - ERD.png">
  <p align="center"> Diagram <em> Entity Realtionship</em></p>
</p>

### 🔗 Website

Website pada skripsi ini menggunakan Bootstrap dan Laravel. Laravel yang digunakan pada skripsi ini untuk mengatur beberapa hal seperti *template engine*, *cookies* untuk authentikasi, dan lain sebagainya. Untuk kode dan lebih detail mengenai Website dapat dilihat pada [berikut ini](https://github.com/dimas519/Skripsi/tree/main/Program/API).


## ✂️ Format Pertukaran Data




Pada skripsi ini format pertukaran data yang digunakan adalah JSON. Alasan penggunaan JSON dapat dibaca pada dokumen skripsi pada sub-bab 3.3 (silahkan contact jika membutuhkan). Namun ada beberapa bagian yang tidak menggunakan JSON atau menyerupai JSON. Bagian-bagian tersebut antara lain:

  - Komunikasi Node Sensor ke *Base Station*
  
    Untuk bagian ini tidak menggunakan JSON secara utuh karena pada *base station* akan dilakukan pemrosesan lagi di *base station* ataupun hanya berakhir di *base station* saja. Sebagai contoh komunikasi yang tidak menggunakan JSON adalah komunikasi pengiriman data sensing sebagai berikut:
      ```
      server:"time":<waktu milidetik>,
      "id":"<identifier>","key":"<token 10 charcter>",
      "T":<nilai>,"rh":<nilai>,
      "Pa":<nilai>,"a":[<nilai>,<nilai>,<nilai>]
      ```
      dilakukan pemrosesan di *base station* yang dijalankan komputer menjadi:
      ```
      {
        server:"time":<dd-MM-yyyy>,
        "id":"<identifier>","key":"<token 10 charcter>",
        "T":<nilai>,"rh":<nilai>,
         "Pa":<nilai>,"a":[<nilai>,<nilai>,<nilai>]
      }
      ```
      pada hal ini dapat dilihat dilakukan pengubahan waktu dari milidetik menjadi format ```dd-MM-yyyy``` agar dapat disimpan di basis data dan diambil dari basis data dengan mudah. Pengubahan dilakukan oleh komputer yang menjalankan program *base station* agar tidak membebankan node sensor yang ditenagai baterai dan hanya memiliki ram 64KB. Tidak juga dilakukan di server dengan alasan pembagian beban, agar beban komputasi terbagi-bagi ke komputer yang terhubung dengan *base station* (*decentralize*).
      
  

  - Komunikasi Basis Data dengan API
    
    Untuk komunikasi ini tentu saja langsung menggunakan perintah SQL yang memanggil *store procedure*. Contoh ```CALL store_procedure(params)```.


## ✂️ Peletakan Node Sensor 
Pada perangkat keras Preon32 terdapat sensor akselerasi maka perlu diatur peletakan node sensor. Pada Preon32 sensor akselerasi terletak pada gambar berikut yang diberi kotak biru:

<p align="center">
  <img style="width:200px;" src="Images\sensorAkselerasi.jpg">
  <p align="center"> Sensor Akselerasi</p>
</p>

Kemudian jika dilihat dokumentasi pabrik Analog Devices yang membuat sensor ADLX345 didapatkan arah akselasi sebagai berikut:

<p align="center">
  <img  src="Images\sensorAkselerasi.png">
  <p align="center">Arah Sensor Akselerasi oleh <a href="https://www.analog.com/media/en/technical-documentation/data-sheets/adxl345.pdf">Analog Devices hlm.35</a></p>
</p>

Agar sesuai dengan sistem koordinat Cartesius maka Preon32 yang bertindak sebagai node sensor harus diletakan dengan posisi tebalik dari gambar Sensor Akselerasi.


## 📌 Perintah yang dibutuhkan

### ⛏️ Instalasi Preon32

Untuk Sistem operasi Linux lihat pada bagian [berikut ini](#⛏️-setting-serial-port-di-linux) karena bagian ini dikhususkan untuk sistem operasi Windows.


Driver yang tersedia belum di-*sign* sehingga tidak akan bisa langsung diinstall sehingga perlu mengikuti step sebagai berikut

1. Matikan Secure boot. 
   
   Untuk step ini tidak dapat dijelaskan karena setiap manufaktur atau bahkan model memiliki layout menu bios yang berbeda sehinga untuk cara menonaktfikan secure boot pada bios tidak dapat saya jelaskan. Silahkan [google](https://www.google.com) sendiri 😁.

2. Aktifkan test sign pada windows
   
    Pada step ini dapat dilihat pada website [berikut](https://www.howtogeek.com/167723/how-to-disable-driver-signature-verification-on-64-bit-windows-8.1-so-that-you-can-install-unsigned-drivers/) atau mengiktui step berikut:
      1. Buka CMD dengan Run As Administrator
      2. Ketikan ```bcdedit /set testsigning on```
      3. Restart PC /Laptop
      4. Lakukan instalasi Driver
         1. Buka device manager
         2. Buka Ports (COM & LPT)
         3. Klik Kanan pada device Preon32 kemudian pilih properties
         4. Pilih Update Driver
         5. Pilih Browse my computer for driver
         6. Pilih Browse arahkan ke file .inf driver
         7. kemudian next dan finish
      5. Sebenarnya pada step ini seharusnya sudah selesai instalasi sehingga testsign boleh di nonaktifkan lagi dengan ulangi step 1 hingga 3. Namun pada step 2 perintah diganti menjadi ```bcdedit /set testsigning off```.




### ⛏️ Setting Serial port di Linux
Sistem operasi Linux atau  setidaknya Raspberry PI OS yang dicoba penulis tidak membutuhkan driver khusus untuk Preon32 sehingga bisa langsung dijalankan. Hanya saja ada beberapa step khusus yang perlu dijalankan seperti berikut:

1. Mencari tty atau kalau diwindows terkadang di sebut com-port dapat digunakan command sebagai berikut 
   
        dmesg | grep tty

    Output sebagai berikut:

    ![tty Image](Images/tty.png)


2. Setting comport pada file config [context1.properties](https://github.com/dimas519/Skripsi/blob/main/Program/WSN/Jar/Base%20Stasion%20jar/config/context1.properties) 
   
   Sebagai contoh pada poin 1 tertulis output ```... from ttyUSB0``` maka variabel comport ditulis dengan ```tty0```. Jika outputnya ```... from ttyUSB1``` jika demikian maka variabel comport ditulis dengan ```tty1``` begitu pula seterusnya.
  
### ⛏️ Shell Script dan Batch File

Untuk shell dan batch script terdapat pada bagiannya masing-masing agar lebih mudah dibaca. berikut bagian yang ada:

- WSN
  - [WSN yang bertindak sebagai base station](https://github.com/dimas519/Skripsi/tree/main/Program/WSN/Jar/Base%20Stasion%20jar)
  - [WSN yang bertindak sebagai node sensor](https://github.com/dimas519/Skripsi/tree/main/Program/WSN/Jar/Node%20Stasion%20Jar)
- [API](https://github.com/dimas519/Skripsi/tree/main/Program/API)
- [Website](https://github.com/dimas519/Skripsi/tree/main/Program/Website)


### ⛏️ Perintah Docker

Pada skripsi ini docker digunakan dibagian API dan basis data. untuk bagian tersebut dapat dilihat [disini]().


### ⛏️ Perintah laravel *developement mode*

Untuk menjalankan webserver dapat menggunakan perintah berikut ```php artisan serve``` .


