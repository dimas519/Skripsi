const ctx = document.getElementById('myChart');
const listLokasi=document.getElementsByClassName("optLokasi");
const optLokasi=document.getElementById('lokasiSelection')
const navSensor=document.getElementById("navSensorAvaiable")
const optType=document.getElementById("typeSelection")

const startDate=document.getElementById("startDate")
const startTime=document.getElementById("startTime")
const endDate=document.getElementById("endDate")
const endTime=document.getElementById("endTime")
const intervalInput=document.getElementById("intervalInput")



let layout = {
  width: document.getElementById('workSheet').offsetWidth,
  height: (document.getElementById('workSheet').offsetWidth/16)*9,
  margin: {
    l: 75,
    r: 50,
    b: 50,
    t: 100,
    pad: 4
  },
  paper_bgcolor: '#c7c7c7',
  plot_bgcolor: '#ffffff',
  title : {
    font: {
      family: 'Courier New, monospace',
      size: 24
    },
    xref: 'paper',
  },
  yaxis: {
    title: {
      font: {
        family: 'Courier New, monospace',
        size: 18,
        color: '#000000'
      }
    }
  },
  xaxis: {
      side:"top",
  }
};





const config = {responsive: true}


function validInput(doAlert=true){
  if(startDate.value == ''){
    doAlert ? alert('Select start date') : null
    return false;
  }else if(startTime.value == ''){
    doAlert ? alert('Select start time') : null
    return false;
  }else if(endDate.value == ''){
    doAlert ? alert('Select end date') : null
    return false;
  }else if(endTime.value == ''){
    doAlert ? alert('Select end time') : null
    return false;
  }else if(intervalInput.value == ''){
    doAlert ? alert('Select interval') : null
    return false;
  }else if(optType.value==1){
    doAlert ? alert('Pilih tipe grafik') : null
  }
  return true;
}

function labelsType(type){
  
  if(type=='suhu'){
    return 'Celcius'
  }else if(type=='kelembapan'){
    return '%'
  }else if(type=='tekanan'){
    return 'kPa'
  }else if(type=='akselerasi'){
    return 'g'
  }
}

function show3D(jsonData,tipe,judul){
  // labelData=labelsType(tipe)
  layout.yaxis.title.text="Celcius"
  layout.title.text=judul

  let data = [
    {
      x: jsonData['value']['x'],
      y: jsonData['value']['y'],
      z:jsonData['value']['z'],
      type: tipe
    }
  ];


  Plotly.newPlot('myPlot', data, layout);
}


function show2D(jsonData,tipe,judul,jenisData){
  layout.yaxis.title.text=labelsType(jenisData)
  layout.title.text=judul
  
  if(tipe=='box'){
    return box(jsonData,tipe,judul)
  }

  let data = [
    {
      x: jsonData['time'],
      y: jsonData['value'],
      type: tipe
    }
  ];

  if(tipe=="scatter"){
    data[0].fill='tonexty'
  }

  
  
  Plotly.newPlot('myPlot', data, layout);
}


function box(jsonData,tipe,judul){
  let value=jsonData['value']
  let date=jsonData['time']
  let data = [];

    for(let i=0;i<value.length;i++){
      data.push(
        {
          y: value[i],
          type: "box",
          name: date[i]
        },
      )
    }
    
  Plotly.newPlot('myPlot', data, layout);

}




function show(doAlert=true){
// if (!validInput(doAlert)){ 
  //   return null;
  // }

  let type=document.getElementsByClassName("selected")[0].getAttribute("box")
  let start=`${startDate.value} ${startTime.value}`
  let end=`${endDate.value}-${endTime.value}`
  let bs=optLokasi.options[optLokasi.selectedIndex].text
  let judul=`Grafik ${type} di ${bs} dari ${start} sampai ${end}`
  let tipeGrafik=optType.value;

  let jsonString={
    "idBS":`${optLokasi.value}`
    ,"start":`${start}:00`
    ,"end":`${end}:00`
    ,"interval":`${intervalInput.value}`
    ,"type":type
    ,"graph":tipeGrafik
}

    
  jsonString={ //debugger
        "idBS":"AAAb"
        ,"start":"2023-05-08 00:00:00"
        ,"end":"2023-05-08 23:55:00"
        ,interval:3600
        ,"type":type
        ,"graph":tipeGrafik
    }

    fetch(`${window.location.origin}/data`,{
        method: "POST",
        headers: {
            Accept: 'application.json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonString),
        }).then(response => response.json()) .then(response=>{


            if(response['value']=='noData'){
              alert("Data tidak ditemukan")
            }else{

              if(type=="akselerasi"){
                show3D(response,tipeGrafik,judul)
              }else{
                show2D(response,tipeGrafik,judul,type)
              }

            }

            
        }).catch((error) => {
            console.log(error)
        });
}







//LISTENER
document.getElementById('kotaSelection').addEventListener("change",function(event) {
  let selectedCity=event.target.value
  for (let i=0;i<listLokasi.length;i++) {
      if(listLokasi[i].getAttribute('city')!=selectedCity){
          listLokasi[i].hidden=true
      }else{
          listLokasi[i].hidden=false
      }
    }
    optLokasi.value=-1
    navSensor.hidden=true

});
optLokasi.addEventListener("change",function(event) {
  navSensor.hidden=false
});


//untuk auto show kalau ganti sensor
function select(elem){

  //pindahin hightlight abu
  let selectedBefore=document.getElementsByClassName("selected") // hapus yang sebelumnya sudah masuk
  selectedBefore[0].classList.remove("selected")
  elem.parentNode.classList.add("selected")

  //untuk memfilter tipe grafik yang tidak sesuai
  let selectedTipe=elem.parentElement.getAttribute("box")
  let opsiTipe=optType.children;
  for(let i=0;i<opsiTipe.length ;i++){

    let tujuan=opsiTipe[i].getAttribute("for").split(" ");
 
    if( tujuan.includes(selectedTipe)){
      opsiTipe[i].hidden=false;
    }else{
      opsiTipe[i].hidden=true;
    }
  }

  if(selectedTipe=="akselerasi"){
    optType.selectedIndex=4;
  }else{
    if(optType.selectedIndex>=4){
      optType.selectedIndex=1;
    }
  }

  show(false)
}

optType.addEventListener("change",function(event) {
  show(false)
});