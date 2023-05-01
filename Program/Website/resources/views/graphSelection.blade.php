<link rel="stylesheet" href="{{'css/location.css'}}">

<script src="{{asset('js/lokasiForm.js')}}" defer></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<div class="container">
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
        <option hidden class="optLokasi" value="{{$lokasi['id']}}" city="{{$lokasi['idKota']}}">{{$lokasi['nama']}}</option>
        @endforeach
      </Select>
    </div>
  </div>
    
  <div class="row">
    <div class="col-1">
      <div class="pt-2" >Start Time </div>
      <div class="pt-2" >End  Time </div>
      <div class="pt-3">Interval </div>
    </div>
    <div class="col-3">
      <input type="date" id="startDate" class="mt-2">
      <input type="time" id="startTime" class="mt-2">
      <input type="date" id="endDate" class="mt-2">
      <input type="time" id="endTime" class="mt-2">
      <input type="number" placeholder="Interval" class="mt-2" id="intervalInput">
    </div>
  </div>


    
  <div class="row">
    <div class="col-4" >
      <button onclick="show()" class="btn btn-primary mt-2">Tampilkan Visualisasi</button>
    </div>
  </div>

</div>

 

  <div>
    <canvas id="myChart"></canvas>
  </div>




