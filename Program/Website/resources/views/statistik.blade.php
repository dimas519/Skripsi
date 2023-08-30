<script src="https://cdn.plot.ly/plotly-2.23.2.min.js" charset="utf-8"></script>

<script>
    const urlAPI='{{$api}}'
    </script>
  <link rel="stylesheet" href="{{'css/mainUser.css'}}">
  
  <script src="{{asset('js/lokasiFilter.js')}}" defer></script>
  <script src="{{asset('js/statistic.js')}}" defer></script>
  
  
  <div class="container" id="workSheet">
    <div class="row">
      <br>
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
          <option hidden class="optLokasi" value="{{$lokasi['identifier']}}" city="{{$lokasi['idKota']}}">{{$lokasi['namaLokasi']}} {{$lokasi['indoor']==1?"- Indoor":""}} {{"(lat: ".$lokasi['latitude']." ,long: ".$lokasi['longtitude'].")"}}</option>
          @endforeach
        </Select>
      </div>
        <div class="col-1">
        <div class="pt-2" >Start Time </div>
        <div class="pt-3">Interval </div>
      </div>
      <div class="col-3">
        <input type="date" id="startDate" class="mt-2" >
        <input type="time" id="startTime" class="mt-2" >
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
          <select class="mt-2" name="b" id="typeSelection">
            <option value="1" for="suhu tekanan kelembapan">Pilih Diagram</option>
            <option value="scatter"> Scatter plot</option>
            <option value="boxFloating">Min-Max</option>
            <option value="box">box plot</option>
            <option value="summary">Summary</option>
          </select>
        </div>
      </div>
    </div>
  
    <br>


  <div class="alert alert-secondary" role="alert" style="display: block">
  Lokasi dipilih:
  @foreach ($semuaLokasi as $lokasi)
  {{-- <option hidden class="optLokasi" value="{{$lokasi['identifier']}}" city="{{$lokasi['idKota']}}">{{$lokasi['nama']}}</option> --}}
  <button type="button" hidden class="btn btn-secondary selectedLokasi" onclick="removeSelected(this)" value="{{$lokasi['identifier']}}">{{$lokasi['namaLokasi']}}</button>
  @endforeach

  </div>

  <div class="alert alert-light" role="alert" id="scatter" hidden>
      <h4>Konfigurasi Scatter</h4>
      Pilih data untuk X dan Y

      <select class="form-select" aria-label="Default select example" id="scatterX">
        <option selected>Axis X</option>
        <option value="suhu">Suhu</option>
        <option value="kelembapan">Kelembapan</option>
        <option value="Tekanan">Tekanan</option>
      </select>

      <br>

      <select class="form-select" aria-label="Default select example" id="scatterY">
        <option selected>Axis Y</option>
        <option value="suhu">Suhu</option>
        <option value="kelembapan">Kelembapan</option>
        <option value="Tekanan">Tekanan</option>
      </select>

  </div>

  <div class="alert alert-light" role="alert" id="summary" hidden>
    <h4>Konfigurasi Summary</h4>
    
    <select class="form-select" aria-label="Default select example" id="summaryType">
      <option selected>Pilih Parameter</option>
      <option value="inQ">Kuartile</option>
      <option value="split-1">Jumlah per 1</option>
      <option value="split-2">Jumlah per 2</option>
      <option value="split-5">Jumlah per 5</option>
      <option value="split-10">Jumlah per 10</option>
      <option value="split-20">Jumlah per 20</option>
    </select>

    <br>

    <select class="form-select" aria-label="Default select example" id="summaryGraph">
      <option selected>Pilih Tipe Visualisasi</option>
      <option value="histogram">Histogram (Rekomendasi untuk Satu lokasi atau Jumlah per kecil)</option>
      <option value="box">Diagram Batang (Rekomendasi untuk lebih dari Satu lokasi)</option>
      <option value="pie">Diagram Lingkaran</option>
    </select>

</div>


  <button onclick="show()" class="btn btn-primary mt-2">Tampilkan Visualisasi</button>
  
    {{-- <div id="myPlot" style="width:100%; height: 30px;"></div> --}}
  
    <div id="myPlotsuhu" class="chart" style="width:100%; height: 30px; display:none"></div>
    
    <div id="myPlottekanan" class="chart" style="width:100%; height: 30px; margin-top:750px; display:none"></div>
    
  
    
    <div id="myPlotkelembapan" class="chart" style="width:100%; height: 30px; margin-top:750px; display:none"></div>
    
  
{{-- 
    <div id="myPlotakselerasi" class="chart" style="width:100%; height: 30px; margin-top:750px"></div>  --}}
    
  
    @include("accelerationInfo")
  </div>
  
  
  
    
  