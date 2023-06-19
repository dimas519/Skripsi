const optType=document.getElementById("typeSelection");
const selectedLokasi=document.getElementsByClassName("selectedLokasi");
const scatterConf=document.getElementById('scatter');
const xScatter=document.getElementById("scatterX");
const yScatter=document.getElementById("scatterY");

const plotSuhu=document.getElementById("myPlotsuhu")
const plottekanan=document.getElementById("myPlottekanan")
const plotkelembapan=document.getElementById("myPlotkelembapan")
const supportedSensor=['suhu','kelembapan','tekanan'];

const summaryConf=document.getElementById("summary")
const summaryType=document.getElementById("summaryType")
const summaryGraph=document.getElementById("summaryGraph")
let graph=document.getElementsByClassName("chart");
let selectedKota=[]
let selectedKotaName=[]


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
        size: 24,
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
        automargin: true,
        side:"top",
    },
    


  };


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


  function showScatter(jsonData){
      let data=[]
  
      for (let x=0;x<selectedKota.length;x++){
        let xValue=[]
        let yValue=[]
        let bs=selectedKota[x];
        let bsData=jsonData[bs]
  
        for(let i=0;i<bsData.length;i++){
            xValue.push(bsData[i][xScatter.value])
            yValue.push(bsData[i][yScatter.value])
        }
  
        data.push({x:xValue,y:yValue,type:"scatter", mode: 'markers', name:selectedKotaName[x]})
  
      }
  
  
  
    let newLayout={...layout}; //cara copy objek, karena layoutlive merupakan layout utama, sedangkan yang ini akan berubah ubah sesuai tipe data
    newLayout.yaxis.title.text=(yScatter.value)
    newLayout.xaxis['title']={text:xScatter.value, standoff: 2}
    newLayout.title.text=`Grafik Perbandingan antara ${xScatter.value} dengan ${yScatter.value}`
    
      
        Plotly.newPlot("myPlotsuhu", data, newLayout);
    

    
  }

  function showMinMax(jsonData,jenisData){
    layout.yaxis.title.text="Waktu"
    layout.xaxis['title']={text: jenisData, standoff: 2}
    layout.title.text=`Grafik Min-max ${jenisData} dengan interval ${intervalInput.value} detik`
    
      let data=[]
  
      for (let x=0;x<selectedKota.length;x++){
        let start=[]
        let plus=[]
        let bs=selectedKota[x];
        let bsData=jsonData[bs]
        let date=[]
  
        for(let i=0;i<bsData.length;i++){
            date.push(bsData[i]['timeStamp'])
            

            let sortedData=(bsData[i][jenisData]).sort()
            start.push(sortedData[0])
            plus.push(sortedData[sortedData.length-1]-sortedData[0])
            
        }
  
        data.push(
            {x:plus, //nambah brp
                base:start, //mulai di mana
                orientation: 'h',
                y:date,
                hovertemplate:'Min :%{base:.2f}' +
                        '<br>Max :%{x:.2f}'+
                        '<br>Time :%{y}' ,
                type:"bar", 
                mode: 'markers', 
                name:selectedKotaName[x]})
  
      }
  

  
    let newLayout={...layout}; //cara copy objek, karena layoutlive merupakan layout utama, sedangkan yang ini akan berubah ubah sesuai tipe data
    newLayout.yaxis.title.text="Waktu"
    newLayout.xaxis['title']={text: jenisData, standoff: 2}
    newLayout.title.text=`Grafik Min-max ${jenisData} dengan interval ${intervalInput.value} detik`

    newLayout.yaxis["type"]="date"

    
    Plotly.newPlot('myPlot'+jenisData, data, newLayout);
  }


  function showBox(jsonData,jenisData){

    let data = [];
  
    for (let x=0;x<selectedKota.length;x++){
      let dataSensing=[]
      let time=[]
      let bs=selectedKota[x];
      let bsData=jsonData[bs]
    
  
  
      for(let i=0;i<bsData.length;i++){
        let sense=bsData[i][jenisData]
  
        for (let u=0;u<sense.length;u++){
          dataSensing.push(bsData[i][jenisData][u])
        }
     
        for (let u=0;u<sense.length;u++){
          time.push(bsData[i]['timeStamp'])
        }
      
      }
        data.push(
          {
            y: dataSensing,
            x: time,
            name: selectedKotaName[x],
            type: "box"
          }
        )
    }

    let newLayout={...layout}; //cara copy objek, karena layoutlive merupakan layout utama, sedangkan yang ini akan berubah ubah sesuai tipe data
    newLayout.yaxis.title.text=labelsType(jenisData)
    newLayout.xaxis['title']={text: "waktu", standoff: 1}
    newLayout.title.text=`Grafik Min-max ${jenisData} dengan interval ${intervalInput.value} detik`
    
    newLayout.yaxis["type"]="log"
    newLayout.xaxis["type"]="date"

    Plotly.newPlot('myPlot'+jenisData, data, layout);
  
  }

