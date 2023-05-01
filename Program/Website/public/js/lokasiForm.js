c

const ctx = document.getElementById('myChart');
const listLokasi=document.getElementsByClassName("optLokasi");
const optLokasi=document.getElementById('lokasiSelection')
const navSensor=document.getElementById("navSensorAvaiable")

const startDate=document.getElementById("startDate")
const startTime=document.getElementById("startTime")
const endDate=document.getElementById("endDate")
const endTime=document.getElementById("endTime")
const intervalInput=document.getElementById("intervalInput")

const suhuNav=document.getElementById("intervalInput")
var myChart = null;



function select(elem){
    let selectedBefore=document.getElementsByClassName("selected") // hapus yang sebelumnya sudah masuk
    selectedBefore[0].classList.remove("selected")
    elem.parentNode.classList.add("selected")
}


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








function showLine(jsonData){
    if(myChart){
        myChart.clear();
        myChart.destroy();
    }

    myChart=new Chart(ctx, {
        
        data: {
            type: 'line',
        //   labels: jsonData['time'],
          datasets: [{
            data: [30,12.32,12.42,22,29],
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            },
            x: {
                type: 'linear',
                position: 'top'
              }
          },
          plugins: {
            legend: {
              display: false
            }
          }
        }
      });
}




function show(){
    // let jsonString={
    //     "idBS":"AAAA"
    //     ,"start":`${startDate.value} ${startTime.value}:00`
    //     ,"end":`${endDate.value}-${endTime.value}:00`
    //     ,interval:`${intervalInput}`
    // }

    let jsonString={
        "idBS":"AAAA"
        ,"start":"2022-11-01 00:00:00"
        ,"end":"2022-11-30-23:55:00"
        ,interval:86400
        ,"type":document.getElementsByClassName("selected")[0].getAttribute("box")
    }

    console.log(jsonString)

    
    
    fetch(`${window.location.origin}/data`,{
        method: "POST",
        headers: {
            Accept: 'application.json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonString),
        }).then(response => response.json()) .then(response=>{
            showLine(response)
        }).catch((error) => {
            console.log(error)
        });



}





