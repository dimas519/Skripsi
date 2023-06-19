const startDate=document.getElementById("startDate")
const startTime=document.getElementById("startTime")
const endDate=document.getElementById("endDate")
const endTime=document.getElementById("endTime")
const intervalInput=document.getElementById("intervalInput")

const optLokasi=document.getElementById('lokasiSelection')
const listLokasi=document.getElementsByClassName("optLokasi");
const accInfo=document.getElementById("akelserasiInfo")






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
    // navSensor.hidden=true

});
optLokasi.addEventListener("change",function(event) {
  // navSensor.hidden=false
});

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