function showPieold(jsonData){
    let colors = ['rgb(42, 190, 37)', 'rgb(37, 107, 190)', 'rgb(190, 49, 37)'];
    
    for (let p=0;p<selectedKota.length;p++){
      let bs=selectedKota[p];
      let bsData=jsonData[bs]
      

      

      for(let i=0;i<supportedSensor.length;i++){
        let data=[]
        let format;
        let title
        let addInfo=undefined;
        if(summaryType.value=="inQ"){
          format=getInQData(bsData, supportedSensor[i])
          title=`Grafik Perbandingan kuartil data ${supportedSensor[i]}`
          addInfo=`Q1=${Math.round(bsData [supportedSensor[i]]["Q1"]*100)/100}`+
                  `<br>Q3=${Math.round(bsData [supportedSensor[i]]["Q3"]*100)/100}`
        }else{
          format=getStatData(bsData, supportedSensor[i], removeZeros=true)
          title= `Grafik rasio data ${supportedSensor[i]}`
        }

      
      data.push({values: format[0], labels:format[1] 
        ,type:"pie"
        ,textinfo:"label+percent+value"
        ,textposition:"outside"
        ,marker: {
          colors: colors
        },
        rotation: 90,
      })

      let newLayout={...layout}; //cara copy objek, karena layoutlive merupakan layout utama, sedangkan yang ini akan berubah ubah sesuai tipe data
      newLayout.title.text=title
      
      if(addInfo!=undefined){
        newLayout['annotations']= [
          {
            text: addInfo,
            showarrow: false,
            x: 1.0,
            y: 0.5,
            font: {
              family: 'Arial',
              size: 14,
              color: 'black'
            }
          }
        ]
      }
      Plotly.newPlot("myPlot"+supportedSensor[i], data, newLayout);
    } 
  }
}

function showPie(jsonData, jenisData){
  let colors = ['rgb(42, 190, 37)', 'rgb(37, 107, 190)', 'rgb(190, 49, 37)'];


  let data=[]
  let addInfo="";
  let midText=[]

  let row=0
  let col=0;
  let numberOfRow=round(selectedKota.length/2)
  let distanceY=(1-0.4)/numberOfRow   // 0.4 itu pad atas+bawah

  for (let p=0;p<selectedKota.length;p++){
    let bs=selectedKota[p];
    let bsData=jsonData[bs]
  
        if(col==2){
          col=0;
          row=row+1
        }
        
      
      if(summaryType.value=="inQ"){
        format=getInQData(bsData, jenisData)
        title=`Grafik Perbandingan kuartil data ${jenisData}`
        addInfo+=`<br>Kuartil untuk ${selectedKotaName[p]}`+
                `<br>Q1=${Math.round(bsData [jenisData]["Q1"]*100)/100}`+
                `<br>Q3=${Math.round(bsData [jenisData]["Q3"]*100)/100}`
      }else{
        format=getStatData(bsData, jenisData, removeZeros=true)
        title= `Grafik rasio data ${jenisData}`
      }

      let posX=col==0?0.20:0.80
      let poxY=row==0?.80:0.20

      midText.push({font: {
        size: 20
        
      },
      text: selectedKotaName[p],
      showarrow: false,
      x: posX,
      y: poxY
    })





    
    data.push({values: format[0], labels:format[1] 
      ,type:"pie"
      ,textinfo:"label+percent+value"
      ,textposition:"outside"
      ,marker: {
        colors: colors
      },
      rotation: 90,
      domain: {
        row: row,
        column: col
      },
      name: selectedKotaName[p]
    })
    col+=1
  }
    let newLayout={...layout}; //cara copy objek, karena layoutlive merupakan layout utama, sedangkan yang ini akan berubah ubah sesuai tipe data
    newLayout.title.text=title
    
    newLayout['grid']={rows:row+1,columns:2}
    
    if(selectedKota.length==1){
      newLayout.grid.columns=1  //biar ketengah
    }

    if(addInfo!=undefined){
      newLayout['annotations']= [
        {
          text: addInfo,
          showarrow: false,
          x: 0.5,
          y: 1.0,
          font: {
            family: 'Arial',
            size: 14,
            color: 'black'
          }
        }
      ]

      for (let i=0;i<midText.length;i++){
        newLayout.annotations.push(midText[i])
      }
      newLayout.annotations.push(midText)
      console.log(newLayout)
    }
    Plotly.newPlot("myPlot"+jenisData, data, newLayout);
  

}

