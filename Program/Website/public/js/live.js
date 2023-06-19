

const listLokasi=document.getElementsByClassName("optLokasi");
const chartKelembapan=document.getElementById("kelembapanSelection")
const chartSuhu=document.getElementById("suhuSelection")
const chartTekanan=document.getElementById("tekananSelection")
const chartAkselerasi=document.getElementById("akselerasiSelection")


const  layoutLive = { width: 300, height: 150, margin: { t: 40, l: 30, b: 40, r:30 }};


class Live{
    constructor(api,identifier){
        this.url=api+identifier;
        this.idBS=identifier;
        this.time=null;

        this.kelembapan=document.getElementById("kelembapanText"+identifier)
        this.suhu=document.getElementById("suhuText"+identifier)
        this.tekanan=document.getElementById("tekananText"+identifier)
        this.akselerasi=document.getElementById("akselerasiText"+identifier)
        this.timeDoc=document.getElementById("timeText"+identifier)


        this.suhuFirstValue=true
        this.kelembapanFirstValue=true
        this.tekananFirstValue=true
        this.akselerasiFirstValue=true
        this.suhuType='text'
        this.kelembapanType='text'
        this.tekananType='text'
        this.akselerasiType='text'


    }

    visibilityText(elem,visibility,plotName){
        // try {
            if(visibility){
                (elem.parentElement.parentElement).setAttribute("style", "display:inline-block !important;");
                Plotly.purge(plotName)
            }else{
                (elem.parentElement.parentElement).setAttribute("style", "display:none !important;");
    
            }     
    }

    showTemperature(value){
        let plotName="myPlotsuhu"+this.idBS //diconcat dengan id bs karena myplotsuhu banyak, bisa untuk banyak bs
        
        switch(chartSuhu.value) {
            case "lines":

                if(this.suhuType!='lines'){
                    this.suhuFirstValue=true;// agar dia reset kalau yg berubah dari scatter
                    this.suhuType='lines'
                }
                

                this.showLines(plotName,this.suhuFirstValue,value,'Suhu',"lines")
                this.visibilityText(this.suhu,false,plotName)
                this.suhuFirstValue=false;
                break;
            case "simpleText":
                this.suhuType=undefined
                this.visibilityText(this.suhu,true,plotName)
                this.showSimpleText(this.suhu,value)
                this.suhuFirstValue=true;
                break;
            case "scatter":

                if(this.suhuType!='scatter'){
                    this.suhuFirstValue=true;// agar dia reset kalau yg berubah dari lines
                    this.suhuType='scatter'
                }
                
                this.showLines(plotName,this.suhuFirstValue,value,'Suhu',"area")
                this.visibilityText(this.suhu,false,plotName)
                this.suhuFirstValue=false;
                break;
                // code block
        }

    }

    showPressure(value){
        let plotName="myPlottekanan"+this.idBS //diconcat dengan id bs karena myplotsuhu banyak, bisa untuk banyak bs
        
        switch(chartTekanan.value) {
            case "lines":

                if(this.tekananType!='lines'){
                    this.tekananFirstValue=true;// agar dia reset kalau yg berubah dari scatter
                    this.tekananType='lines'
                }           

                this.showLines(plotName,this.tekananFirstValue,value,'Tekanan',"lines")
                this.visibilityText(this.tekanan,false,plotName)
                this.tekananFirstValue=false;

                break;
            case "simpleText":
                this.tekananType=undefined
                this.visibilityText(this.tekanan,true,plotName)
                this.showSimpleText(this.tekanan,value)
                this.tekananFirstValue=true;
                break;
            case "scatter":

                if(this.tekananType!='scatter'){
                    this.tekananFirstValue=true;// agar dia reset kalau yg berubah dari lines
                    this.tekananType='scatter'
                }

                this.showLines(plotName,this.tekananFirstValue,value,'Tekanan',"area")
                this.visibilityText(this.tekanan,false,plotName)
                this.tekananFirstValue=false;
                break;

                // code block
        }

    }

