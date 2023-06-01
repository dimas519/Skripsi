


class Live{

    constructor(api){
        this.api=api;
        this.running=false;
    }

    sensing(identifier,interval){
        this.running=true
        let endpoint=this.api+identifier
        let suhu=document.getElementById("suhuText"+identifier)
        let kelembapan=document.getElementById("kelembapanText"+identifier)
        let tekanan=document.getElementById("tekananText"+identifier)
        let akselerasi=document.getElementById("akselerasiText"+identifier)


        let data
        this.intervalLive=setInterval(async function(){
            const response = await fetch(endpoint);
            data = await response.json();

            suhu.innerHTML=data['result']['T']
            kelembapan.innerHTML=data['result']['rh']
            tekanan.innerHTML=data['result']['Pa']
            akselerasi.innerHTML=data['result']['a']

        },interval);     

        



      }

    stop(){
        this.running=false
        clearInterval(this.intervalLive)
    }
    
}


function initNewLive(idBS,interval){

    let sensing=new Live("http://127.0.0.1:5000/realTime?idBS=");
    sensing.sensing(idBS,interval);
}

