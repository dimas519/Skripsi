
const tabel=document.getElementById('tabeldump')

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
    }
    return true;
  }
  



function show(doAlert=true){
    // if (!validInput(doAlert)){ 
      //   return null;
      // }
    
      let start=`${startDate.value} ${startTime.value}`
      let end=`${endDate.value}-${endTime.value}`
      let bs=optLokasi.options[optLokasi.selectedIndex].text
      
    
      let jsonString={
        "idBS":`${optLokasi.value}`
        ,"start":`${start}:00`
        ,"end":`${end}:00`
        ,"interval":`${intervalInput.value}`
    }
    
        
      jsonString={ //debugger
            "idBS":"AAAb"
            ,"start":"2023-05-08 00:00:00"
            ,"end":"2023-05-08 23:55:00"
            ,interval:1000
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
                    //buang yang sudah ada
                
                    document.getElementsByTagName("tbody").remove

                    let bodyTable=document.createElement("tbody")
                
                    tabel.parentElement.style.display="block"

                    responseResult=response['result']
                    console.log(responseResult[0]['timeStamp'])

                    for(let i=0;i<responseResult.length;i++){
                        let row=document.createElement('tr')

                        let time=document.createElement('td')
                        time.textContent=responseResult[i]['timeStamp']
                        time.classList.add("tabelData")
                        row.appendChild(time)

                        let suhu=document.createElement('td')
                        suhu.textContent=responseResult[i]['suhu']+"°C"
                        suhu.classList.add("suhu")
                        row.appendChild(suhu)

                        let kelembapan=document.createElement('td')
                        kelembapan.textContent=responseResult[i]['kelembapan']+"%"
                        kelembapan.classList.add("tabelData")
                        row.appendChild(kelembapan)

                        let tekanan=document.createElement('td')
                        tekanan.textContent=responseResult[i]['tekanan']+"kPa"
                        tekanan.classList.add("tabelData")
                        row.appendChild(tekanan)

                        let akselerasi=document.createElement('td')
                        akselerasi.textContent="("+responseResult[i]['akselerasi']["x"]+", "+responseResult[i]['akselerasi']["y"]+", "+responseResult[i]['akselerasi']["z"]+")"
                        akselerasi.classList.add("tabelData")
                        row.appendChild(akselerasi)

                        bodyTable.appendChild(row)
                    }

                    tabel.append(bodyTable)

                    // tabel
    
                    accInfo.style.display="block"
                    
                  
    
                }
    
                
            }).catch((error) => {
                console.log(error)
            });
    }