    showHumidity(value){

        let plotName="myPlotkelembapan"+this.idBS //diconcat dengan id bs karena myplotsuhu banyak, bisa untuk banyak bs
        
        switch(chartKelembapan.value) {
            case "lines":

                if(this.kelembapanType!='lines'){
                    this.kelembapanFirstValue=true;// agar dia reset kalau yg berubah dari scatter
                    this.kelembapanType='lines'
                }
                value=value==-1?0:value

                this.showLines(plotName,this.kelembapanFirstValue,value,'Kelembapan',"lines")
                this.visibilityText(this.kelembapan,false,plotName)
                this.kelembapanFirstValue=false;
                break;
            case "simpleText":
                value=value==-1?"Offline":value
                this.kelembapanType=undefined
                this.visibilityText(this.kelembapan,true,plotName)
                this.showSimpleText(this.kelembapan,value)
                this.kelembapanFirstValue=true;
                break;
            case "scatter":

                if(this.kelembapanType!='scatter'){
                    this.kelembapanFirstValue=true;// agar dia reset kalau yg berubah dari lines
                    this.kelembapanType='scatter'
                }
                
                value=value==-1?0:value
                this.showLines(plotName,this.kelembapanFirstValue,value,'Kelembapan',"area")
                this.visibilityText(this.kelembapan,false,plotName)
                this.kelembapanFirstValue=false;
                break;
            case "gauge":
                if(this.kelembapanType!='gauge'){
                    this.kelembapanFirstValue=true;// agar dia reset kalau yg berubah dari lines
                    this.kelembapanType="gauge"
                }
                value=value==-1?0:value
                this.showGauge(value)
                this.visibilityText(this.kelembapan,false,plotName)
                this.kelembapanFirstValue=false;
                break;
            case "bar":
                value=value==-1?0:value
                if(this.kelembapanType!='bar'){
                    this.kelembapanFirstValue=true;// agar dia reset kalau yg berubah dari lines
                    this.kelembapanType='bar'
                }
                

                this.showLines(plotName,this.kelembapanFirstValue,value,'Kelembapan',"area")
                this.visibilityText(this.kelembapan,false,plotName)
                this.kelembapanFirstValue=false;
                break;
  
        }
    }
    
    showAceleration(value){
        let plotName="myPlotakselerasi"+this.idBS //diconcat dengan id bs karena myplotsuhu banyak, bisa untuk banyak bs
        
        switch(chartAkselerasi.value) {
            case "lines":

                if(this.akselerasiType!='lines'){
                    this.akselerasiFirstValue=true;// agar dia reset kalau yg berubah dari scatter
                    this.akselerasiType='lines'
                }

                this.showLines3D(plotName,this.akselerasiFirstValue,value,'Akselerasi',"lines")
                this.visibilityText(this.akselerasi,false,plotName)
                this.akselerasiFirstValue=false;

                break;
            case "simpleText":
                this.akselerasiType=undefined
                this.visibilityText(this.akselerasi,true,plotName)
                this.showSimpleText(this.akselerasi,value)
                this.akselerasiFirstValue=true;
                break;
            case "scatter":

                if(this.akselerasiType!='scatter'){
                    this.akselerasiFirstValue=true;// agar dia reset kalau yg berubah dari lines
                    this.akselerasiType='scatter'
                }
                this.showLines3D(plotName,this.akselerasiFirstValue,value,'akselerasi',"area")
                this.visibilityText(this.akselerasi,false,plotName)
                this.akselerasiFirstValue=false;
                break;

                // code block
        }

    }

    showSimpleText(elem,value){
        
        elem.textContent=value
        elem.nextElementSibling.hidden=value=='Offline'?true:false
    }

