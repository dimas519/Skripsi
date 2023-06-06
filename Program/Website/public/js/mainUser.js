

const ctx = document.getElementById('myChart');
const navSensor=document.getElementById("navSensorAvaiable")
const optType=document.getElementById("typeSelection")
const chartDiv=document.getElementsByClassName("chart")
const chartHeight=(document.getElementById('workSheet').offsetWidth/16)*9


const optTypeAceleration=document.getElementById("typeSelectionAceleration")
let sensorSelected=[true,false,false,false]
let sensorOrder=['suhu','tekanan','kelembapan','akselerasi']

let layout = {
  width: document.getElementById('workSheet').offsetWidth,
  height: chartHeight,
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
  }else if(optTypeAceleration.value==1){
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

function show3D(jsonData,judul){
  // labelData=labelsType(tipe)
  layout.title.text=judul+"*"

  let tipe=optTypeAceleration.value;


  let x=[]
  let y=[]
  let z=[]
  let time=[]

  for(let i=0;i<jsonData.length;i++){
    x.push(jsonData[i]['akselerasi']['x'])
    y.push(jsonData[i]['akselerasi']['y'])
    z.push(jsonData[i]['akselerasi']['z'])
    time.push(jsonData[i]['timeStamp'])
  }

  let data;
  if (tipe!="lines"){
    data = [
      {
        x: x,
        y: y,
        z: z,
        type: "tipe"
      }
    ];
  }else{
    let Xtrace = {
      x: time,
      y: x,
      type: 'scatter'
    };

    let Ytrace = {
      x: time,
      y: y,
      type: 'scatter'
    };

    let Ztrace = {
      x: time,
      y: z,
      type: 'scatter'
    };

    data=[Xtrace, Ytrace, Ztrace]

  }


  Plotly.newPlot('myPlotakselerasi', data, layout);
}


function show2D(jsonData,judul,jenisData){
  layout.yaxis.title.text=labelsType(jenisData)
  layout.title.text=judul
  
  let tipe=optType.value;

  let dataSensing=[]
  let time=[]

  for(let i=0;i<jsonData.length;i++){
    dataSensing.push(jsonData[i][jenisData])
    time.push(jsonData[i]['timeStamp'])
  }


  if(tipe=='box'){
    return box(dataSensing,time,jenisData,judul)
  }

  let data = [
    {
      x: time,
      y: dataSensing,
      type: tipe
    }
  ];



  if(tipe=="scatter"){
    data[0].fill='tonexty'
  }

  
  
  Plotly.newPlot('myPlot'+jenisData, data, layout);
}


function box(dataSensing,time,jenisData,judul){

  let data = [];

    for(let i=0;i<dataSensing.length;i++){
      data.push(
        {
          y: dataSensing[i],
          type: "box",
          name: time[i]
        },
      )
    }
    
  Plotly.newPlot('myPlot'+jenisData, data, layout);

}




function show(doAlert=true){
// if (!validInput(doAlert)){ 
  //   return null;
  // }

  let type=document.getElementsByClassName("selected")[0].getAttribute("box")
  let start=`${startDate.value} ${startTime.value}`
  let end=`${endDate.value}-${endTime.value}`
  let bs=optLokasi.options[optLokasi.selectedIndex].text
  let tipe=optType.value;


  let jsonString={
    "idBS":`${optLokasi.value}`
    ,"start":`${start}:00`
    ,"end":`${end}:00`
    ,"interval":`${intervalInput.value}`
    ,"stat":"avg"
}



    
  jsonString={ //debugger
        "idBS":"AAAb"
        ,"start":"2023-05-08 00:00:00"
        ,"end":"2023-05-08 23:55:00"
        ,interval:3600
        ,"stat":"avg"
    }


    //khusus untuk boxplot dia raw tidak di aggregasi
if(tipe=='box'){
    jsonString.stat="raw"
  }
  

    // fetch(`${window.location.origin}/data`,{
      fetch(`${urlAPI}/data`,{
        method: "POST",
        headers: {
            Accept: 'application.json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonString),
        }).then(response => response.json()) .then(response=>{


            
            if(response['result']=='false'){
              alert("Data tidak ditemukan")
            }else{ 
              
              responseResult=response['result']
              let first=true

              console.log(responseResult)

              for(let i=0;i<sensorSelected.length;i++){
                if(sensorSelected[i]){
                  if(!first){
                  chartDiv[i].style.display="block"
                  chartDiv[i].style.marginTop="750px"
                  }
                  first=false;

                  type=sensorOrder[i]
                  let judul=`Grafik ${type} di ${bs} dari ${start} sampai ${end}`
                    if(type=="akselerasi"){
                      accInfo.style.display="block"
                      accInfo.style.marginTop="750px"
                      show3D(responseResult,judul)
                    }else{
                      show2D(responseResult,judul,type)
                    }
                }else{



                }
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
  // let selectedBefore=document.getElementsByClassName("selected")

  

  // selectedBefore[0].classList.remove("selected")// hapus yang sebelumnya sudah masuk
  elem.parentNode.classList.toggle("selected")
  let index=elem.getAttribute("index")
  sensorSelected[index]=!sensorSelected[index]
  console.log(sensorSelected)

  //untuk memfilter tipe grafik yang tidak sesuai
  // let selectedTipe=elem.parentElement.getAttribute("box")
  // let opsiTipe=optType.children;
  // for(let i=0;i<opsiTipe.length ;i++){

  //   let tujuan=opsiTipe[i].getAttribute("for").split(" ");
 
  //   if( tujuan.includes(selectedTipe)){
  //     opsiTipe[i].hidden=false;
  //   }else{
  //     opsiTipe[i].hidden=true;
  //   }
  // }

  // if(selectedTipe=="akselerasi"){
  //   optType.selectedIndex=4;
  // }else{
  //   if(optType.selectedIndex>=4){
  //     optType.selectedIndex=1;
  //   }
  // }


}

// optType.addEventListener("change",function(event) {
//   show(false)
// });