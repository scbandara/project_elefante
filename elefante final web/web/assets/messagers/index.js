// Initialize cloud firestore from firebase
var db = firebase.firestore();



// read documents from firebase
const tbody1 =document.querySelector("#tbody1");

db.collection("nic").doc("1234").collection("messages").onSnapshot((querySnapshot) => {
    querySnapshot.forEach((doc) => {


        list_div.innerHTML+="<div class ='list-item'> <h3>"  + doc.data().title /* name can change to any thing you want.._*/ 
        +"</h3> <p>Message :  "+doc.data().description+ ""
     });
 });


