// Initialize cloud firestore from firebase
var db = firebase.firestore();



// read documents from firebase
const tbody1 =document.querySelector("#tbody1");

db.collection("detections").onSnapshot((querySnapshot) => {
    querySnapshot.forEach((doc) => {

        // var stdNo=0;
        // function AdditemsToTable(name,time,latitude,longitude){
        //     var tbody=doc.getElementById('tbody1');
        //     var td1 = doc.createElement('td');
        //     var td2 = doc.createElement('td');
        //     var td3 = doc.createElement('td');
        //     var td4 = doc.createElement('td');
        //     var td5 = doc.createElement('td');
        //     td1.innerHTML=++stdNo;
        //     td2.innerHTML=++name;
        //     td3.innerHTML=++time;
        //     td4.innerHTML=++latitude;
        //     td5.innerHTML=++longitude;
        //     trow.appendChild(td1);
        //     trow.appendChild(td2);
        //     trow.appendChild(td3);
        //     trow.appendChild(td4);
        //     trow.appendChild(td5);
        //     tbody.appendChild(trow);
        
           
        // }

        list_div.innerHTML+="<div class ='list-item'> <h3>"  + doc.data().name /* name can change to any thing you want.._*/ 
        +"</h3> <p>Name :  "+doc.data().name+ "  &nbsp &nbsp &nbsp- &nbsp &nbsp &nbsp Time :  "+doc.data().time+ " &nbsp &nbsp &nbsp- &nbsp &nbsp &nbspLongitude :  "+doc.data().longitude+ " &nbsp &nbsp &nbsp- &nbsp &nbsp &nbspLatitude :  "+doc.data().latitude+ "</p> </div>"
     });
 });