function showHistogram(jsonData,jenisData,gap=0){

  let data = [];

  for (let x=0;x<selectedKota.length;x++){
    let bs=selectedKota[x];
    let bsData=jsonData[bs]
  

      let sense=bsData[jenisData]
      let format;
      if(summaryType.value=="inQ"){
        format=getInQData(sense,undefined)
        addInfo=`Q1=${Math.round(bsData [jenisData]["Q1"]*100)/100}`+
                `<br>Q3=${Math.round(bsData [jenisData]["Q3"]*100)/100}`
      }else{
        format=getStatData(sense,undefined,false)
      }


      data.push(
        {
          y: format[0],
          x: format[1],
          name: selectedKotaName[x],
          type: "bar",
        }
      )
    
  }

  let newLayout={...layout}; //cara copy objek, karena layoutlive merupakan layout utama, sedangkan yang ini akan berubah ubah sesuai tipe data
  
  newLayout.title.text=`Grafik Histogram untuk ${jenisData}`
  
  newLayout.yaxis.title.text="Frekuensi"
  newLayout.xaxis['title']={text: labelsType(jenisData), standoff: 1}

  newLayout.xaxis.side="bottom"
  newLayout.yaxis["type"]="linear"
  newLayout.xaxis["type"]="category"
  newLayout['bargap']=gap
  

  if(summaryType.value=="inQ"){
    newLayout.title.text=`Grafik Histogram interkuartil untuk ${jenisData}`
  }

  Plotly.newPlot('myPlot'+jenisData, data, newLayout);
}


function getInQData(indata,tipe){
  let x;
  if(tipe!=undefined){
    x=[indata[tipe]["numQ1"], indata[tipe]["numQ2"],indata[tipe]["numQ3"]]
  }else{
    x=[indata["numQ1"], indata["numQ2"],indata["numQ3"]]

  }

  let y=["Q1", "Q2", "Q3"]

  return [x,y]
}

function getStatData(indata,tipe, removeZeros=false){
  let x;
  if(tipe!=undefined){
    x=indata[tipe]
  }else{
    x=indata
    
  }

  let incerement= (100/x.length)
  let y=[];
  for (let i=1;i<=100;i+=incerement){
    y.push(i+" - "+(i+incerement))
  }



  if(removeZeros){
    for (let i=0;i<100;i++){
       let pos=x.indexOf(0)
       console.log(pos)
        if(pos> -1){
          x.splice(pos,1)
          y.splice(pos,1)
        }    
    }
  }
  return [x,y]
}





function show(doAlert=true){


  if (!validInput(doAlert)){ 
    return null;
  }

    for (let i=0;i<graph.length;i++){
        graph[i].style.display="none";
    }


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

        
    if(tipe=='box' || tipe=="boxFloating"){
        jsonString.stat="raw"
    }else if(tipe=="summary"||tipe== "split-1"  ||
             tipe=="split-2"||tipe== "split-5" ||
             tipe=="split-10"||tipe== "split-20" 
    ){
      jsonString.stat=summaryType.value
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
                    if(tipe=="scatter"){
                        graph[0].style.display="block";
                        Plotly.purge(document.getElementById("myPlotsuhu"))
                        Plotly.purge(document.getElementById("myPlottekanan"))
                        Plotly.purge(document.getElementById("myPlotkelembapan"))
                        showScatter(responseResult)
                    }else if(tipe=="boxFloating"){
                        for (let m=0; m <supportedSensor.length;m++){
                            graph[(m)].style.display="block";
                            new showMinMax(responseResult,supportedSensor[m])
                        }
                    }else if(tipe=="box"){
                        for (let m=0; m <supportedSensor.length;m++){
                            graph[(m)].style.display="block";
                            new showBox(responseResult,supportedSensor[m]);
                        }
                    }else if(tipe=="summary"){
                      for (let m=0; m <supportedSensor.length;m++){
                        graph[(m)].style.display="block";
                      }
                      if(summaryGraph.value=="pie"){
                        for (let m=0; m <supportedSensor.length;m++){
                          graph[(m)].style.display="block";
                          showPie(responseResult,supportedSensor[m]) 
                        }
                      }else if(summaryGraph.value=="histogram"){
                        for (let m=0; m <supportedSensor.length;m++){
                          graph[(m)].style.display="block";
                          new showHistogram(responseResult,supportedSensor[m]);
                        }
                      }else if(summaryGraph.value=="box"){
                        for (let m=0; m <supportedSensor.length;m++){
                          graph[(m)].style.display="block";
                          new showHistogram(responseResult,supportedSensor[m],0.7);
                        }
                      }
                      
                    }
    

                }
            }).catch((error) => {
                console.log(error)
            });
    }




    optLokasi.addEventListener("change",function(event) {
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
      }


    optType.addEventListener("change",function(event) {
        console.log(event.target.value)
        scatterConf.hidden=true
        switch (event.target.value){
            case "scatter":
                scatterConf.hidden=false
                break;
            case "summary":
              summaryConf.hidden=false;
              break;
        }

        
  





    });