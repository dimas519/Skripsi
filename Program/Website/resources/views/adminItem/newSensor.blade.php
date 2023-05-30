<div>
    <form action="sensorBaru" method="post">  
      <div class="row">
        <div class="col-6">
          <Select class="form-select" id="kotaSelection">
            <option value="-1">Pilih Kota</option>
            @foreach ($semuaKota as $kota)
              <option value="{{$kota['id']}}">{{$kota['nama']}}</option>
              @endforeach
          </Select>
        </div>
      </div>
  
      <div class="row ">
        <div class="col-1">
          <label for="nama">Nama Lokasi</label>
          <label for="latitude">Latitude</label>
          <label for="longtitude">Longtitude</label>
          <label for="indoor">Indoor</label>
        </div>
  
        <div class="col-5">
          <input type="text" class="form-control" placeholder="Nama Lokasi" name="nama">
          <input type="text" class="form-control" placeholder="Latitude" name="latitude">
          <input type="text" class="form-control" placeholder="Longtitude" name="longtitude">
          <input class="form-check-input" type="checkbox" name="indoor">
        </div>
      </div>
  
  
      <div class="row "  >
        <div class="col-6">
          <label for="indoor">Sensor :</label>
          <input class="form-check-input" type="checkbox" value="suhu" name="suhu" id="suhuCheck">
          <label class="form-check-label" for="suhu">Suhu</label>
  
          <input class="form-check-input" type="checkbox" value="tekanan" name="tekanan" id="tekannaCheck">
          <label class="form-check-label" for="tekanan">Tekanan</label>
  
          <input class="form-check-input" type="checkbox" value="kelembapan" name="kelembapan" id="kelembapanCheck">
          <label class="form-check-label" for="kelembapan">Kelembapan</label>
  
          <input class="form-check-input" type="checkbox" value="akselerasi" name="akselerasi" id="akselerasiCheck">
          <label class="form-check-label" for="akselerasi">Akselerasi</label>
        </div>
  
        <div class="row "  >
          <div class="col-12">
            <button type="submit" class="btn btn-primary mt-2">Kirim</button>
          </div>
        </div>
  
  
    
      </form>
    </div>