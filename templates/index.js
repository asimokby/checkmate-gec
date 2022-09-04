document.getElementById("hello").addEventListener("input", myFunction);
const checkHereParagraph = document.getElementById("checkHere");

let value = "";
function myFunction(e) {
  value = e.target.value;
  httpPost("http://localhost:5000/api");
}

function httpPost(theUrl) {
    checkHereParagraph.innerHTML = "";
    fetch(theUrl, {
        method: 'post',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(value)
      }).then(response => {
        return response.json();
      }).then(jsonResponse => {
        res = JSON.stringify(jsonResponse)
        console.log(typeof res);
       checkHereParagraph.innerHTML += res;
    
      }).catch (error => {
        console.log(error)
      })


//   var xmlHttp = new XMLHttpRequest();
//   xmlHttp.open("POST", theUrl, true);
//   xmlHttp.setRequestHeader("Content-Type", "application/json");
//   xmlHttp.send(
//     JSON.stringify({
//       value,
//     })
//   );
//   console.log(xmlHttp.responseText);
//   if (xmlHttp.readyState == 4) {
//     if (xmlHttp.status == 200) {
//       console.log(xmlHttp.responseText);
//     }
//   }
  //   httpGet("http://localhost:5000/api");
}

function httpGet(theUrl) {
  var xmlHttp2 = new XMLHttpRequest();
  xmlHttp2.open("GET", theUrl, false);
  xmlHttp2.send(null);
  console.log(xmlHttp2.responseText);
}
