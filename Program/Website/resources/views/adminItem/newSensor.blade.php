<div class="collapse partBox" id="tambahSensor">
    <h3> Tambah WSN</h3>
    <form action="sensorBaru" method="post">  
      <div class="row">
        <div class="col-6">
          <Select class="form-select" id="kotaSelection" name="kota">
            <option value="-1">Pilih Kota</option>
            @foreach ($semuaKota as $kota)
              <option value="{{$kota['id']}}">{{$kota['nama']}}</option>
              @endforeach
          </Select>
        </div>
      </div>
  
      <div class="row ">
        <div class="col-2">
          <label for="nama" class="conf">Nama Lokasi</label>
          <br>
          <label for="latitude" class="conf">Latitude</label>
          <br>
          <label for="longtitude"class="conf">Longtitude</label>
          <br>
          <label for="indoor"class="conf">Indoor</label>
        </div>
  
        <div class="col-5">
          <input type="text" class="form-control conf" placeholder="Nama Lokasi" name="nama">
          <input type="text" class="form-control conf" placeholder="Latitude" name="latitude">
          <input type="text" class="form-control conf" placeholder="Longtitude" name="longtitude">
          <input class="form-check-input indoor" type="checkbox" name="indoor" >
        </div>
      </div>
  
  
      <div class="row "  >

        <div class="col-2">
          <label for="idBS" class="conf">Identifier</label>
          <br>
          <label for="interval"class="conf">Interval</label>
        </div>
  
        <div class="col-5">
          <input type="text" class="form-control conf" placeholder="Identifier" name="idBS">
          <input type="number" class="form-control conf" placeholder="second" name="interval" min=1>
        </div>
      </div>
      <div class="row "  >
        <div class="col-6">
          <label for="indoor">Sensor :</label>
          <input class="form-check-input" type="checkbox" name="suhu" id="suhuCheck" checked>
          <label class="form-check-label" for="suhu">Suhu</label>
  
          <input class="form-check-input" type="checkbox" name="tekanan" id="tekannaCheck" checked>
          <label class="form-check-label" for="tekanan">Tekanan</label>
  
          <input class="form-check-input" type="checkbox" name="kelembapan" id="kelembapanCheck" checked>
          <label class="form-check-label" for="kelembapan">Kelembapan</label>
  
          <input class="form-check-input" type="checkbox" name="akselerasi" id="akselerasiCheck" checked>
          <label class="form-check-label" for="akselerasi">Akselerasi</label>
        </div>
      </div>
  
        <div class="row "  >
          <div class="col-12">
            <button type="submit" class="btn btn-primary mt-2">Kirim</button>
          </div>
        </div>
  
  
    
      </form>
    </div>