    showLines3D(plotName,create,value,title,type){


        if(create){

            let Xtrace = {
                x: [this.time],
                y: [value[0]],
                name:"X",
                type: 'lines'
              };
          
              let Ytrace = {
                x: [this.time],
                y: [value[1]],
                name:"Y",
                type: 'lines'
              };
          
              let Ztrace = {
                x: [this.time],
                y: [value[2]],
                name:"Z",
                type: 'lines'
              };
                  
            let data=[Xtrace, Ytrace, Ztrace]
     
            if(type=="area"){
                data[0].fill='tonexty'
                data[1].fill='tonexty'
                data[2].fill='tonexty'
              }

            console.log(data)
             
            let newLayout={...layoutLive}; //cara copy objek, karena layoutlive merupakan layout utama, sedangkan yang ini akan berubah ubah sesuai tipe data
        
            newLayout["title"]={text:title,font:{size:20}}

            Plotly.newPlot(plotName, data,newLayout);
        }else{

            let update={y:[[value[0]],[value[1]],[value[2]]] , x:[[this.time],[this.time],[this.time]]    }

            
        Plotly.extendTraces(plotName,update, [0,1,2],30)
        }
        
        
    }


    showLines(plotName,create,value,title,type){
        if(create){
            let data = [
                {
                  x: [this.time],
                  y: [value],
                  type: type,
        
                }
              ];

              if(type=="area"){
                data[0]["fill"]='tonexty'
              }

              
            let newLayout={...layoutLive}; //cara copy objek, karena layoutlive merupakan layout utama, sedangkan yang ini akan berubah ubah sesuai tipe data
        
            newLayout["title"]={text:title,font:{size:20}}

            Plotly.newPlot(plotName, data,newLayout);
        }else{

            let update = {
                x:  [[this.time]],
                y: [[value]]
            }
            
            Plotly.extendTraces(plotName,update, [0],30)
        }
        
        
    }


    showGauge(value){
        if(this.kelembapanFirstValue){
            let datachart = [
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

            Plotly.newPlot(`myPlotkelembapan${this.idBS}`, datachart, layoutLive);
        }else{
            Plotly.update(`myPlotkelembapan${this.idBS}`, {value:value}, {}, [0])
        }
    }


    getData(){
        fetch(this.url,{
            method: "GET",
            headers: {
                Accept: 'application.json',
                'Content-Type': 'application/json'
            },
            }).then(response => response.json()) .then(response=>{
    
    
                
                if (response['time']=='1970-01-01 00:00:00'){
                    this.timeDoc.textContent='Offline'
                }else{
                    this.timeDoc.textContent=response['time']
                    this.time=response['time']
                }
               
                if(response['result']['T']==undefined){
                    this.showTemperature('Offline')
                }else{
                    this.showTemperature(response['result']['T'])
                }
                
                if(response['result']['Pa']==undefined){
                    this.showPressure('Offline')
                }else{
                    this.showPressure(response['result']['Pa'])
                }
        
                if(response['result']['a']==undefined){
                    this.showAceleration('Offline')
                }else{
                    this.showAceleration(response['result']['a'])
                }
                
                if(response['result']['rh']==undefined){
                    this.showHumidity(-1)
                }else{
                    this.showHumidity(response['result']['rh'])
                }
    
                
            }).catch((error) => {
                console.log(error)
            });





    }

    

    stop(){
        clearInterval(this.intervalLive)
    }

    

    








    
}


function initNewLive(idBS,interval){

    let live=new Live(`${urlAPI}/realTime?node=`,idBS);
    setInterval(function(){live.getData()},1000);


    console.log(interval)

    // live.live(interval);

}


document.getElementById('kotaSelection').addEventListener("change",function(event) {
    let selectedCity=event.target.value
    console.log(selectedCity)
    for (let i=0;i<listLokasi.length;i++) {
        if(selectedCity!=-1 && listLokasi[i].getAttribute('city')!=selectedCity ){
            listLokasi[i].style.display="none"
            // listLokasi[i].hidden=false
        }else{
            listLokasi[i].style.display="block"
            // listLokasi[i].hidden=true
        }
      }

  
  });