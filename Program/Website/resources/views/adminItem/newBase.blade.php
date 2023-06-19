<div class="collapse partBox" id="tambahBase">
    <h3> Tambah Base Station</h3>
    <form action="baseBaru" method="post">  
      <div class="row">
        <div class="col-6">
          <Select class="form-select" id="kotaSelection3" name="kota">
            <option value="-1">Pilih Kota</option>
            @foreach ($semuaKota as $kota)
              <option value="{{$kota['id']}}">{{$kota['nama']}}</option>
              @endforeach
          </Select>
        </div>



      </div>
  
      <div class="row ">
        <div class="col-2">
          <label for="nama" class="conf">Nama Base</label>
          <br>
          <label for="latitude" class="conf">Latitude</label>
          <br>
          <label for="longtitude"class="conf">Longtitude</label>
        </div>
  
        <div class="col-5">
          <input required type="text" class="form-control conf" placeholder="Nama Base Station" name="nama">
          <input required type="text" class="form-control conf" placeholder="Latitude" name="latitude">
          <input required type="text" class="form-control conf" placeholder="Longtitude" name="longtitude">
        </div>
      </div>
  

        <div class="row "  >
          <div class="col-12">
            <button type="submit" class="btn btn-primary mt-2">Kirim</button>
          </div>
        </div>
  
  
    
      </form>
    </div>