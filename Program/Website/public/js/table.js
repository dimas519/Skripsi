
const tabel=document.getElementById('tabeldump')

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
    }else if(intervalInput.value == ''){
      doAlert ? alert('Pilih interval') : null
      return false;
    }else if(optLokasi.value == ''){
      doAlert ? alert('Pilih Lokasi') : null
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
  



var bodytable=undefined;

function show(doAlert=true){
    if (!validInput(doAlert)){ 
        return null;
      }
    
      let start=`${startDate.value} ${startTime.value}`
      let end=`${endDate.value}-${endTime.value}`
      let bs=optLokasi.options[optLokasi.selectedIndex].text
      
    
      let jsonString={
        "node":`${optLokasi.value}`
        ,"start":`${start}:00`
        ,"end":`${end}:00`
        ,"interval":`${intervalInput.value}`
        ,'stat':"avg"
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

                    if(bodytable!=undefined){
                      bodytable.remove()
                    }
              
                    

                    bodytable=document.createElement("tbody")
                    
                
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

                        bodytable.appendChild(row)
                    }

                    tabel.append(bodytable)

                    // tabel
    
                    accInfo.style.display="block"
                    
                  
    
                }
    
                
            }).catch((error) => {
                console.log(error)
            });
    }