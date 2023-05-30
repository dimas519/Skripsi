<link rel="stylesheet" href="{{'css/location.css'}}">
<script src="https://cdn.plot.ly/plotly-2.23.2.min.js" charset="utf-8"></script>
<script src="{{asset('js/mainUser.js')}}" defer></script>


<div class="container" id="workSheet">
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
        <option hidden class="optLokasi" value="{{$lokasi['identifier']}}" city="{{$lokasi['idKota']}}">{{$lokasi['nama']}}</option>
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
      <div class="pt-3">Diagram Type</div>
    </div>

    <div class="col-3">
      <div>
        <input type="date" id="endDate" class="mt-2">
        <input type="time" id="endTime" class="mt-2">
      </div>
      <div>
        <select class="mt-2" name="" id="typeSelection">
          <option value="1" for="suhu tekanan kelembapan">Select city and location</option>
          <option value="line" for="suhu tekanan kelembapan">Line Chart</option>
          <option value="scatter" for="suhu tekanan kelembapan">Area Chart</option>
          <option value="box" for="suhu tekanan kelembapan">Box Plot</option>
          <option value="scatter3d" for="akselerasi" hidden>Line chart for acceleration</option>
          <option value="mesh3d" for="akselerasi" hidden>Scatter 3d (only for acceleration)</option>
          
        </select>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="col-4" >
      <button onclick="show()" class="btn btn-primary mt-2">Tampilkan Visualisasi</button>
    </div>
  </div>

  <br><br>

  <div id="myPlot" style="width:100%; height: 30px;"></div>
</div>



  
