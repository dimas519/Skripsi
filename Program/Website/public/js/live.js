

const listLokasi=document.getElementsByClassName("optLokasi");
const  layoutLive = { width: 250, height: 150, margin: { t: 40, l: 30, b: 40, r:30 }};


class Live{

    constructor(api){
        this.api=api;
    }

    sensing(identifier,interval){
        let endpoint=this.api+identifier
        let suhu=document.getElementById("suhuText"+identifier)
        let tekanan=document.getElementById("tekananText"+identifier)
        let akselerasi=document.getElementById("akselerasiText"+identifier)
        let timeDoc=document.getElementById("timeText"+identifier)

        let idBS=identifier

        if(interval==undefined){
            interval=1000
        }
        

        let data
        let datachart
        this.intervalLive=setInterval(async function(){
            const response = await fetch(endpoint);
            data = await response.json();


            if (data['time']=='1970-01-01 00:00:00'){
                timeDoc.textContent='Offline'
            }else{
                timeDoc.textContent=data['time']
            }
           
            if(data['result']['T']==undefined){
                suhu.textContent='Offline'
                suhu.nextElementSibling.hidden=true
            }else{
                suhu.textContent=data['result']['T']
                suhu.nextElementSibling.hidden=false
            }
            
            if(data['result']['Pa']==undefined){
                tekanan.textContent='Offline'
                tekanan.nextElementSibling.hidden=true
            }else{
                tekanan.textContent=data['result']['Pa']
                tekanan.nextElementSibling.hidden=false
            }

            if(data['result']['a']==undefined){
                akselerasi.textContent='Offline'
                akselerasi.nextElementSibling.hidden=true
            }else{
                akselerasi.textContent=data['result']['a']
                akselerasi.nextElementSibling.hidden=false
            }
            
            if(data['result']['rh']==undefined){
                Plotly.update(`kelembapanText${idBS}`, {value:0}, {}, [0])
            }else{
                Plotly.update(`kelembapanText${idBS}`, {value:data['result']['rh']}, {}, [0])
            }
    
        },interval);     

        



      }

    stop(){
        clearInterval(this.intervalLive)
    }
    
}


function initNewLive(idBS,interval){

    let sensing=new Live(`${urlAPI}/realTime?idBS=`);

    datachart = [
        {
            domain: { x: [0, 1], y: [0, 1] },
            value: 0.00,
            number: { suffix: "%", valueformat: ".2f" },
            title: { text: "Kelembapan",font: { size: 20 } },
            type: "indicator",
            mode: "gauge+number",
            gauge: { axis: { 
                range: [0, 100] ,
                tickvals: [0, 20, 40, 60, 80, 100]
                } 
            }

        }
    ];



    Plotly.newPlot(`kelembapanText${idBS}`, datachart, layoutLive);

    console.log(interval)

    sensing.sensing(idBS,interval);

}


document.getElementById('kotaSelection').addEventListener("change",function(event) {
    let selectedCity=event.target.value
    console.log(selectedCity)
    for (let i=0;i<listLokasi.length;i++) {
        if(listLokasi[i].getAttribute('city')!=selectedCity){
            listLokasi[i].style.display="none"
            // listLokasi[i].hidden=false
        }else{
            listLokasi[i].style.display="block"
            // listLokasi[i].hidden=true
        }
      }

  
  });