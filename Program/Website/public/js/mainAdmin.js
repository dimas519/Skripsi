const ctx = document.getElementById('myChart');
const listLokasi=document.getElementsByClassName("optLokasi");
const optLokasi=document.getElementById('lokasiSelection')
const navSensor=document.getElementById("navSensorAvaiable")
const optType=document.getElementById("typeSelection")








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
   

});



