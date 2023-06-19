

const ctx = document.getElementById('myChart');
const navSensor=document.getElementById("navSensorAvaiable")
const optType=document.getElementById("typeSelection")
const chartDiv=document.getElementsByClassName("chart")
const chartHeight=(document.getElementById('workSheet').offsetWidth/16)*9


const optTypeAceleration=document.getElementById("typeSelectionAceleration")
let sensorSelected=[true,false,false,false]
let sensorOrder=['suhu','tekanan','kelembapan','akselerasi']
const selectedLokasi=document.getElementsByClassName("selectedLokasi")
let selectedKota=[]
let selectedKotaName=[]

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
    tickangle: -45,
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
    doAlert ? alert('Pilih Tanggal Mulai') : null
    return false;
  }else if(startTime.value == ''){
    doAlert ? alert('Pilih Waktu Mulai') : null
    return false;
  }else if(endDate.value == ''){
    doAlert ? alert('Pilih Tanggal Akhir') : null
    return false;
  }else if(endTime.value == ''){
    doAlert ? alert('Pilih Waktu Akhir') : null
    return false;
  }else if(selectedKota.length==0){
    doAlert ? alert('Pilih Lokasi lebih dahulu'):null
    return false;
  }else if(intervalInput.value == ''){
    doAlert ? alert('Pilih interval') : null
    return false;
  }else if(optType.value==1){
    doAlert ? alert('Pilih tipe grafik') : null
    return false;
  }else if(sensorSelected[3]==true && optTypeAceleration.value==1){
    doAlert ? alert('Pilih tipe grafik untuk akselerasi') : null
    return false;
  }


  if (startDate.value > endDate.value){
    doAlert ? alert('Tanggal Selesai Harus Sesudah Tanggal Mulai') : null
  }else if(startDate.value == endDate.value){
    if(startTime.value >= endTime.value ){
      doAlert ? alert('Waktu Selesai Harus Sesudah Waktu Mulai') : null
    }
  }



  return true;
}



function show3D(jsonData,judul){
  layout.yaxis.title.text="g"
  layout.title.text=judul+"*"

  let tipe=optTypeAceleration.value;

  
  if (optType.value=='box'){
    alert("Akselerasi tidak dapat ditampilkan jika pemilihan visualisasi lainnya boxplot")
    return null;
  }
  


  let data=[]
  for (let a=0;a<selectedKota.length;a++){
    let dataSensing=[]
    let time=[]
    let bs=selectedKota[a];
    let bsData=jsonData[bs]

    let x=[]
    let y=[]
    let z=[]



    for(let i=0;i<bsData.length;i++){
      x.push(bsData[i]['akselerasi']['x'])
      y.push(bsData[i]['akselerasi']['y'])
      z.push(bsData[i]['akselerasi']['z'])
      time.push(bsData[i]['timeStamp'])
    }


    if (tipe!="lines"){
      data.push ( 
        {
          x: x,
          y: y,
          z: z,
          type: tipe
          ,name:selectedKotaName[a]
        })
    }else{
      let Xtrace = {
        x: time,
        y: x,
        name:"X"+selectedKotaName[a],
        type: 'lines'
      };

      let Ytrace = {
        x: time,
        y: y,
        name:"Y"+selectedKotaName[a],
        type: 'lines'
      };

      let Ztrace = {
        x: time,
        y: z,
        name:"Z"+selectedKotaName[a],
        type: 'lines'
      };

      data.push(Xtrace,Ytrace,Ztrace)

    }
  }

  console.log(data)

  // for (let x=0;x<selectedKota.length;x++){
  //   let dataSensing=[]
  //   let time=[]
  //   let bs=selectedKota[x];
  //   let bsData=jsonData[bs]
  //   console.log(bsData)
  //   for(let i=0;i<bsData.length;i++){
  //     dataSensing.push(bsData[i][jenisData])
  //     time.push(bsData[i]['timeStamp'])
  //   }


  //   data.push({x:time,y:dataSensing,type:tipe, name:selectedKotaName[x]})

  // }


if(tipe=="scatter"){
  data[0].fill='tonexty'
}





  Plotly.newPlot('myPlotakselerasi', data, layout);
}


function show2D(jsonData,judul,jenisData,SelectedKota){
  layout.yaxis.title.text=labelsType(jenisData)
  layout.title.text=judul
  
  let tipe=optType.value;

  
  


  if(tipe=='box'){
    return box(jsonData,jenisData)
  }

    let data=[]

    for (let x=0;x<selectedKota.length;x++){
      let dataSensing=[]
      let time=[]
      let bs=selectedKota[x];
      let bsData=jsonData[bs]

      for(let i=0;i<bsData.length;i++){
        dataSensing.push(bsData[i][jenisData])
        time.push(bsData[i]['timeStamp'])
      }

      data.push({x:time,y:dataSensing,type:tipe, name:selectedKotaName[x]})

    }

  if(tipe=="scatter"){
    for (let x=0;x<data.length;x++){
      data[x].fill='tozeroy'
    }
  }

  let newLayout={...layout}; //cara copy objek, karena layoutlive merupakan layout utama, sedangkan yang ini akan berubah ubah sesuai tipe data
        



  Plotly.newPlot('myPlot'+jenisData, data, newLayout);
}





function show(doAlert=true){
if (!validInput(doAlert)){ 
    return null;
  }

  let type=document.getElementsByClassName("selected")[0].getAttribute("box")
  let start=`${startDate.value} ${startTime.value}`
  let end=`${endDate.value} ${endTime.value}`
  let bs=optLokasi.options[optLokasi.selectedIndex].text
  let tipe=optType.value;


  let jsonString={
    "node":selectedKota
    ,"start":`${start}:00`
    ,"end":`${end}:00`
    ,"interval":intervalInput.value
    ,"stat":"avg"
}


// if(selectedKota.length==1){
  // jsonString.idBS=selectedKota[0]

// }





    

    //khusus untuk boxplot dia raw tidak di aggregasi
if(tipe=='box'){
    jsonString.stat="raw"
  }
  
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



              for(let i=0;i<sensorSelected.length;i++){
                if(sensorSelected[i]){

                  
                  if(!first){
                  chartDiv[i].style.display="block"
                  chartDiv[i].style.marginTop="750px"
                  }
                  first=false;

                  type=sensorOrder[i]
                  let judul=`Grafik ${type} dari ${start} sampai ${end}`
                  
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
  let lokasi=event.target.value
  
  selectedKota.push(lokasi)

  for (let i=0;i<selectedLokasi.length;i++){
    if(selectedLokasi[i].value==lokasi){
      selectedLokasi[i].hidden=false;
      selectedKotaName.push(selectedLokasi[i].textContent)
    }
  }

  for (let i=0;i<listLokasi.length;i++){
    if(listLokasi[i].value==lokasi){
      listLokasi[i].hidden=true;
    }
  }

  optLokasi.value=-1
  

console.log(selectedKotaName)
});

function removeSelected(elem){
  let lokasi=elem.value
  let index = selectedKota.indexOf(lokasi);
  if (index !== -1) {
    selectedKota.splice(index, 1);
    selectedKotaName.splice(index,1)
  }

  for (let i=0;i<selectedLokasi.length;i++){
    if(selectedLokasi[i].value==lokasi){
      selectedLokasi[i].hidden=true;
    }
  }


  for (let i=0;i<listLokasi.length;i++){
    if(listLokasi[i].value==lokasi){
      listLokasi[i].hidden=false;
    }
  }

  console.log(selectedKotaName)
}



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