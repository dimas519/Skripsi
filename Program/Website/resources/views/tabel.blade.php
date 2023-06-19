<script>
  const urlAPI='{{$api}}'

  </script>
<script src="{{asset('js/lokasiFilter.js')}}" defer></script>
<script src="{{asset('js/table.js')}}" defer></script>

<div class="container" id="workSheet">
  <br>
    <div class="row">
      
      <div class="col-6">
        <Select class="form-select" id="kotaSelection">
          <option value="-1">Pilih Kota</option>
          @foreach ($semuaKota as $kota)
          <option value="{{$kota['id']}}">{{$kota['nama']}}</option>
          @endforeach
        </Select>
      </div>
      <div class="col-6">
        <Select class="form-select" id="lokasiSelection"  >
          <option value="-1">Pilih Lokasi</option>
          @foreach ($semuaLokasi as $lokasi)
          <option hidden class="optLokasi" value="{{$lokasi['identifier']}}" city="{{$lokasi['idKota']}}">{{$lokasi['namaLokasi']}}</option>
          @endforeach
        </Select>
      </div>
        <div class="col-1">
        <div class="pt-2" >Start Time </div>
        <div class="pt-3">Interval </div>
      </div>
      <div class="col-3">
        <input type="date" id="startDate" class="mt-2">
        <input type="time" id="startTime" class="mt-2">
        <input type="number" placeholder="second" class="mt-2" id="intervalInput">
      </div>
  
      <div class="col-2">
        <div class="pt-2" >End  Time </div>
      </div>
  
      <div class="col-3">
        <div>
          <input type="date" id="endDate" class="mt-2">
          <input type="time" id="endTime" class="mt-2">
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-4" >
        <button onclick="show()" class="btn btn-primary mt-2">Tampilkan Tabel</button>
      </div>
    </div>


    <div class="row" style="background-color:white; padding:50px 20px; display:none">
      <table id="tabeldump" class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Tanggal</th>
            <th scope="col">Suhu</th>
            <th scope="col">Kelembapan</th>
            <th scope="col">Tekanan</th>
            <th scope="col">Akselerasi (X,Y,Z)*</th>
          </tr>
        </thead>




      </table>
    </div>


    @include("accelerationInfo")