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

const optLokasi2=document.getElementById('lokasiSelection2')
const listLokasi2=document.getElementsByClassName("optLokasi2");

document.getElementById('kotaSelection2').addEventListener("change",function(event) {
    let selectedCity=event.target.value
    for (let i=0;i<listLokasi2.length;i++) {
        if(listLokasi2[i].getAttribute('city')!=selectedCity){
            listLokasi2[i].hidden=true
        }else{
            listLokasi2[i].hidden=false
        }
      }
      optLokasi2.value=-1
     
  
  });



